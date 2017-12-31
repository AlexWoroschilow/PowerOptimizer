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
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets


class ToolbarbarWidget(QtWidgets.QToolBar):
    def __init__(self):
        super(ToolbarbarWidget, self).__init__()

        self.setOrientation(Qt.Horizontal)

        self.powersafe = QtWidgets.QAction(self.tr('Powersafe'), self)
        self.powersafe.triggered.connect(self._onPowersafe)
        self.addAction(self.powersafe)

        self.oprimized = QtWidgets.QAction(self.tr('Optimal'), self)
        self.oprimized.triggered.connect(self._onOptimize)
        self.addAction(self.oprimized)

        self.performance = QtWidgets.QAction(self.tr('Performance'), self)
        self.performance.triggered.connect(self._onPerformance)
        self.addAction(self.performance)

    @inject.params(manager='manager', dispatcher='event_dispatcher')
    def _onOptimize(self, event=None, manager=None, dispatcher=None):
        """

        :param event: 
        :param manager: 
        :return: 
        """
        dispatcher.dispatch('window.toggle_optimizer', True)
        manager.optimize()

    @inject.params(manager='manager', dispatcher='event_dispatcher')
    def _onPerformance(self, event=None, manager=None, dispatcher=None):
        """

        :param event: 
        :param manager: 
        :return: 
        """
        dispatcher.dispatch('window.toggle_optimizer', False)
        manager.performance()

    @inject.params(manager='manager', dispatcher='event_dispatcher')
    def _onPowersafe(self, event=None, manager=None, dispatcher=None):
        """

        :param event: 
        :param manager: 
        :return: 
        """
        dispatcher.dispatch('window.toggle_optimizer', False)
        manager.powersafe()
