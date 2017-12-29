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


class USBDevice(object):
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
        for result in glob.glob('%s/product' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'r') as stream:
                return stream.read().strip("\n")
        return self._path

    @property
    def status(self):
        """
        
        :return: 
        """

        for result in glob.glob('%s/power/control' % self._path):
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
        return self.status in ['auto']


    def powersafe(self):
        """
        https://www.kernel.org/doc/Documentation/usb/power-management.txt

        According to the docs, there were several changes to the USB power management from kernels 2.6.32, 
        which seem to settle in 2.6.38. Now you'll need to wait for the device to become idle, 
        which is governed by the particular device driver. The driver needs to support it, otherwise 
        the device will never reach this state. Unluckily, now the user has no chance to force this. 
        However, if you're lucky and your device can become idle, then to turn this off you need to:

        :return: 
        """
        for result in glob.glob('%s/power/autosuspend' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('0')
                stream.close()

        for result in glob.glob('%s/power/level' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('auto')
                stream.close()

        for result in glob.glob('%s/power/autosuspend_delay_ms' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('0')
                stream.close()

        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('auto')
                stream.close()

    def performance(self):
        """
        https://www.kernel.org/doc/Documentation/usb/power-management.txt

        According to the docs, there were several changes to the USB power management from kernels 2.6.32, which seem to settle in 2.6.38. Now you'll need to wait for the device to become idle, which is governed by the particular device driver. The driver needs to support it, otherwise the device will never reach this state. Unluckily, now the user has no chance to force this. However, if you're lucky and your device can become idle, then to turn this off you need to:

        echo "0" > "/sys/bus/usb/devices/usbX/power/autosuspend"
        echo "auto" > "/sys/bus/usb/devices/usbX/power/level"
        or, for kernels around 2.6.38 and above:

        echo "0" > "/sys/bus/usb/devices/usbX/power/autosuspend_delay_ms"
        echo "auto" > "/sys/bus/usb/devices/usbX/power/control"
        This literally means, go suspend at the moment the device becomes idle.

        So unless your fan is something "intelligent" that can be seen as a device and controlled by a driver, you probably won't have much luck on current kernels.

        :return: 
        """
        for result in glob.glob('%s/power/autosuspend' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('-1')
                stream.close()

        for result in glob.glob('%s/power/level' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('on')
                stream.close()

        for result in glob.glob('%s/power/autosuspend_delay_ms' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('-1')
                stream.close()

        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('on')
                stream.close()


class USB(object):
    def __init__(self, path="/sys/bus/usb/devices/"):
        """
        
        :param path: 
        """
        self._path = path

    @property
    def devices(self):
        """

        :return: 
        """
        for device in glob.glob('%s/*' % self._path):
            yield USBDevice(device)
