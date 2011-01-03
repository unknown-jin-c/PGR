#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

r"""

PGR - A Python for Gwt remote procedure call implementation

    - Description -

        This is simple small tool, for use both GWT (Google Web Toolkit) and GAE (Google App Engine)
        technologies together. This is a tool for simple and quick integration without using json
        as a communication protocol. If you use this library you can write GWT services implementation in
        Python, with full support of transfer primitive types, custom object types
        and exceptions objects, with full type translation.

        Now pgr is a set of python classes for full server side support of GWT rpc. But we also working
        on generator for automatically create all needed server side stuff.

    - Requirement -

        - GAE 1.1.0 or above
        - GWT 1.5 or above

    - History -

        2008-04-21  First implementation, support primitives, string and custom class

        2008-05-20  Added: Interceptors support, thread local context, some refactoring

    - How to use -

        1. Seting RPC Handler
           Simple set pgr.core.RpcHandler as request handler:

            ...
            from pgr import core
            ...

            # Set GwtRpcHandler as a handler for rpc call
            application = webapp.WSGIApplication(
                [('/services', core.RpcHandler)],
                debug=True)
            ...

        2. Adding interceptors
           Optionaly add some interceptors for rpc proccessing

            ...
            from pgr import auth
            from pgr import log
            ...
            core.RpcHandler.addInterceptr(auth.AuthorizationInterceptor())
            core.RpcHandler.addInterceptr(log.LoggingInterceptor())
            ...

        3. Implementing of service
           Now implement gwt service java interface:

            // file: /simpatico/pgr/test/service/TestService.java

            package simpatico.pgr.test.service;

            public interface TestService extends RemoteService {
                int sum(int a,int b);
            }

            by python implementation:

            # file: /simpatico/pgr/test/services.py

            from pgr import core

            class TestService():
                __serialization__ = {
                    'sum':   core.Types.INT
                }

                def sum(self, a, b):
                    return a + b

            ! __serialization__ property of service implementation class is a dict object
              with service methods names as keys and return types names as values, this is
              required because pgr need to know how to serialize return object. For primitive
              types and strings use pgr.core.Types dictionary from pgr library, for arrays use
              pgr.core.Types.getArrayType(name) method, where 'name' is name of array element type.

            ! Generator will be generate a base python class with __serialization__ property. The base class
              will be overwrite all time when GWT compiler will be run.

        4. Implementing VOs
           If you want use custom objects (VO, DTO) as a service methods parameters or return types, you must
           provide python implementation of this class.

            // file: /simpatico/pgr/test/vo/Obj1.java

            package simpatico.pgr.test.vo;
            import java.io.Serializable;

            public class Obj1 implements Serializable {

                private String str1;

                public void setStr1(String str1) {
                    this.str1 = str1;
                }
                public String getStr1() {
                    return str1;
                }
            }

            # file: /simpatico/pgr/test/vo.py

            from pgr import core

            class Obj1():
                __serialization__ = {
                    'str1': core.Types.STRING
                }

            ! __serialization__ property of custom class is a dict object
              with properties names as keys and types names as values, this is required
              because pgr need to know how to serialize object. For primitive types and strings
              use pgr.core.Types dictionary from pgr library, for arrays use
              pgr.core.Types.getArrayType(name) method, where 'name' is name of array element type.

            ! Generator will be generate all VO classes with __serialization__ property. The classes
              will be overwrite all time when GWT compiler will be run.

        5. Adding signatures descriptor.
           To pgr module you must add sig.py file with __signatures__
           property. This property is a dict with types and it's signature number, GWT use
           signatures for server/client side classes versioning. GWT generate signatures
           in compile time. Full list of signatures you can find in compiled javascript of
           your GWT classes, if you use PRETTY as gwt compile style, you find the signatures in
           similar line :

            function $clinit_173(){
                $clinit_173 = nullMethod;
                methodMap = {'com.google.gwt.user.client.rpc.IncompatibleRemoteServiceException/3936916533':[instantiate, deserialize, serialize], ...
                signatureMap = {'com.google.gwt.user.client.rpc.IncompatibleRemoteServiceException':'3936916533', 'java.lang.String':'2004016611', ...
            }

          you can copy whole line with signatureMap and paste it to python code:

            # file: /pgr/sig.py

            __signatures__ = {'com.google.gwt.user.client.rpc.IncompatibleRemoteServiceException':'3936916533', 'java.lang.String':'2004016611', ...

            ! Generator will be generate this file.

        6. Calling service.
           Simple call the service from your java code:

            TestServiceAsync ourInstance = (TestServiceAsync) GWT.create(TestService.class);
            ((ServiceDefTarget) ourInstance).setServiceEntryPoint("/services");
            ourInstance.sum(
               1, 2, new AsyncCallback(){
                public void onFailure(Throwable arg0) {
                    Window.alert(arg0.getMessage());
                    }
                public void onSuccess(Object arg0) {
                    Window.alert(arg0);
                }
            });

        7. Accessing request processing values.
           The pgr make accessible to whole rpc processing values by local thread
           value pgr.core.RpcHandler.ctx. User have access to:

              - request (google.appengine.ext.webapp.Request)
              - requestText (string) - encoded request body
              - requestObject (pgr.core._RpcRequest)
              - response (google.appengine.ext.webapp.Response)
              - responseObject - service methor return value
              - responseText (string)

           User can also store custom values on ctx object

        8. Custom interceptors.
           Pgr allow to add custom interceptors for request processing.
           On processing pgr core module call methods:

               - beforeRequestDecode
               - afterRequestDecode
               - beforeResponseDecode
               - afterResponseDecode
               - beforeExceptionDecode
               - afterExceptionDecode
               - beforeEvaluate
               - afterEvaluate

           Also interceptors can call methods on other interceptors by
           call static method pgr.core.RpcHandler._callInterceptors(name),
           where name parameter is name of other interceptors method.


    - ToDo -

        - Exceptions serialization
        - Generator of whole server side stuff
        - Java collections mapping to python list and dict types

"""

