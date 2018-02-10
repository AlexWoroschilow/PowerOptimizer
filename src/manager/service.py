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
    def __init__(self, battery=None):
        """
        
        :param battery: 
        """
        self._battery = battery
        self._devices = []
        self._perfomance = None
        self._powersafe = None

    def append(self, device):
        """
        
        :param device: 
        :return: 
        """
        self._devices.append(device)

    @property
    def devices(self):
        """
        
        :return: 
        """
        return self._devices

    @inject.params(logger='logger')
    def powersafe(self, logger=None):
        """

        :return: 
        """
        for device in self._devices:
            logger.debug('powersafe - %s' % device.name)
            device.powersafe()

        self._perfomance = False
        self._powersafe = True

    @inject.params(logger='logger')
    def performance(self, logger=None):
        """

        :return: 
        """

        for device in self._devices:
            logger.debug('performance - %s' % device.name)
            device.performance()

        self._perfomance = True
        self._powersafe = False

    @inject.params(logger='logger', battery='battery')
    def synchronize(self, logger=None, battery=None):
        """
        
        :param logger: 
        :param battery: 
        :return: 
        """

        if self._perfomance == True:
            return self.performance()

        if self._powersafe == True:
            return self.powersafe()

    @inject.params(logger='logger', battery='battery')
    def optimize(self, logger=None, battery=None):
        """

        :param logger: 
        :return: 
        """
        if battery.discharging == True:
            if self._perfomance in [True, None]:
                return self.powersafe()
            return True

        if self._powersafe in [True, None]:
            return self.performance()
        return None
