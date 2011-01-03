#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

r"""

PGR AUTH - Authorization interceptor for PGR library

    - Description -

        This a simple rpc interceptor for provide custom authorization for Ajax
        applications.

    - History -

        2008-05-20:  First version
        2008-06-23:  Move session persistence from DB to Memcache

    - Requirement -

        - GAE 1.1.0 or above
        - PGR 0.3 or above
        - Cookies enabled in browser

    - How to use -

        1. Add Authorization interceptor to PGR request handler:

            core.RpcHandler.addInterceptr(auth.AuthorizationInterceptor())

        2. From your custom login service call userAuthenticated method with two parameters:
            - authenticated user role
            - your custom object to store in session (e.g. for user identification)

            auth.AuthorizationInterceptor.userAuthenticated("adm", None)

        3. Set permission to your services methods by set __perm__ property in service class,
           __perm__ is  a dict object with method name as key and roles array as value

            __perm__ = {
                "subArray" : ["user", "manager"],
                "subObject" : ["adm"]
            }

        4. If rpc try to access restricted method then exception is throw
           to client side (there no specialized exception for accces denied)

        5. On user logout call userDeauthenticated() method

            auth.AuthorizationInterceptor.userDeauthenticated()

    - Todo -

        - Add java specialized exception for caching on client side
        - Add @Prem java annotation for compile time generation of __perm__ property 


"""

__author__ =    "Pawel Majewski <http://simpatico.pl/>"
__date__ =      "2008-06-23"
__version__ =   "0.3"
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

import datetime
import random
import sys
import pickle

from pgr import core
from google.appengine.api import memcache

class AuthorizationException(core._RpcException):
    "General authentication exception"

class _Subject:
    pass

class AuthorizationInterceptor:
    "Request Authorization interceptor"

    instance = None

    # in minutes
    SESSION_TIMEOUT = 1
    SESSION_TICKET = "sessionTicket"
    COOKIE_EXP = 1

    def beforeEvaluate(self):
        isTicketFinded = False
        isTicketFine = False
        ticketOwner = None


        core.RpcHandler._callInterceptors("beforeAuthorization")

        ctx = core.RpcHandler.ctx
        req = ctx.request
        res = ctx.response
        met = ctx.methodInstance
        inst = ctx.serviceInstance

        ctx.user = None

        if self.SESSION_TICKET in req.cookies:
            ctx.sessionTicket = req.cookies[self.SESSION_TICKET]
            isTicketFinded, isTicketFine, ticketOwner = self.__getDataFromTicket(
                ctx.sessionTicket, req, res)

        # check the permission (autorizate)
        if "__perm__" in inst.__class__.__dict__:
            if met.__name__ in inst.__perm__:
                if not isTicketFinded:
                    raise AuthorizationException("Forbidden method (%s) access without ticket" % met.__name__)
                if isTicketFinded and not isTicketFine:
                    raise AuthorizationException("Forbidden method (%s) access with expired ticket" % met.__name__)
                if ticketOwner == None:
                    raise AuthorizationException("Forbidden method (%s) access with invalid ticket" % met.__name__)

                havePerm = False
                if ticketOwner.roles in inst.__perm__[met.__name__]:
                    havePerm = True

                if not havePerm:
                    raise AuthorizationException("Forbidden method (%s) access" % met.__name__)


        if ticketOwner != None:
            ctx.user = ticketOwner

        core.RpcHandler._callInterceptors("afterAuthorization")

    ##
    # end of current session
    @staticmethod
    def userDeauthenticated():

        res = core.RpcHandler.ctx.response
        result = False

        core.RpcHandler._callInterceptors("beforeUserDeauthentication")
        if core.RpcHandler.ctx.user != None:
            au = core.RpcHandler.ctx.user

            memcache.delete(au.sessionTicket)

            expires = datetime.datetime.now()
            res.headers.add_header(
                'Set-Cookie', str(AuthorizationInterceptor.SESSION_TICKET + "=; expires=%s" % expires.ctime()))
            core.RpcHandler._callInterceptors("afterbeforeUserDeauthentication")
            core.RpcHandler.ctx.user = None
            result = True

        return result

    ###
    # start new session
    # @param roles subject rolesa
    # @param userObject custom object stored with subject
    @staticmethod
    def userAuthenticated(roles, userObject):

        req = core.RpcHandler.ctx.request
        res = core.RpcHandler.ctx.response

        core.RpcHandler._callInterceptors("beforeUserAuthentication")
        ticket = AuthorizationInterceptor.__getNewTicket()

        au = _Subject()
        au.sessionTicket = ticket
        au.roles = roles
        au.sessionStratTime = datetime.datetime.now()
        au.sessionIp = req.remote_addr
        au.userObject = userObject

        memcache.set(ticket, pickle.dumps(au), AuthorizationInterceptor.SESSION_TIMEOUT * 60)

        expires = datetime.datetime.now() + datetime.timedelta(days=AuthorizationInterceptor.COOKIE_EXP)
        res.headers.add_header(
            'Set-Cookie', str(AuthorizationInterceptor.SESSION_TICKET + "=" + ticket +"; expires=%s" % expires.ctime()))
        core.RpcHandler._callInterceptors("afterUserAuthentication")
        return True

    ##
    # get data for ticket and update access time for ticket if found
    # @return tuple of (is_ticket_finded, is_fine_ticket, subject)
    def __getDataFromTicket(self, ticket, req, resp):
        isTicket = False
        isActual = False
        appUser = None

        # memcache mechanism remove expired ticket by self
        sesdata = memcache.get(ticket)
        isTicket = sesdata != None
        appUser = None
        isActual = True

        if isTicket:
            appUser = pickle.loads(sesdata)
            # is no timeout and ip is not changed
            isActual = isActual and appUser.sessionIp == req.remote_addr

            if isActual:
                appUser.sessionLastTime = datetime.datetime.now()

                memcache.set(ticket, sesdata, AuthorizationInterceptor.SESSION_TIMEOUT * 60)

                # set cookie
                expires = datetime.datetime.now() + datetime.timedelta(days=AuthorizationInterceptor.COOKIE_EXP)
                resp.headers.add_header(
                    'Set-Cookie', str(AuthorizationInterceptor.SESSION_TICKET + "=" + appUser.sessionTicket +"; expires=%s" % expires.ctime()))
            else:
                memcache.delete(ticket)
                appUser = None

        return (isTicket, isActual, appUser)


    ###
    # @return new generated ticket
    #
    @staticmethod
    def __getNewTicket():
        ticket = ''.join([random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890') for x in xrange(20)])
        if memcache.get(ticket) != None:
            return AuthorizationInterceptor.__getNewTicket()
        else:
            return ticket
    