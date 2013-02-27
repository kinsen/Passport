
"""
This file reserved to upgrade nonblocking http request.

Note: blocking http request would block the whole web process,
but for simplify the demo, we use blocking request now.
"""

import sys
import json
import logging

#import eventlet
import httplib2
#httplib2 = eventlet.import_patched('httplib2')

from passport import settings
from passport import exception

#Just print log now
LOG = logging
LOG.debug = sys.stderr.write

class Httplib2Client(httplib2.Http):
    USER_AGENT = 'passport-httplib2client'
    
    def __init__(self, *args, **kargs):
        super(Httplib2Client, self).__init__(*args, **kargs)
        self.http_log_debug = settings.HTTP_LOG_DEBUG
    
    def http_log_resp(self, resp, body):
        if not self.http_log_debug:
            return
        
        LOG.debug("RESP:%s %s\n" % (resp, body))
    
    def http_log_req(self, args, kwargs):
        if not self.http_log_debug:
            return

        string_parts = ['curl']
        for element in args:
            if element in ('GET', 'POST', 'DELETE', 'PUT'):
                string_parts.append(' -X %s' % element)
            else:
                string_parts.append(' %s' % element)

        for element in kwargs['headers']:
            header = ' -H "%s: %s"' % (element, kwargs['headers'][element])
            string_parts.append(header)

        if 'body' in kwargs:
            string_parts.append(" -d '%s'" % (kwargs['body']))
        
        string_parts.append(" | python -mjson.tool")
            
        LOG.debug("\nREQ: %s\n" % "".join(string_parts))
    
    def request(self, *args, **kwargs):
        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = self.USER_AGENT
        kwargs['headers']['Accept'] = 'application/json'
        if 'body' in kwargs:
            kwargs['headers']['Content-Type'] = 'application/json'
            kwargs['body'] = json.dumps(kwargs['body'])

        self.http_log_req(args, kwargs)
        resp, body = super(Httplib2Client, self).request(*args, **kwargs)
        self.http_log_resp(resp, body)

        if body:
            # NOTE(alaski): Because force_exceptions_to_status_code=True
            # httplib2 returns a connection refused event as a 400 response.
            # To determine if it is a bad request or refused connection we need
            # to check the body. httplib2 tests check for 'Connection refused'
            # or 'actively refused' in the body, so that's what we'll do.
            try:
                body = json.loads(body)
            except ValueError:
                pass
        else:
            body = None

        if resp.status >= 400:
            raise exception.from_response(resp, body)

        return resp, body

HTTPClient = Httplib2Client