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
import functools
import inject

from PyQt5 import QtCore
from PyQt5 import QtWidgets as QtGui
from PyQt5 import QtWidgets

from .list import DeviceListWidget

class USBWidget(QtGui.QWidget):
    _bright = False
    _actions = False

    @inject.params(manager='usb')
    def __init__(self, manager=None):
        """

        :param actions: 
        """
        super(USBWidget, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.translations = DeviceListWidget(self)

        #
        # self.scrollArea = QtGui.QScrollArea(self)
        # self.scrollArea.setGeometry(QtCore.QRect(5, 5, 390, 190))
        # self.scrollArea.setWidgetResizable(True)
        #
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.translations, -1)

        for device in manager.devices:
            self.translations.append(device.name)
