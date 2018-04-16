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
import inject


class Battery(object):

    def __init__(self, path=None):
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
        for result in glob.glob('%s/model_name' % self._path):
            return self.__pr__property_getoperty(result)
        return self._path

    @property
    def vendor(self):
        for result in glob.glob('%s/manufacturer' % self._path):
            return self.__pro__property_getperty(result)
        return None

    @property
    def technology(self):
        for result in glob.glob('%s/technology' % self._path):
            return self.__property_get(result)
        return None

    @property
    def exists(self):
        for result in glob.glob('%s/present' % self._path):
            return self.__property_get(result)
        return None

    @property
    def status(self):
        for result in glob.glob('%s/status' % self._path):
            return self.__property_get(result)
        return None

    @property
    def discharging(self):
        return self.status in ['Discharging']

    @property
    def current_now(self):
        for result in glob.glob('%s/current_now' % self._path):
            return int(self.__property_get(result))
        return 0

    @property
    def voltage_now(self):
        for result in glob.glob('%s/voltage_now' % self._path):
            return int(self.__property_get(result))
        return 0

    @property
    def consumption(self):
        current_now = self.current_now
        voltage_now = self.voltage_now
        if current_now and voltage_now:
            return current_now * voltage_now / 1000000000000
        return 0


class BatteryPool(object):

    def __init__(self, path='/sys/class/power_supply'):
        self._path = path

    @property
    def devices(self):
        for device in glob.glob('%s/BAT[0-9]*' % self._path):
            yield Battery(device)
