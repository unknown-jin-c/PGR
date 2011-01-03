    
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import cgi 
import wsgiref.handlers
from google.appengine.ext import webapp

# import PGR library
from pgr import core
from pgr import auth
from pgr import log

core.RpcHandler.addInterceptr(auth.AuthorizationInterceptor())
core.RpcHandler.addInterceptr(log.LoggingInterceptor())


# Set GwtRpcHandler as a handler for rpc call
application = webapp.WSGIApplication(
    [('/services', core.RpcHandler)], 
    debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)
  
if __name__ == '__main__':
    main()    