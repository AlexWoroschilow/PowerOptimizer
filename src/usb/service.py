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
from lib.pciid import Manager


class USBDevice(object):

    def __init__(self, path=''):
        self._path = path
        self._name = None

    def _read(self, path=None):
        if os.path.exists(path):
            with open(path, 'r') as stream:
                return stream.read().strip("\n")
        return None

    @property
    def name(self):
        if self._name != None:
            return "USB - " + self._name

        for result in glob.glob('%s/interface' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'r') as stream:
                return "USB - " + stream.read().strip("\n")

        if self.unique != None:
            return "USB - " + self.unique

        return "USB - " + self._path

    @name.setter
    def name(self, value=None):
        self._name = value

    @property
    def unique(self):
        vendor = self.vendor
        device = self.device
        if vendor != None and device != None:
            return "%s:%s" % (vendor, device)
        return None

    @property
    def device(self):
        return self._read('%s/idProduct' % self._path)

    @property
    def vendor(self):
        return self._read('%s/idVendor' % self._path)

    @property
    def status(self):
        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'r') as stream:
                return stream.read().strip("\n")
        return None

    @property
    def optimized(self):
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
        self._path = path
        self._manager = Manager('./usb.ids')

    @property
    def devices(self):
        for device in glob.glob('%s/*' % self._path):
            device_usb = USBDevice(device)
            if self._manager.has(device_usb.unique):
                device = self._manager.get(device_usb.unique)
                device_usb.name = device.__str__()
            yield device_usb