__author__ =    "Pawel Majewski <http://simpatico.pl/>"
__date__ =      "2008-06-20"
__version__ =   "0.3"
__credits__ =   """

    Copyright (c) 2008 Pawel Majewski  <http://simpatico.pl/>
    Licensed under GNU GPL 3.0 or later.  See license.txt included with this software.

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

__err_msg__ = {
    "ser.nf": """The implementation of '%s' service interface have not serialization information, class have to have __serialization__ property whit return type of service methods.""",
    "ser.met.nf": """The implementation of '%s.%s' service method have not information about return type, pleas update __serialization__ property in service class.""",
    "met.nf": """The implementation of '%s' service interface have not implement service method '%s'.""",
    "cnf": """Can't find or load implementation of class '%s'""",
    "pnf": """Can't find or load package (module) '%s'""",
    "sig.nf": """Can't find signatures dictionary, pleas add pgr.sig module with __signaturs__ property.""",
    "sig.tnf": """Can't find signatures for '%s' type, pleas correct pgr.sig.__signatures__ property.""",
    "sig.ne": """This application is perhaps out of date, the class signature on client and server side not equal for type '%s'."""
}


import sys
import new
import threading
import traceback
import logging

from pgr import sig
from google.appengine.ext import webapp


class Types:
    " Primitives, String and Array types signature enum "

    VOID = ''
    INT = 'I'
    LONG = 'J'
    SHORT = 'S'
    FLOAT = 'F'
    DOUBLE = 'D'
    BOOLEAN = 'Z'
    CHAR = 'C'
    BYTE = 'B'
    STRING = 'java.lang.String'

    ##
    # @param:  type object type
    # @return: array type name for providing object type name
    @staticmethod
    def getArrayType(type):
        if type.count('.') > 0:
            return '[L' + type + ';'
        return '[' + type

    ##
    # @param type full array type name
    # @return array element type name
    @staticmethod
    def getTypeFromArrayType(type):
        s = type
        if s.startswith("[L"):
            s = s[2:len(s)-1]
        else:
            if s.startswith("["):
                s = s[1:len(s)]
        return s


