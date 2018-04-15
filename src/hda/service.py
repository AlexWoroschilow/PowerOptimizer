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


class HDADevice(object):

    def __init__(self, path=''):
        self._path = path

    @property
    def name(self):
        return 'HDA - Intel HDA'

    @property
    def status(self):
        if os.path.isfile(self._path):
            with open(self._path, 'r', errors='ignore') as stream:
                return stream.read().strip("\n")
        return None

    @property
    def optimized(self):
        return self.status in ['1']

    def powersafe(self):
        with open(self._path, 'w') as stream:
            stream.write('1')
            stream.close()

    def performance(self):
        with open(self._path, 'w') as stream:
            stream.write('0')
            stream.close()


class HDA(object):

    def __init__(self, path="/sys/module/snd_hda_intel/parameters/power_save"):
        self._path = path

    @property
    def devices(self):
        yield HDADevice(self._path)
