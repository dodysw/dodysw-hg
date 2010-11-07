"""
Gudangterasi FB: Facebook bot toy
Copyright (C) 2010 Dody Suria Wijaya <dodysw@gmail.com>

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
import webbrowser, urllib, urllib2
from urlparse import urlparse, parse_qs
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

CONSUMER_KEY = "171458256203117"
CONSUMER_SECRET = "70da93e2f219db243ef05b3be71d05b3"

LOCAL_WEBSERVER_ADDR = 'localhost'
LOCAL_WEBSERVER_PORT = 7777

class FbHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.last_path = self.path
        self.send_response(200)
        self.end_headers()
        print >>self.wfile, "<html><head><title>Thank you</title></head><body onload='window.close();'><h1>Thank you</h1><p>You can now close this browser.</p></body></html>"

class FbSession:
    def __init__(self):
        self.redirect_uri = "http://%s:%s/" % (LOCAL_WEBSERVER_ADDR, LOCAL_WEBSERVER_PORT)
    
        self.FetchRequestToken()
        if not self.request_token:
            print "User does not accept authorization"
            return

        self.FetchAccessToken()
        
    def FetchRequestToken(self):
        uri = "https://graph.facebook.com/oauth/authorize?client_id=%s&redirect_uri=%s&scope=publish_stream" % (CONSUMER_KEY, self.redirect_uri)
        webbrowser.open(uri)
        httpd = HTTPServer((LOCAL_WEBSERVER_ADDR, LOCAL_WEBSERVER_PORT), FbHandler)
        httpd.handle_request()  #will block until one request
        self.request_token = parse_qs(urlparse(httpd.last_path).query).get('code',[None])[0]
    
    def FetchAccessToken(self):
        uri = "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (CONSUMER_KEY, self.redirect_uri, CONSUMER_SECRET, self.request_token)
        print uri
        req = urllib2.Request(uri)
        try:
            o = urllib2.urlopen(req)
            kv = parse_qs(o.read())
            if "access_token" in kv:
                self.access_token = kv["access_token"][0]
                print "Fetched acccess token:", self.access_token
        except urllib2.HTTPError, e:
            self._handleHttpError(e)

    def _handleHttpError(self, e):
        buff = e.read()
        print e, buff
    
    def 
    
    def post_feed(self, **kwargs):
        """http://developers.facebook.com/docs/reference/api/post
        """
        uri = "https://graph.facebook.com/me/feed"
        values = {
            "access_token":self.access_token
        }
        values.update(kwargs)
        payload = urllib.urlencode(values)
        print uri
        req = urllib2.Request(uri, payload)
        try:
            o = urllib2.urlopen(req)
            buff = o.read()
            try:
                return json.loads(buff)
            except ValueError:
                return buff
            
        except urllib2.HTTPError, e:
            self._handleHttpError(e)        


if __name__ == "__main__":
    fb = FbSession()
    if fb.access_token:
        fb.post_feed()