class RpcHandler(webapp.RequestHandler):
    " Handler for GWT rpc "

    ##
    # Local thread storage, use this field to access (or storing) processing
    # variables from interceptors or service implementation.
    # Accessible properties:
    #    request, requestText, requestObject (_RpcRequest) ,response, responseObject, responseText
    ctx = threading.local()

    ##
    # set of interceptors on request processing
    __interceptors__ = []

    ##
    # request processing start point
    def post(self):

        RpcHandler.ctx.request = self.request
        RpcHandler.ctx.response = self.response
        req = None

        try:
            rr = _RpcRequestReader()
            rw = _RpcResponseWriter()

            RpcHandler._callInterceptors("beforeRequestDecode")

            req = rr.readRequest(self.request.body)
            RpcHandler.ctx.requestObject = req

            RpcHandler._callInterceptors("afterRequestDecode")
            val = req.evaluate()
            RpcHandler._callInterceptors("beforeResponseDecode")

            resp = rw.encodeResponse(val, req)
            RpcHandler.ctx.responseText = resp

            RpcHandler._callInterceptors("afterResponseDecode")

            self.response.out.write(resp)

        except _RpcException, inst:
            logging.warning(inst)
            RpcHandler.ctx.exception = inst
            RpcHandler._callInterceptors("beforeExceptionDecode")
            resp = rw.encodeResponse(inst, req, True)
            RpcHandler.ctx.responseText = resp
            RpcHandler._callInterceptors("afterExceptionDecode")
            self.response.out.write(resp)

    ##
    # call interceptors on main proccessing points
    # @param methodName name of interceptor method
    @staticmethod
    def _callInterceptors(methodName):
        if len(RpcHandler.__interceptors__) > 0:
            for interceptor in RpcHandler.__interceptors__:
                if methodName in interceptor.__class__.__dict__:
                    method = getattr(interceptor, methodName)
                    method.__call__()

    ##
    # @param interceptor new interceptor
    @staticmethod
    def addInterceptr(intereptor):
        RpcHandler.__interceptors__.append(intereptor)


class _RpcRequest:
    " Request object "

    version = 0;
    flags = 0;

    moduleBaseURL = None
    strongName = None
    serviceIntfName = None
    serviceMethodName = None
    parameterTypes = None
    parameterValues = None
    returnType = None

    ##
    # excecute target service method
    # @return:
    def evaluate(self):
        classe = _RpcUtils.class_for_name(self.serviceIntfName)

        if self.serviceMethodName not in classe.__dict__:
            raise _RpcException(__err_msg__["met.nf"] %(self.serviceIntfName, self.serviceMethodName))

        serialization = {}
        methods = []

        _RpcUtils.multi_inherit_serialization(classe, serialization, methods)

        if len(serialization) > 0:
            if self.serviceMethodName in serialization:
                self.returnType = serialization[self.serviceMethodName]
            else:
                raise _RpcException(__err_msg__["ser.met.nf"] %(self.serviceIntfName, self.serviceMethodName))
        else:
            raise _RpcException(__err_msg__["ser.nf"] %(self.serviceIntfName))

        instance = new.instance(classe)
        method = getattr(instance, self.serviceMethodName)

        RpcHandler.ctx.serviceInstance = instance
        RpcHandler.ctx.methodInstance = method

        RpcHandler._callInterceptors("beforeEvaluate")
        val =  method.__call__(*self.parameterValues)
        RpcHandler.ctx.responseObject = val
        RpcHandler._callInterceptors("afterEvaluate")

        return val


class _RpcException(Exception):
    " Base PGR exception "
    pass

