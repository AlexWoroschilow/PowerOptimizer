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
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .list import DeviceListWidget


class ManagerWidget(QtWidgets.QWidget):
    _bright = False
    _actions = False

    @inject.params(manager='manager', battery='battery')
    def __init__(self, manager=None, battery=None):
        """

        :param actions: 
        """
        super(ManagerWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.translations = DeviceListWidget(self)

        self.acceptButton = QtWidgets.QPushButton(self)
        self.acceptButton.setGeometry(QtCore.QRect(100, 100, 100, 25))
        self.acceptButton.setText("Optimize")
        self.acceptButton.clicked.connect(self._onOptimize)

        QtCore.QTimer.singleShot(1000, self._onRefresh)

        self.label = QtWidgets.QLabel(self)
        self.label.setText('%.2f W' % battery.consumption)
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label.setFont(QtGui.QFont('SansSerif', 28, QtGui.QFont.Bold))  # the title size is good

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label, -1)

        self.layout.addWidget(self.translations, -1)
        self.layout.addWidget(self.acceptButton, -1)

    @inject.params(manager='manager', battery='battery')
    def _onRefresh(self, event=None, manager=None, battery=None):
        """
        
        :param event: 
        :return: 
        """
        self.translations.clear()
        for device in manager.devices:
            self.translations.append(device.name, device.optimized)
        self.label.setText('%.2f W' % battery.consumption)

        QtCore.QTimer.singleShot(1000, self._onRefresh)

    @inject.params(manager='manager', battery='battery')
    def _onOptimize(self, event=None, manager=None, battery=None):
        """
        
        :param event: 
        :param manager: 
        :return: 
        """
        if battery.discharging:
            return manager.powersafe()
        return manager.performance()
