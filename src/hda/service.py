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


class HDA(object):

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
        return 'HDA - Intel HDA'

    @property
    def status(self):
        return self.__property_get(self._path)

    @property
    def optimized(self):
        return self.status in ['1']

    def powersafe(self):
        self.__property_set(self._path, '1')

    def performance(self):
        self.__property_set(self._path, '0')


class HDAPool(object):

    def __init__(self, path="/sys/module/snd_hda_intel/parameters/power_save"):
        self._path = path

    @property
    def devices(self):
        yield HDA(self._path)
