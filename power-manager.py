#!/usr/bin/python3

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

import sys
import inject
import logging
import optparse

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from lib.kernel import Kernel


class Application(QtWidgets.QApplication):
    def __init__(self, options=None, args=None, dispatcher=None, logger=None):
        """

        :param options: 
        :param args: 
        """
        self.kernel = Kernel(options, args)
        self.window = None

        QtWidgets.QApplication.__init__(self, sys.argv)
        self.setQuitOnLastWindowClosed(False)

        dispatcher = self.kernel.get('event_dispatcher')
        dispatcher.add_listener('app.start', self.onWindowToggle)
        dispatcher.add_listener('window.toggle', self.onWindowToggle)
        dispatcher.add_listener('window.exit', self.onWindowExit)

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def exec_(self, dispatcher=None, logger=None):
        """

        :param dispather: 
        :param logger: 
        :return: 
        """
        dispatcher.dispatch('app.start', self)

        return super(Application, self).exec_()

    def onWindowToggle(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        if self.window is None:
            self.window = MainWindow()
            self.window.setWindowTitle('Power Optimizer')
            return self.window.show()

        self.window.close()
        self.window = None
        return None

    def onWindowExit(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.exit()


class MainWindow(QtWidgets.QFrame):
    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def __init__(self, parent=None, dispatcher=None, logger=None):
        """

        :param parent: 
        """

        super(MainWindow, self).__init__(parent)

        self.setMinimumHeight(500)
        self.setMinimumWidth(290)
        self.setFixedWidth(290)

        self.setWindowIcon(QtGui.QIcon("img/power-manager.svg"))

        self.tab = QtWidgets.QTabWidget(self)
        self.tab.setTabPosition(QtWidgets.QTabWidget.West)
        self.tab.setFixedSize(self.size())

        dispatcher.dispatch('window.tab', self.tab)

        self.show()

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def closeEvent(self, event, dispatcher=None, logger=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.toggle')

    def resizeEvent(self, event):
        """

        :param event: 
        :return: 
        """
        self.tab.setFixedSize(event.size())


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-t", "--tray", action="store_true", default=False, dest="tray", help="enable grafic user interface")
    parser.add_option("-g", "--gui", action="store_true", default=True, dest="gui", help="enable grafic user interface")
    parser.add_option("-w", "--word", default="baum", dest="word", help="word to translate")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
