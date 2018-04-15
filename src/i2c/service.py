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


class I2CDevice(object):

    def __init__(self, path=''):
        self._path = path

    @property
    def name(self):
        for result in glob.glob('%s/name' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'r', errors='ignore') as stream:
                return "I2C - " + stream.read().strip("\n")
        return "I2C - " + self._path

    @property
    def status(self):
        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'r', errors='ignore') as stream:
                return stream.read().strip("\n")

        for result in glob.glob('%s/*/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'r', errors='ignore') as stream:
                return stream.read().strip("\n")

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
            with open(result, 'w') as stream:
                stream.write('auto')
                stream.close()

        for result in glob.glob('%s/*/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('auto')
                stream.close()

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
            with open(result, 'w') as stream:
                stream.write('on')
                stream.close()

        for result in glob.glob('%s/*/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('on')
                stream.close()

        return None


class I2C(object):

    def __init__(self, path="/sys/bus/i2c/devices"):
        self._path = path

    @property
    def devices(self):
        for device in glob.glob('%s/i2c-*' % self._path):
            yield I2CDevice(device)
