#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

r"""

PGR LOGGING - Example interceptor for PGR library


    - History -

        2008-05-27:  First version

"""

__author__ =    "Pawel Majewski <http://simpatico.pl/>"
__date__ =      "2008-05-27"
__version__ =   "0.1"
__credits__ =   """

    Copyright (c) 2008 Pawel Majewski  <http://simpatico.pl/>
    Licensed under GNU GPL 3.0 or later. See license.txt included with this software.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import logging

from pgr.core import RpcHandler

class LoggingInterceptor:
    " Logging interceptor for PGR "

    # Methods call by core PGR module

    def beforeRequestDecode(self):
        logging.info("beforeRequestDecode")
        pass

    def afterRequestDecode(self):
        logging.info("afterRequestDecode")
        pass

    def beforeResponseDecode(self):
        logging.info("beforeResponseDecode")
        pass

    def afterResponseDecode(self):
        logging.info("afterResponseDecode")
        pass

    def beforeExceptionDecode(self):
        logging.error("beforeExceptionDecode")
        pass

    def afterExceptionDecode(self):
        logging.error("afterExceptionDecode")
        pass

    def beforeEvaluate(self):
        logging.info("beforeEvaluate")
        pass

    def afterEvaluate(self):
        logging.info("afterEvaluate")
        pass


    # Methods call by Authentication interceptor if it is attached


    def beforeAuthorization(self):
        logging.info("beforeAuthorization")
        pass

    def afterAuthorization(self):
        logging.info("afterAuthorization")
        pass

    def beforeUserDeauthentication(self):
        logging.info("beforeUserDeauthentication")
        pass

    def afterbeforeUserDeauthentication(self):
        logging.info("afterbeforeUserDeauthentication")
        pass

    def beforeUserAuthentication(self):
        logging.info("beforeUserAuthentication")
        pass

    def afterUserAuthentication(self):
        logging.info("afterUserAuthentication")
        pass