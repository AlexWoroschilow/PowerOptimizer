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


class I2C(object):

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
        for result in glob.glob('%s/name' % self._path):
            if not os.path.isfile(result):
                continue
            return "I2C -%s " % self.__property_get(result)
        return "I2C - %s" % self._path

    @property
    def status(self):
        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            return self.__property_get(result)

        for result in glob.glob('%s/*/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            return self.__property_get(result)
        return None

    @property
    def optimized(self):
        return self.status in ['auto']

    def powersafe(self):
        """
        The /sys/devices/.../power/control attribute allows the user
        space to control the run-time power management of the device.

        All devices have one of the following two values for the
        power/control file:

        + "auto\n" to allow the device to be power managed at run time;
        + "on\n" to prevent the device from being power managed;

        The default for all devices is "auto", which means that they may
        be subject to automatic power management, depending on their
        drivers.  Changing this attribute to "on" prevents the driver
        from power managing the device at run time.  Doing that while
        the device is suspended causes it to be woken up.

        :return: 
        """
        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            self.__property_set(result, 'auto')
            
        for result in glob.glob('%s/*/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            self.__property_set(result, 'auto')

        return None

    def performance(self):
        """

        The /sys/devices/.../power/control attribute allows the user
        space to control the run-time power management of the device.

        All devices have one of the following two values for the
        power/control file:

        + "auto\n" to allow the device to be power managed at run time;
        + "on\n" to prevent the device from being power managed;

        The default for all devices is "auto", which means that they may
        be subject to automatic power management, depending on their
        drivers.  Changing this attribute to "on" prevents the driver
        from power managing the device at run time.  Doing that while
        the device is suspended causes it to be woken up.

        :return: 
        """
        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            self.__property_set(result, 'on')

        for result in glob.glob('%s/*/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            self.__property_set(result, 'on')

        return None


class I2CPool(object):

    def __init__(self, path="/sys/bus/i2c/devices"):
        self._path = path

    @property
    def devices(self):
        for device in glob.glob('%s/i2c-*' % self._path):
            yield I2C(device)
