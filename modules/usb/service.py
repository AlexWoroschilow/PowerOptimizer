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

from lib.pciid import Manager


class Pool(object):

    manager = Manager('res/usb.ids')

    @property
    @inject.params(config='config')
    def devices(self, config=None):
        if int(config.get('ignore.usb')):
            return None
        
        for path in glob.glob('/sys/bus/usb/devices/*'):
            
            device = USB(path)
            if device.unique is None:
                continue

            device.name = device.unique
            if self.manager.has(device.unique):
                device_recognized = self.manager.get(device.unique)
                device.name = device_recognized.__str__()

            unique = device.unique.replace(':', '/')
            if unique is not None and not config.has('ignore_usb.%s' % unique):
                config.comment('ignore_usb', device.name, '0, do not ignore by default')
                config.set('ignore_usb.%s' % unique, '0')
                
            if int(config.get('ignore_usb.%s' % unique)):
                continue
                
            yield device


class USB(object):

    def __init__(self, path=''):
        self.path = path
        self._name = None

    @inject.params(logger='logger')
    def _read(self, path=None, logger=None):
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
    def _write(self, path=None, value=None, logger=None):
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
        if self._name != None:
            return "USB - %s" % self._name

        for result in glob.glob('%s/interface' % self.path):
            if not os.path.isfile(result):
                continue
            return "USB - %s" % self._read(result)

        if self.unique != None:
            return "USB - %s" % self.unique

        return "USB - %s" % self.path

    @name.setter
    def name(self, value=None):
        self._name = value

    @property
    def unique(self):
        vendor = self.vendor
        device = self.device
        if vendor is not None and len(vendor) and device is not None and len(device):
            return "%s:%s" % (vendor, device)
        return None

    @property
    def device(self):
        return self._read('%s/idProduct' % self.path)

    @property
    def vendor(self):
        return self._read('%s/idVendor' % self.path)

    @property
    def status(self):
        for result in glob.glob('%s/power/control' % self.path):
            if not os.path.isfile(result):
                continue
            return self._read(result)
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
        for result in glob.glob('%s/power/autosuspend' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, '0')

        for result in glob.glob('%s/power/level' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, 'auto')

        for result in glob.glob('%s/power/autosuspend_delay_ms' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, '0')

        for result in glob.glob('%s/power/control' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, 'auto')

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
        for result in glob.glob('%s/power/autosuspend' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, '-1')

        for result in glob.glob('%s/power/level' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, 'on')

        for result in glob.glob('%s/power/autosuspend_delay_ms' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, '-1')

        for result in glob.glob('%s/power/control' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, 'on')
