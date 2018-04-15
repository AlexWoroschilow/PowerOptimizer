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
import inject


class Manager(object):

    @inject.params(logger='logger')
    def _thread(self, method=None, logger=None):
        try:
            method()
        except PermissionError as ex:
            logger.error(ex)

    def __init__(self, battery=None):
        self._battery = battery
        self._devices = []

    def append(self, device):
        self._devices.append(device)

    @property
    def devices(self):
        return self._devices

    @inject.params(logger='logger')
    def pool(self, performance=False, logger=None):
        tasks_pool = []
        for device in self._devices:
            logger.debug('pool  - %s: %s' % (device.name, 'performance' if performance else 'powersafe'))
            tasks_pool.append(device.performance if performance else device.powersafe)
        return tasks_pool

    @inject.params(logger='logger')
    def powersafe(self, logger=None):
        for device in self._devices:
            logger.debug('powersafe - %s' % device.name)
            device.powersafe()
            
    @inject.params(logger='logger')
    def performance(self, logger=None):
        for device in self._devices:
            logger.debug('performance - %s' % device.name)
            device.performance()
