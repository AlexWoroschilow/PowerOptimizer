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


class PowerDevice(object):
    def __init__(self, path=''):
        """

        :param path: 
        """
        self._path = path

    def __property(self, path=None):
        """

        :param path: 
        :return: 
        """
        try:

            if not path or not os.path.isfile(path):
                return 0
            with open(path, 'r') as stream:
                return stream.read().strip("\n")
        except OSError:
            return 0
        return 0

    @property
    def name(self):
        """

        :return: 
        """
        for result in glob.glob('%s/model_name' % self._path):
            return self.__property(result)
        return self._path

    @property
    def vendor(self):
        for result in glob.glob('%s/manufacturer' % self._path):
            return self.__property(result)
        return None

    @property
    def technology(self):
        for result in glob.glob('%s/technology' % self._path):
            return self.__property(result)
        return None

    @property
    def exists(self):
        for result in glob.glob('%s/present' % self._path):
            return self.__property(result)
        return None

    @property
    def status(self):
        for result in glob.glob('%s/status' % self._path):
            return self.__property(result)
        return None

    @property
    def discharging(self):
        for status in self.status:
            if status in ['Discharging']:
                return True
        return False

    @property
    def current_now(self):
        for result in glob.glob('%s/current_now' % self._path):
            return int(self.__property(result))
        return 0

    @property
    def voltage_now(self):
        for result in glob.glob('%s/voltage_now' % self._path):
            return int(self.__property(result))
        return 0

    @property
    def consumption(self):
        """
        
        :return: 
        """
        current_now = self.current_now
        voltage_now = self.voltage_now
        if current_now and voltage_now:
            return current_now * voltage_now / 1000000000000
        return 0


class Battery(object):
    def __init__(self, path='/sys/class/power_supply'):
        """

        :param path: 
        """
        self._path = path

    @property
    def devices(self):
        """

        :return: 
        """
        for device in glob.glob('%s/BAT[0-9]' % self._path):
            yield PowerDevice(device)
