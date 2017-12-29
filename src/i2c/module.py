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

from .service import I2C
from .gui.widget import I2CWidget

class Loader(Loader):
    @property
    def enabled(self):
        """

        :return:
        """
        return True

    def config(self, binder):
        """

        :param binder:
        :return:
        """

        binder.bind('i2c', I2C())

    @inject.params(manager='manager', bus='i2c', dispatcher='event_dispatcher')
    def boot(self, manager=None, bus=None, dispatcher=None):
        """

        :param manager: 
        :param cpu: 
        :return: 
        """
        for device in bus.devices:
            manager.append(device)


        dispatcher.add_listener('window.tab', self.OnWindowTab, -90)


    def OnWindowTab(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        widget = I2CWidget()
        event.data.addTab(widget, widget.tr('I2C'))
