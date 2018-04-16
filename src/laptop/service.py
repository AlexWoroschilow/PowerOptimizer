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
# WITHOUT WARRANTIES OR CONDITION
import os
import inject


class LaptopMode(object):

    def __init__(self, path=''):
        self._path = path

    @inject.params(logger='logger')
    def __property_get(self, path=None, logger=None):
        try:
            if not path or not os.path.isfile(path):
                return None
            with open(path, 'r', errors='ignore') as stream:
                return stream.read().strip("\n")
        except (OSError, IOError) as ex:
            logger.error(ex)
            return None
        return None

    @inject.params(logger='logger')
    def __property_set(self, path=None, value=None, logger=None):
        try:
            if not path or not os.path.isfile(path):
                return None
            with open(path, 'w', errors='ignore') as stream:
                stream.write(value)
                stream.close()
        except (OSError, IOError) as ex:
            logger.error(ex)
        return None

    @property
    def name(self):
        return "Laptop mode"

    @property
    def status(self):
        return self.__property_get(self._path)

    @property
    def optimized(self):
        return self.status in ['5']

    def powersafe(self):
        """
        (On older kernels you may need to use noatime instead of relatime.)
        Also consider merely using a larger value for the commit option. This defines how often changed data is written to the disk (it is cached until then). 
        The default value is 5 seconds.
        See man mount(8) for details on how the rel/noatime and commit options work.
        Use laptop_mode to reduce disk usage by delaying and grouping writes. You should enable it, at least while on battery. 
        See Laptop-mode for more details:        
        :return:  None
        """
        self.__property_set(self._path, '5')
        return None

    def performance(self):
        """
        (On older kernels you may need to use noatime instead of relatime.)
        Also consider merely using a larger value for the commit option. This defines how often changed data is written to the disk (it is cached until then). 
        The default value is 5 seconds.
        See man mount(8) for details on how the rel/noatime and commit options work.
        Use laptop_mode to reduce disk usage by delaying and grouping writes. You should enable it, at least while on battery. 
        See Laptop-mode for more details:        
        :return: 
        """
        self.__property_set(self._path, '0')
        return None


class LaptopModePool(object):

    def __init__(self, path="/proc/sys/vm/laptop_mode"):
        self._path = path

    @property
    def devices(self):
        yield LaptopMode(self._path)
