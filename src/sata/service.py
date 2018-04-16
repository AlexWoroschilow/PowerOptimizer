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


class Sata(object):

    def __init__(self, path=''):
        """
        min_power
        This mode sets the link to its lowest power state (SLUMBER) when there is no I/O on the disk. 
        This mode is useful for times when an extended period of idle time is expected.

        medium_power
        This mode sets the link to the second lowest power state (PARTIAL) when there is no I/O on the disk. 
        This mode is designed to allow transitions in link power states (for example during times of intermittent heavy I/O and idle I/O) 
        with as small impact on performance as possible.
        medium_power mode allows the link to transition between PARTIAL and fully-powered (that is "ACTIVE") states, depending on the load. 
        Note that it is not possible to transition a link directly from PARTIAL to SLUMBER and back; in this case, 
        either power state cannot transition to the other without transitioning through the ACTIVE state first.

        max_performance
        ALPM is disabled; the link does not enter any low-power state when there is no I/O on the disk.

        To check whether your SATA host adapters actually support ALPM you can check if the file /sys/class/scsi_host/host*/link_power_management_policy exists. 
        To change the settings simply write the values described in this section to these files or display the files to check for the current setting.

        :param path: 
        """
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
        return "SATA - %s" % self._path

    @property
    def status(self):
        for result in glob.glob('%s/link_power_management_policy' % self._path):
            if not os.path.isfile(result):
                continue
            return self.__property_get(result)
        return None

    @property
    def optimized(self):
        return self.status in ['min_power']

    def powersafe(self):
        """
        min_power
        This mode sets the link to its lowest power state (SLUMBER) when there is no I/O on the disk. 
        This mode is useful for times when an extended period of idle time is expected.

        medium_power
        This mode sets the link to the second lowest power state (PARTIAL) when there is no I/O on the disk. 
        This mode is designed to allow transitions in link power states (for example during times of intermittent heavy I/O and idle I/O) 
        with as small impact on performance as possible.
        medium_power mode allows the link to transition between PARTIAL and fully-powered (that is "ACTIVE") states, depending on the load. 
        Note that it is not possible to transition a link directly from PARTIAL to SLUMBER and back; in this case, 
        either power state cannot transition to the other without transitioning through the ACTIVE state first.

        max_performance
        ALPM is disabled; the link does not enter any low-power state when there is no I/O on the disk.

        :return: 
        """
        for result in glob.glob('%s/link_power_management_policy' % self._path):
            if not os.path.isfile(result):
                continue
            self.__property_set(result, 'min_power')

    def performance(self):
        """
        min_power
        This mode sets the link to its lowest power state (SLUMBER) when there is no I/O on the disk. 
        This mode is useful for times when an extended period of idle time is expected.

        medium_power
        This mode sets the link to the second lowest power state (PARTIAL) when there is no I/O on the disk. 
        This mode is designed to allow transitions in link power states (for example during times of intermittent heavy I/O and idle I/O) 
        with as small impact on performance as possible.
        medium_power mode allows the link to transition between PARTIAL and fully-powered (that is "ACTIVE") states, depending on the load. 
        Note that it is not possible to transition a link directly from PARTIAL to SLUMBER and back; in this case, 
        either power state cannot transition to the other without transitioning through the ACTIVE state first.

        max_performance
        ALPM is disabled; the link does not enter any low-power state when there is no I/O on the disk.

        :return: 
        """
        for result in glob.glob('%s/link_power_management_policy' % self._path):
            if not os.path.isfile(result):
                continue
            self.__property_set(result, 'max_performance')


class SataPool(object):

    def __init__(self, path="/sys/class/scsi_host/"):
        self._path = path

    @property
    def devices(self):
        for device in glob.glob('%s/*' % self._path):
            yield Sata(device)