class _RpcRequestReader:
    " Reader of request "

    __content_type__ = "utf-8"
    __token_separator__ = u'\uffff'

    ##
    # read request object from string content
    # @param content request string
    # @return request object
    def readRequest(self, content):

        self.__tokenList = None
        self.__stringTable = None
        self.__seenArray = []
        self.__tokenListIndex = 0;

        gwtRpcRequest = _RpcRequest();
        self.__prepareToRead(content)
        
        print content
        print self.__tokenList;
        
        gwtRpcRequest.version = self.__readInt()
        gwtRpcRequest.flags = self.__readInt()

        self.__deserializeStringTable()

        if gwtRpcRequest.version > 2 :
            gwtRpcRequest.moduleBaseURL = self.__readString()
            gwtRpcRequest.strongName = self.__readString()

        gwtRpcRequest.serviceIntfName = self.__readString()
        gwtRpcRequest.serviceMethodName = self.__readString()

        paramCount = self.__readInt()
        gwtRpcRequest.parameterTypes = []

        for i in range(paramCount):
            gwtRpcRequest.parameterTypes.append(self.__readString())

        gwtRpcRequest.parameterValues = self.__readParametersValues(gwtRpcRequest.parameterTypes)
        return gwtRpcRequest

    def __prepareToRead(self, content):
        content = content.decode(self.__content_type__)
        self.__tokenList = content.split(self.__token_separator__)
        RpcHandler.ctx.requestText = str(self.__tokenList)


    def __deserializeStringTable(self):
        count = self.__readInt()
        self.__stringTable = []
        for i in range(count):
            self.__stringTable.append(self.__extract())

    def __readParametersValues(self, types):
        paramValues = []
        for type in types:
            paramValues.append(self.__deserializeValue(type))
        return paramValues

    def __deserializeValue(self, type):
        val = None
        try:
            val = {
               Types.INT: self.__readInt,
               Types.LONG: self.__readLong,
               Types.SHORT: self.__readShort,
               Types.FLOAT: self.__readFloat,
               Types.DOUBLE: self.__readDouble,
               Types.BOOLEAN: self.__readBoolean,
               Types.CHAR: self.__readChar,
               Types.BYTE: self.__readByte,
               Types.STRING: self.__readString
           }[type]()
        except KeyError:
            val =  self.__readObject()
        return val

    def __readInt(self):
        v = self.__extract()
        print v
        return int(v)

    def __readBoolean(self):
        return int(self.__extract()) == 1

    def __readDouble(self):
        return float(self.__extract())

    def __readFloat(self):
        return float(self.__extract())

    def __readLong(self):
        return eval("0X"+self.__extract()+"L")

    def __readShort(self):
        return int(self.__extract())

    def __readChar(self):
        return unichr(self.__readInt())

    # TODO Investigate
    def __readByte(self):
        return long(self.__extract())

    def __readString(self):
        return self.__getString(self.__readInt())

    def __getString(self, index):
        if index == 0:
            return None
        return self.__stringTable[index - 1]

    def __extract(self):
        var = self.__tokenList[self.__tokenListIndex]
        self.__tokenListIndex += 1
        return var

    def __readObject(self):

        token = self.__readInt()
        if token < 0:
            return self.__seenArray[(-(token + 1))]

        typeSignature = self.__getString(token)
        if typeSignature == None:
            return None
        return self.__deserialize(typeSignature)

    def __deserialize(self, typeSignature):
        si = typeSignature.rpartition("/")
        name = si[0]
        signature = si[2]

        if sig.__signatures__ == None:
            raise _RpcException(__err_msg__["sig.nf"])
        if name not in sig.__signatures__:
            raise _RpcException(__err_msg__["sig.tnf"] %(name))
        if sig.__signatures__[name] != signature:
            raise _RpcException(__err_msg__["sig.ne"] %(name))

        if name.startswith("["):
            return self.__deserializeArray(name)
        else:
            return self.__deserializeObject(name)

    def __deserializeArray(self, name):
        res = []
        len = self.__readInt()
        fun = None
        try:
            fun = {
                Types.getArrayType(Types.INT): self.__readInt,
                Types.getArrayType(Types.LONG): self.__readLong,
                Types.getArrayType(Types.SHORT): self.__readShort,
                Types.getArrayType(Types.FLOAT): self.__readFloat,
                Types.getArrayType(Types.DOUBLE): self.__readDouble,
                Types.getArrayType(Types.BOOLEAN): self.__readBoolean,
                Types.getArrayType(Types.CHAR): self.__readChar,
                Types.getArrayType(Types.BYTE): self.__readByte,
                Types.getArrayType(Types.STRING): self.__readString
           }[name]
        except KeyError:
            fun =  self.__readObject
        for i in range(len):
            res.append(fun())
        self.__seenArray.append(res)
        return res

    def __deserializeObject(self, name):
        classe = _RpcUtils.class_for_name(name)
        instance = new.instance(classe)

        serialization = dict()
        fields = []
        _RpcUtils.multi_inherit_serialization(classe, serialization, fields)
        for fname in fields:
            val = self.__deserializeValue(serialization[fname])
            instance.__dict__[fname] = val
        return instance

