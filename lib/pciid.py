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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
import re
import copy
import time


class Vendor(object):
    delimeter = '  '

    def __init__(self, string=None):
        self._id = None
        self._name = None

        start = string.find(self.delimeter)
        self._id = string[:start]
        self._name = string[start + len(self.delimeter):]

        self._devices = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def append(self, device):
        self._devices.append(device)


class Device(object):
    delimeter = '  '

    def __init__(self, vendor=None, string=None):
        start = string.find(self.delimeter)
        self._id = string[:start]
        self._name = string[start + len(self.delimeter):]

        self._vendor = vendor

    @property
    def id(self):
        return self._id

    @property
    def vendor(self):
        return self._vendor.id

    @property
    def name(self):
        return self._name

    def __str__(self):
        return "%s (%s)" % (
            self._name,
            self._vendor.name
        )


class SubDevice(Device):

    def __init__(self, vendor=None, string=None, parent=None):
        start = string.find(self.delimeter)

        self._id, self._sub_id = string[:start].split(' ')
        self._name = string[start + len(self.delimeter):]

        self._parent = parent
        self._vendor = vendor


class Manager(object):

    def __init__(self, path='res/pci.ids'):
        self._devices = []
        self._vendors = []
        self._hashmap = {}
        with open(path, 'r', errors='ignore') as stream:

            vendor = None
            device = None

            for line in stream.readlines():
                if line.find('# List of known device classes') == 0:
                    break

                line = line.strip("\n")
                if line.find("#") in [0]:
                    continue

                if len(line) and line.count("\t") == 0:
                    vendor = Vendor(line)
                    self.addVendor(vendor)
                    continue

                if len(line) and line.count("\t") == 1:
                    line = line.strip("\t")
                    device = Device(vendor, line)
                    vendor.append(device)
                    self.addDevice(device)
                    continue

                if len(line) and line.count("\t") == 2:
                    line = line.strip("\t")
                    sub_device = SubDevice(vendor, line, device)
                    vendor.append(sub_device)
                    self.addDevice(sub_device)
                    continue

    @property
    def devices(self):
        return self._devices

    @property
    def vendors(self):
        return self._vendors

    def addDevice(self, device=None):
        self._hashmap["%s:%s" % (
            device.vendor,
            device.id,
        )] = device

        self._devices.append(device)

    def addVendor(self, vendor=None):
        self._vendors.append(vendor)

    def has(self, code=None):
        return code in self._hashmap

    def get(self, code=None):
        if code is not None and self.has(code):
            return self._hashmap[code]
        return None


def main(path=None):
    # Syntax:
    # vendor  vendor_name
    # 	device  device_name				<-- single tab
    # 		subvendor subdevice  subsystem_name	<-- two tabs
    manager = Manager(path)
    for device in manager.devices:
        print(device)

# if __name__ == "__main__":
    # main('/usr/share/misc/pci.ids')
#     main('../usb.ids')
