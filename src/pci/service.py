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


class PCIDevice(object):
    def __init__(self, path=''):
        """

        :param path: 
        """
        self._path = path
        self._name = path

    def _read(self, path=None):
        """
        
        :param path: 
        :return: 
        """
        with open(path, 'r') as stream:
            return stream.read().strip("\n")
        return path

    @property
    def name(self):
        return "PCI - " + self._name

    @name.setter
    def name(self, value):
        """
        
        :param value: 
        :return: 
        """
        self._name = value

    @property
    def unique(self):
        return "%s:%s" % (
            self.vendor,
            self.device,
        )

    @property
    def device(self):
        """

        :return: 
        """
        device = self._read('%s/device' % self._path)
        return device.strip('0x')

    @property
    def vendor(self):
        """

        :return: 
        """
        device = self._read('%s/vendor' % self._path)
        return device.strip('0x')

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
        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('auto')
                stream.close()

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
        for result in glob.glob('%s/power/control' % self._path):
            if not os.path.isfile(result):
                continue
            with open(result, 'w') as stream:
                stream.write('on')
                stream.close()


class PCI(object):
    def __init__(self, path="/sys/bus/pci/devices/"):
        """

        :param path: 
        """
        self._path = path
        self._manager = Manager()

    @property
    def devices(self):
        """

        :return: 
        """
        for device_path in glob.glob('%s/*' % self._path):
            pci_device = PCIDevice(device_path)
            pci_device.name = pci_device.unique
            if self._manager.has(pci_device.unique):
                device = self._manager.get(pci_device.unique)
                pci_device.name = device.__str__()
            yield pci_device
