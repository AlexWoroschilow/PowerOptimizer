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
import os
import sys
import inject
import logging
import optparse

from multiprocessing import Pool

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

from lib.kernel import Kernel


class Application(Kernel):

    @inject.params(kernel='kernel', manager='manager', logger='logger')
    def run(self, kernel=None, manager=None, logger=None):
        
        pool = Pool(processes=int(kernel.options.thread))
        pool.map(manager._thread, manager.pool(
                kernel.options.perfomance
        ))


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--threads", default=4, dest="thread", help="Numer of threads to process the data")    
    parser.add_option("--perfomance", action="store_true", default=False, dest="perfomance", help="Switch to the performance mode")
    parser.add_option("--log-level", default=logging.DEBUG, dest="loglevel", help="Log level")
    parser.add_option("--log-file", default='power-manager.log', dest="logile", help="File to write the logs")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format, filename=options.logile)

    application = Application(options, args)
    sys.exit(application.run())