class _RpcResponseWriter:
    " Response writer "

    ##
    # create response string from result object
    # @param o object to serialization
    # @param req request object
    # @param ex is exception
    # @return response string
    def encodeResponse(self, o, req, ex = False):
        self.__objectCount = 0
        self.__objMap = dict()
        self.__tokenList = []
        self.__tokenListCharCount = 0
        self.__stringMap = dict()
        self.__stringTable = []
        self.__request = None
        self.__request = req

        if not ex:
            if self.__request.returnType != Types.VOID:
                self.__serializeValue(o, self.__request.returnType)
            prefix = "//OK"
        else:
            self.__serializeException(o)
            prefix = "//EX"

        return prefix + self.__toString()


    def __serializeValue(self, o, t):
        try:
            {
               Types.INT: self.__writeAsString,
               Types.LONG: self.__writeAsString,
               Types.SHORT: self.__writeAsString,
               Types.FLOAT: self.__writeAsString,
               Types.DOUBLE: self.__writeAsString,
               Types.BOOLEAN: self.__writeBoolean,
               Types.CHAR: self.__writeAsString,
               Types.BYTE: self.__writeAsString,
               Types.STRING: self.__writeString
            }[t](o)
        except KeyError:
            self.__writeObject(o, t)

    def __serializeException(self, ex):
        return

    def __addString(self, string):
        if string == None:
            return 0
        if string in self.__stringMap:
            return self.__stringMap[string]
        else:
            self.__stringTable.append(string)
            i = len(self.__stringTable)
            self.__stringMap[string] = i
            return i

    def __toString(self):
        buffer = ""
        buffer += "[";
        buffer = self.__writePayload(buffer)
        buffer = self.__writeStringTable(buffer)
        buffer = self.__writeHeader(buffer)
        buffer += "]"
        return buffer

    def __writePayload(self, b):

        for i in range(len(self.__tokenList)):
            k = len(self.__tokenList) - i  -1

            token = self.__tokenList[k]
            b += token
            if k > 0:
                b += ","
        return b

    def __writeStringTable(self, buffer):
        if len(self.__tokenList) > 0:
            buffer += ","
        buffer += "["
        for i in range(len(self.__stringTable)):
            if i > 0:
                buffer += ","
            buffer += self.__escapeString(self.__stringTable[i])
        buffer += "]"
        return buffer

    def __writeHeader(self, buffer):
        buffer += ","
        buffer += str(self.__request.flags)
        buffer += ","
        buffer += str(self.__request.version)
        return buffer

    def __escapeString(self, str):
        # TODO implement
        return '"' + str + '"'

    def __writeBoolean(self, b):
        val = {
             True : "1",
             False : "0"
        }[b]
        self.__append(val)

    def __writeString(self, value):
        self.__writeAsString(self.__addString(value));

    def __writeAsString(self, o):
        self.__append(str(o))


    def __writeObject(self, o, t = ""):
        if o == None:
            self.__writeString("null");
        else:
            if not isinstance(o, list):
                if o in self.__objMap:
                    pos = self.__objMap[o]
                    self.__writeAsString(-(pos + 1))
                else:
                    self.__objMap[o] = self.__objectCount
                    self.__objectCount +=1
            else:
                self.__objectCount +=1

            s = t
            s += "/"

            if sig.__signatures__ == None:
                raise _RpcException(__err_msg__["sig.nf"])
            if t not in sig.__signatures__:
                raise _RpcException(__err_msg__["sig.tnf"] %(t))

            s += sig.__signatures__[t]
            self.__writeString(s);

            if t.startswith("["):
                self.__serializeArray(o, t)
            else:
                self.__serialize(o, t)

    def __serialize(self, o, t):
        classe = _RpcUtils.class_for_name(t)
        serialization = dict()
        fields = []
        _RpcUtils.multi_inherit_serialization(classe, serialization, fields)
        for fname in fields:
            self.__serializeValue(o.__dict__[fname], serialization[fname])

    def __serializeArray(self, o, t):
        self.__writeAsString(len(o))
        try:
            fun = {
                Types.getArrayType(Types.INT): self.__writeAsString,
                Types.getArrayType(Types.LONG): self.__writeAsString,
                Types.getArrayType(Types.SHORT): self.__writeAsString,
                Types.getArrayType(Types.FLOAT): self.__writeAsString,
                Types.getArrayType(Types.DOUBLE): self.__writeAsString,
                Types.getArrayType(Types.BOOLEAN): self.__writeBoolean,
                Types.getArrayType(Types.CHAR): self.__writeAsString,
                Types.getArrayType(Types.BYTE): self.__writeAsString,
                Types.getArrayType(Types.STRING): self.__writeString
            }[t]
            for a in o:
                fun(a)
        except KeyError:
            for a in o:
                self.__writeObject(a, Types.getTypeFromArrayType(t))

    def __append(self, token):
        self.__tokenList.append(token);
        if token != None:
            self.__tokenListCharCount += len(token)

