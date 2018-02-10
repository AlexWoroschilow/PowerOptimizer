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

from lib.plugin import Loader

from .service import Manager
from .gui.widget import ManagerWidget
from .gui.tray import DictionaryTray


class Loader(Loader):
    tray = None
    widget = None
    optimize = None

    @property
    def enabled(self):
        """

        :return:
        """
        return True

    @inject.params(battery='battery')
    def __create_manager(self, battery=None):
        """

        :param battery: 
        :return: 
        """
        return Manager(battery)

    def config(self, binder=None):
        """

        :param binder:
        :return:
        """

        binder.bind_to_constructor('manager', self.__create_manager)

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, dispatcher=None):
        """
        
        :param dispatcher: 
        :return: 
        """
        dispatcher.add_listener('window.tab', self._onWindowTab, -120)
        dispatcher.add_listener('window.toggle_optimizer', self._onToggleOptimizer, 0)
        dispatcher.add_listener('app.start', self._onAppStart, 0)

    def _onWindowTab(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        application = event.data
        if application is None:
            return None

        self.widget = ManagerWidget()
        application.addTab(self.widget, self.widget.tr('Devices'))

    def _onAppStart(self, event=None, dispatcher=None):
        """

        :param event:
        :param dispatcher:
        :return:
        """
        self.tray = DictionaryTray(event.data)

        self.timer = QtCore.QTimer(event.data)
        self.timer.timeout.connect(self._onActionUpdate)
        self.timer.setSingleShot(False)
        self.timer.start(10 * 1000)

        self.timer = QtCore.QTimer(event.data)
        self.timer.timeout.connect(self._onActionSynchronize)
        self.timer.setSingleShot(False)
        self.timer.start(60 * 1000)

    def _onToggleOptimizer(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        optimize = event.data
        if optimize is None:
            return None
        self.optimize = optimize

    @inject.params(battery='battery', manager='manager')
    def _onActionUpdate(self, battery=None, manager=None):
        """

        :param value: 
        :param manager: 
        :return: 
        """
        self.tray.update()

        if self.optimize == True:
            manager.optimize()

    @inject.params(battery='battery', manager='manager')
    def _onActionSynchronize(self, battery=None, manager=None):
        """

        :param value: 
        :param manager: 
        :return: 
        """
        manager.synchronize()
