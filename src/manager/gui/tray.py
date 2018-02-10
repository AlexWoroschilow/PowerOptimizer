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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from gettext import gettext as _


class DictionaryTray(QtWidgets.QSystemTrayIcon):
    @inject.params(battery='battery', dispatcher='event_dispatcher')
    def __init__(self, app=None, battery=None, dispatcher=None):
        """
        
        :param app: 
        """

        self.scanBattery = True
        self.hidden = False

        icon = QtGui.QIcon("img/power-manager.svg")
        QtWidgets.QApplication.__init__(self, icon, app)
        self.activated.connect(self._onActionClick)

        self.menu = QtWidgets.QMenu()

        self.power = QtWidgets.QAction(self.menu)
        self.power.setText("Battery power consumption: \n%.2f W" % battery.consumption)
        self.power.setDisabled(True)
        self.menu.addAction(self.power)

        self.optimize = QtWidgets.QAction(_("Optimize perfomance automatically"), self.menu)
        self.optimize.triggered.connect(self._onActionToggleOptimizer)
        self.optimize.setCheckable(True)
        self.optimize.setChecked(self.scanBattery)
        self.menu.addAction(self.optimize)

        dispatcher.add_listener('window.toggle_optimizer', self._onRefreshCheckbox, 0)

        self.exit = QtWidgets.QAction(_("Exit"), self.menu)
        self.exit.triggered.connect(self._onActionExit)
        self.menu.addAction(self.exit)

        self.setContextMenu(self.menu)

        self.show()

    @inject.params(battery='battery', manager='manager')
    def update(self, battery=None, manager=None):
        """

        :param text: 
        :return: 
        """
        if self.power is not None:
            message = 'Battery power consumption: %.2f W' % battery.consumption
            self.power.setText(message)

    @inject.params(dispatcher='event_dispatcher')
    def _onActionClick(self, value=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """

        if value == self.Trigger:
            dispatcher.dispatch('window.toggle')

    def _onRefreshCheckbox(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        if self.optimize is None:
            return None
        self.optimize.setChecked(event.data)

    @inject.params(dispatcher='event_dispatcher')
    def _onActionToggleOptimizer(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.toggle_optimizer', event)

    @inject.params(dispatcher='event_dispatcher')
    def _onActionExit(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.exit')
