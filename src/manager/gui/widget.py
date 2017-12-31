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
import inject

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .list import DeviceListWidget
from .bar import ToolbarbarWidget


class ManagerWidget(QtWidgets.QWidget):
    _bright = False
    _actions = False

    @inject.params(manager='manager', battery='battery', dispatcher='event_dispatcher')
    def __init__(self, manager=None, battery=None, dispatcher=None):
        """

        :param actions: 
        """
        super(ManagerWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        dispatcher.add_listener('window.toggle_optimizer', self._onToggleOptimizer, 0)

        self.translations = DeviceListWidget(self)
        self.toolbar = ToolbarbarWidget()

        self.powerDevice = QtWidgets.QLabel(self)
        self.powerDevice.setText('Battery:')
        self.powerDevice.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.powerDevice.setFont(QtGui.QFont('SansSerif', 14))  # the title size is good

        self.powerConsumption = QtWidgets.QLabel(self)
        self.powerConsumption.setText('%.2f W' % battery.consumption)
        self.powerConsumption.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.powerConsumption.setFont(QtGui.QFont('SansSerif', 32, QtGui.QFont.Bold))  # the title size is good

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.powerDevice, -1)
        self.layout.addWidget(self.powerConsumption, -1)

        self.layout.addWidget(self.toolbar, -1)
        self.layout.addWidget(self.translations, -1)

        self.optimize = QtWidgets.QCheckBox(self.tr('Optimize perfomance automatically'))
        self.optimize.stateChanged.connect(self._onActionToggleOptimizer)
        self.optimize.setChecked(True)
        self.layout.addWidget(self.optimize, -1)

        self.scannerTimer = QtCore.QTimer(self)
        self.scannerTimer.timeout.connect(self._onRefresh)
        self.scannerTimer.setSingleShot(False)
        self.scannerTimer.start(1000)

        for device in manager.devices:
            self.translations.append(device)

    def _onToggleOptimizer(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        try:
            if self.optimize is None:
                return None
            self.optimize.setChecked(event.data)
        except (RuntimeError):
            return None

    @inject.params(dispatcher='event_dispatcher')
    def _onActionToggleOptimizer(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.toggle_optimizer', True if event else False)

    @inject.params(manager='manager', battery='battery')
    def _onRefresh(self, event=None, manager=None, battery=None):
        """

        :param event: 
        :return: 
        """
        if self.powerConsumption is None:
            return None

        message = '%.2f W' % battery.consumption
        self.powerConsumption.setText(message)
