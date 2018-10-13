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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import configparser


class ConfigService(object):
    _parser = None

    def __init__(self, file=None):
        self._file = file
        self._parser = configparser.ConfigParser()
        if os.path.exists(self._file):
            self._parser.read(self._file)
            return None
                    
        folder = os.path.dirname(self._file)
        if len(folder) and not os.path.exists(folder):
            os.makedirs(folder)

        with open(self._file, 'w') as stream:
            self._parser.add_section('ignore')
            self._parser.set('ignore', 'cpu', '0')
            self._parser.set('ignore', 'hda', '0')
            self._parser.set('ignore', 'i2c', '0')
            self._parser.set('ignore', 'laptop', '0')
            self._parser.set('ignore', 'watchdog', '0')
            self._parser.set('ignore', 'pci', '0')
            self._parser.set('ignore', 'sata', '0')
            self._parser.set('ignore', 'usb', '0')
            
            self._parser.write(stream)
            stream.close()
            
        self._parser.read(self._file)
        return None

    def get(self, name, default=None):
        section, option = name.split('.', 1)
        if not self._parser.has_section(section):
            return None
        if self._parser.has_option(section, option):
            return self._parser.get(section, option)
        return None

    def set(self, name, value=None):
        section, option = name.split('.', 1)
        
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        
        self._parser.set(section, option, value)
        with open(self._file, 'w') as stream:
            self._parser.write(stream)
            stream.close()

    def has(self, name):
        section, option = name.split('.', 1)
        if self._parser.has_section(section):
            return self._parser.has_option(section, option)
        return False

