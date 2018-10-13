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

    manager = Manager()

    @property
    @inject.params(config='config')
    def devices(self, config=None):
        if int(config.get('ignore.pci')):
            return None
        
        for path in glob.glob('/sys/bus/pci/devices/*'):
            
            device = PCI(path)
            if device.unique is None:
                continue
            
            device.name = device.unique
            if self.manager.has(device.unique):
                device_recognized = self.manager.get(device.unique)
                device.name = device_recognized.__str__()
                
            unique = device.unique.replace(':', '/')
            if unique is not None and not config.has('pci.%s' % unique):
                config.set('pci.%s' % unique, '0')
                
            yield device


class PCI(object):

    def __init__(self, path=''):
        self.path = path
        self._name = path

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
        return "PCI - %s" % self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def unique(self):
        return "%s:%s" % (
            self.vendor,
            self.device,
        )

    @property
    def device(self):
        value = self._read('%s/device' % self.path)
        return value.strip('0x')

    @property
    def vendor(self):
        value = self._read('%s/vendor' % self.path)
        return value.strip('0x')

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
        Each device in the driver model has a flag to control whether it is subject to runtime power management. 
        This flag, runtime_auto, is initialized by the bus type (or generally subsystem) code using pm_runtime_allow() or pm_runtime_forbid(); 
        the default is to allow runtime power management.

        The setting can be adjusted by user space by writing either “on” or “auto” to the device’s power/control sysfs file. 
        Writing “auto” calls pm_runtime_allow(), setting the flag and allowing the device to be runtime power-managed by its driver. 
        Writing “on” calls pm_runtime_forbid(), clearing the flag, returning the device to full power if it was in a low-power state, 
        and preventing the device from being runtime power-managed. User space can check the current value of the runtime_auto flag by reading that file.
        The device’s runtime_auto flag has no effect on the handling of system-wide power transitions. 

        In particular, the device can (and in the majority of cases should and will) be put into a low-power state during a system-wide transition to a sleep state even though its runtime_auto flag is clear.
        For more information about the runtime power management framework, refer to Documentation/power/runtime_pm.txt.
        :return: 
        """
        for result in glob.glob('%s/power/control' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, 'auto')

    def performance(self):
        """
        Each device in the driver model has a flag to control whether it is subject to runtime power management. 
        This flag, runtime_auto, is initialized by the bus type (or generally subsystem) code using pm_runtime_allow() or pm_runtime_forbid(); 
        the default is to allow runtime power management.

        The setting can be adjusted by user space by writing either “on” or “auto” to the device’s power/control sysfs file. 
        Writing “auto” calls pm_runtime_allow(), setting the flag and allowing the device to be runtime power-managed by its driver. 
        Writing “on” calls pm_runtime_forbid(), clearing the flag, returning the device to full power if it was in a low-power state, 
        and preventing the device from being runtime power-managed. User space can check the current value of the runtime_auto flag by reading that file.
        The device’s runtime_auto flag has no effect on the handling of system-wide power transitions. 

        In particular, the device can (and in the majority of cases should and will) be put into a low-power state during a system-wide transition to a sleep state even though its runtime_auto flag is clear.
        For more information about the runtime power management framework, refer to Documentation/power/runtime_pm.txt.

        :return: 
        """
        for result in glob.glob('%s/power/control' % self.path):
            if not os.path.isfile(result):
                continue
            self._write(result, 'on')
