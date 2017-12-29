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
from lib.plugin import Loader

from .service import Manager
from .gui.widget import ManagerWidget


class Loader(Loader):
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

    def config(self, binder):
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
        dispatcher.add_listener('window.tab', self.OnWindowTab, -120)


    def OnWindowTab(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        widget = ManagerWidget()
        event.data.addTab(widget, widget.tr('Devices'))


#         # while True:
#         #     time.sleep(2)
#         #     print(battery.status)
#         # for device in manager._devices:
#         #     print(device.powersafe())
#         #     print(device.performance())
#
#         for device in manager.devices:
#         #     device.performance()
#             print(device.name, device.status)
