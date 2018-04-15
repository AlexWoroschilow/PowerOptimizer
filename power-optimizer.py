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
import time

from multiprocessing import Pool

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

from lib.kernel import Kernel


class Application(Kernel):

    @inject.params(kernel='kernel', manager='manager', logger='logger')
    def run(self, kernel=None, manager=None, logger=None):
        
        logger.info('Switch to %s mode' % ('performance' if kernel.options.perfomance else 'powersave'))
        pool = Pool(processes=int(kernel.options.thread))
        pool.map(manager._thread, manager.pool(
                kernel.options.perfomance
        ))


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--threads", default=4, dest="thread", help="Numer of threads to process the data")    
    parser.add_option("--performance", action="store_true", default=False, dest="perfomance", help="Switch to the performance mode")
    parser.add_option("--log-level", default=logging.DEBUG, dest="loglevel", help="Log level")
    parser.add_option("--log-file", default=None, dest="logile", help="File to write the logs")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=int(options.loglevel), filename=options.logile, format=log_format)

    application = Application(options, args)
    sys.exit(application.run())