class _RpcUtils:
    " Reflection utility class "

    __class_cache__ = dict()

    ##
    # read serialization information from base class and its children
    # @param class class to be chcecked
    # @param dict target dictionary with field/method name as key and type as value
    # @param fileds target list with fields names
    @staticmethod
    def multi_inherit_serialization(classe, dict, fields):

        if "__serialization__" in classe.__dict__:
            for k in sorted(classe.__serialization__):
                dict[k] = classe.__serialization__[k]
                fields.append(k);

        for b in classe.__bases__:
            _RpcUtils.multi_inherit_serialization(b, dict, fields)

    ##
    # return class object for give name
    # @param class name (with package/module)
    # @return class object
    @staticmethod
    def class_for_name(name):
        if name in _RpcUtils.__class_cache__:
            return _RpcUtils.__class_cache__[name]

        className = None

        pos = name.rfind(".")
        if pos > -1:
            parts = name.rpartition(".")
            module = _RpcUtils.import_module(parts[0])
            className = parts[2]

        else:
            className = name
            module = globals()
        if className not in module.__dict__:
            raise _RpcException(__err_msg__["cnf"] %(name))

        classe = getattr(module, className)
        _RpcUtils.__class_cache__[name] = classe
        return classe

    ##
    # import module by name
    # @param name module name
    @staticmethod
    def import_module(name):
        try:
            mod = __import__(name)
        except Exception, inst:
            # Found some error in service source
            logging.exception(inst)
            raise _RpcException(__err_msg__["pnf"] %(name))
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod


