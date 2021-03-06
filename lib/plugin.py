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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
class Loader(object):

    def __init__(self, options, args):
        """

        :param options: 
        :param args: 
        """
        self._options = options
        self._args = args

    def __enter__(self):
        """
        
        :return: 
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        
        :param type: 
        :param value: 
        :param traceback: 
        :return: 
        """
        pass

    @property
    def enabled(self):
        """

        :return: 
        """
        return True

    def config(self, binder):
        """

        :return: 
        """

    def boot(self, options=None, args=None):
        """
        
        :param event_dispatcher: 
        :return: 
        """
