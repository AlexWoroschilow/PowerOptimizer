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
import functools
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import Qt


class DeviceListWidget(QtWidgets.QListView):
    def __init__(self, parent):
        """

        :param actions: 
        """
        super(DeviceListWidget, self).__init__(parent)
        self.parent = parent
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setModel(QtGui.QStandardItemModel())

        self.scannerTimer = QtCore.QTimer(self)
        self.scannerTimer.timeout.connect(self._onRefresh)
        self.scannerTimer.setSingleShot(False)
        self.scannerTimer.start(2000)

    def _onRefresh(self, event=None):
        """
        
        :param event: 
        :return: 
        """

        model = self.model()
        if model is None:
            return None

        for index in range(0, model.rowCount()):
            item = model.item(index)
            device = item.device
            item.setCheckState(2 if device.optimized else 0)

    def append(self, device):
        """
        
        :param string: 
        :return: 
        """

        model = self.model()
        if model is None:
            return None

        item = QtGui.QStandardItem(device.name)
        item.setCheckState(2 if device.optimized else 0)
        item.setCheckable(False)
        item.device = device

        model.appendRow(item)
