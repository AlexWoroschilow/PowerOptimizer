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
import glob


class HDADevice(object):
    def __init__(self, path=''):
        """

        :param path: 
        """
        self._path = path

    @property
    def name(self):
        """

        :return: 
        """
        return 'Intel HDA'

    @property
    def status(self):
        """

        :return: 
        """
        if os.path.isfile(self._path):
            with open(self._path, 'r') as stream:
                return stream.read().strip("\n")
        return None

    @property
    def optimized(self):
        """

        :return: 
        """
        return self.status in ['1']

    def powersafe(self):
        """

        :return: 
        """
        with open(self._path, 'w') as stream:
            stream.write('1')
            stream.close()

    def performance(self):
        """

        :return: 
        """
        with open(self._path, 'w') as stream:
            stream.write('0')
            stream.close()


class HDA(object):
    def __init__(self, path="/sys/module/snd_hda_intel/parameters/power_save"):
        """

        :param path: 
        """
        self._path = path

    @property
    def devices(self):
        """

        :return: 
        """
        yield HDADevice(self._path)
