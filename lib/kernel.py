# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import glob
import logging
import inject

import importlib
from lib.event import Dispatcher


class Kernel(object):

    def __init__(self, options=None, args=None, sources="src/**/module.py"):
        """_
        
        :param self: 
        :param options: 
        :param args: 
        :param config: 
        :return: 
        """
        self._options = options
        self._sources = sources
        self._args = args
        self._loaders = []

        inject.configure(self.__configure_container)

        for loader in self._loaders:
            if hasattr(loader.__class__, 'boot') and \
            callable(getattr(loader.__class__, 'boot')):
                loader.boot(options, args)

        self._container = inject.get_injector()
        ed = self._container.get_instance('event_dispatcher')
        ed.dispatch('kernel.start')

    @property
    def options(self):
        return self._options

    @property
    def args(self):
        return self._args

    def __configure_container(self, binder):
        binder.bind('kernel', self)
        
        logger = logging.getLogger('app')
        binder.bind('logger', logger)
        
        logger = logging.getLogger('dispatcher')
        binder.bind('event_dispatcher', Dispatcher(logger))

        logger = logging.getLogger('kernel')
        for module_source in self.__modules(self._sources):
            try:
                module = importlib.import_module(module_source, False)
                with module.Loader(self._options, self._args) as loader:
                    if not loader.enabled:
                        continue
                    
                    if hasattr(loader.__class__, 'config') and \
                    callable(getattr(loader.__class__, 'config')):
                            binder.install(loader.config)
                            
                    self._loaders.append(loader)
                    
            except (SyntaxError, RuntimeError) as err:
                logger.critical("%s: %s" % (module_source, err))
                continue

    def __modules(self, mask=None):
        logger = logging.getLogger('kernel')
        for source in glob.glob(mask):
            if os.path.exists(source):
                logger.debug("config: %s" % source)
                yield source[:-3].replace('/', '.')

    def get(self, name):
        if self._container is None:
            return None
        return self._container.get_instance(name)
