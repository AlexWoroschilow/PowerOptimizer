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


class LaptopDevice(object):

    def __init__(self, path=''):
        self._path = path

    @property
    def name(self):
        return "Laptop mode"

    @property
    def status(self):
        with open(self._path, 'r') as stream:
            return stream.read().strip("\n")
        return None

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
        with open(self._path, 'w') as stream:
            stream.write('5')
            stream.close()
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
        with open(self._path, 'w') as stream:
            stream.write('0')
            stream.close()
        return None


class Laptop(object):

    def __init__(self, path="/proc/sys/vm/laptop_mode"):
        self._path = path

    @property
    def devices(self):
        yield LaptopDevice(self._path)
