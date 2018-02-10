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


class CPUDevice(object):
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
        return "CPU - " + self._path

    @property
    def status(self):
        """

        :return: 
        """

        for result in glob.glob('%s/cpufreq/scaling_governor' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'r') as stream:
                return stream.read().strip("\n")
        return None

    @property
    def optimized(self):
        """

        :return: 
        """
        return self.status in ['powersave']

    def powersafe(self):
        """

        :return: 
        """
        for result in glob.glob('%s/cpufreq/scaling_governor' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('powersave')
                stream.close()

    def performance(self):
        """

        :return: 
        """
        for result in glob.glob('%s/cpufreq/scaling_governor' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('performance')
                stream.close()


class CPU(object):
    def __init__(self, path="/sys/devices/system/cpu/"):
        """
        
        :param path: 
        """
        self._path = path

    @property
    def devices(self):
        """

        :return: 
        """
        for device in glob.glob('%s/cpu[0-9]' % self._path):
            yield CPUDevice(device)
