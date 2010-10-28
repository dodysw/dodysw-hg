"""
Gudangterasi YM: Yahoo messenger bot that return top google result
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

import urllib, urllib2, random, time
import json

# change this to your own api number, get it from https://developer.apps.yahoo.com/dashboard/createKey.html
CONSUMER_KEY = "dj0yJmk9V0t0MXFVTUNUbjFhJmQ9WVdrOVUwMVRhSE01TlRBbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD05Zg--"
CONSUMER_SECRET = "1822a3db9b80e117a731ea288998d513244c0249"

class SimpleOAuth:
    """Generate correct Authoriation header based on consumer key&secret, oauth_token&secret"""

    def __init__(self, oauth_server, oauth_consumer_key, oauth_consumer_secret, oauth_token="", oauth_token_secret="", realm=None):
        self.oauth_server = oauth_server
        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_consumer_secret = oauth_consumer_secret
        if realm is None:
            realm = "yahooapis.com"
        self.realm = realm
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        #init token
        self.updateTokenAccess()

    def updateTokenAccess(self):
        """Sign all keys to get a new token and token secret, must redo after oauth_expires_in second
        """
        headers = self.getHeaderNoCheck()
        req = urllib2.Request(self.oauth_server, None, headers)
        try:
            o = urllib2.urlopen(req)
            resp = o.read()
            self.access_token = dict([el.split("=") for el in resp.split("&")])
            print "Access token", self.access_token
            self.last_token_update = time.time()
            self.updateToken(self.access_token['oauth_token'], self.access_token['oauth_token_secret'])
            return True
        except urllib2.HTTPError, e:
            self._handleHttpError(e)
        return False

    def getHeader(self):
        if time.time() > (self.last_token_update + int(self.access_token['oauth_expires_in'])):
            self.updateTokenAccess()
        return self.getHeaderNoCheck()

    def getHeaderNoCheck(self):
        headers = {}
        headers["Authorization"] ="""OAuth realm="%s",oauth_consumer_key="%s",oauth_signature_method="PLAINTEXT",oauth_nonce="%s",oauth_timestamp="%s",oauth_signature="%s",oauth_token="%s",oauth_version="1.0\"""" % (
            self.realm,
            self.escape(self.oauth_consumer_key), 
            self.escape(self.generate_nonce()), 
            self.escape(str(self.generate_timestamp())), 
            self.escape("%s&%s" % (self.oauth_consumer_secret,self.oauth_token_secret)), 
            self.oauth_token)
        return headers
        
    def updateToken(self, new_oauth_token, new_oauth_token_secret = None):
        self.oauth_token = new_oauth_token
        if new_oauth_token_secret is not None:
            self.oauth_token_secret = new_oauth_token_secret
    
    # snippet from python-oauth2 module
    @staticmethod
    def generate_timestamp():
        """Get seconds since epoch (UTC)."""
        return int(time.time())
    @staticmethod
    def generate_nonce(length=8):
        """Generate pseudorandom number."""
        return ''.join([str(random.randint(0, 9)) for i in range(length)])
    @staticmethod
    def escape(s):
        """Escape a URL including any /."""
        return urllib.quote(s, safe='~')
    # end snippet

ACCESS_SERVER = "http://developer.messenger.yahooapis.com"
CONTENT_TYPE = "application/json;charset=utf-8"
OAUTH_SERVER = "https://api.login.yahoo.com/oauth/v2/get_token"
        
class YMSession:
    """Manage the life of yahoo messenger session"""

    def __init__(self, userid, password, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.last_sequence = 0
        self.part_token = None

        if not self.initPart(userid, password):
            raise Exception, "Unable to init PART token"
        self.initOAuth()

            
        self.contacts = None    
        
        #ready to logon...
            
        
    #convert user+password to PART token
    def initPart(self, userid, password):
        print ">initPart"
        uri = "https://login.yahoo.com/WSLogin/V1/get_auth_token?&login=%s&passwd=%s&oauth_consumer_key=%s" % (userid, password, self.consumer_key)
        try:
            o = urllib2.urlopen(uri)
            response = o.read()
            resp_split = response.split("=",1)
            if len(resp_split) == 2:
                self.part_token = resp_split[1].strip()
                return True
        except urllib2.HTTPError, e:
            self._handleHttpError(e)
        return False    
            
    #convert PART token to oauth access token
    def initOAuth(self, part_token=None):
        print ">initOauth"
        if part_token is not None:
            self.part_token = part_token
        self.oauth = SimpleOAuth(OAUTH_SERVER, self.consumer_key, self.consumer_secret, self.part_token)
        
    #init session
    def login(self, presence_state=0, presence_message=""):
        print ">login"
        uri = "%s/v1/session?notifyServerToken=%s" % (ACCESS_SERVER, 1)
        headers = self.oauth.getHeader()
        headers['Content-type'] = CONTENT_TYPE
        body = json.dumps({"presenceState": presence_state, "presenceMessage": presence_message})
        req = urllib2.Request(uri, body, headers)
        try:
            o = urllib2.urlopen(req)
            self.notify_token = o.headers['set-cookie'].split(";")[0].split("=")[1]
            resp = o.read()
            self.login_data = json.loads(resp)
            print "server:%s notifyserver:%s" % (self.login_data['server'], self.login_data['notifyServer'])
            self.session_expired_time = time.time() + 3600  #mark time when session will expire
            return True
        except urllib2.HTTPError, e:
            self._handleHttpError(e)
        return False
        
    def logout(self):
        print ">logout"
        uri = "http://%s/v1/session?sid=%s" % (self.login_data['server'], self.login_data['sessionId'])
        headers = self.oauth.getHeader()
        headers['Content-type'] = CONTENT_TYPE
        req = urllib2.Request(uri, None, headers)
        req.get_method = lambda: 'DELETE'
        try:
            o = urllib2.urlopen(req)
            return True
        except urllib2.HTTPError, e:
            self._handleHttpError(e)
        return False
    
    """
    Call before 60 minutes to keep session alive
    """
    def keepAlive(self):
        print ">keepalive"
        uri = "http://%s/v1/keepalive?sid=%s&notifyServerToken=%s" % (self.login_data['server'], self.login_data['sessionId'], 1)
        headers = self.oauth.getHeader()
        headers['Content-type'] = CONTENT_TYPE
        req = urllib2.Request(uri, None, headers)
        req.get_method = lambda: 'PUT'
        try:
            o = urllib2.urlopen(req)
            self.notify_token = o.headers['set-cookie'].split(";")[0].split("=")[1]
            print "Cookie:",o.headers['set-cookie']
            self.session_expired_time = time.time() + 3600 - 120 - 60  #mark time when session will expire, 120 is default idle time of main loop, 60 is safety guard
            return True
        except urllib2.HTTPError, e:
            self._handleHttpError(e)
        return False
    
    def sendKeepAliveIfRequired(self):
        if time.time() > self.session_expired_time:
            print "Keep alive required"
            return self.keepAlive()
    
    def sendMessage(self, send_to_yahooid, message):
        uri = "http://%s/v1/message/yahoo/%s?sid=%s" % (self.login_data['server'], send_to_yahooid, self.login_data['sessionId'])
        headers = self.oauth.getHeader()
        headers['Content-type'] = CONTENT_TYPE
        body = json.dumps({"message": message})
        req = urllib2.Request(uri, body, headers)
        try:
            o = urllib2.urlopen(req)
            return True
        except urllib2.HTTPError, e:
            self._handleHttpError(e)
        return False
    
    def fetchContactList(self):
        uri = "http://%s/v1/contacts?sid=%s&fields=%%2Bpresence&fields=%%2Bgroups" % (self.login_data['server'], self.login_data['sessionId'])
        headers = self.oauth.getHeader()
        req = urllib2.Request(uri, None, headers)
        try:
            o = urllib2.urlopen(req)
            resp = o.read()
            self.contacts = json.loads(resp)
            return True
        except urllib2.HTTPError, e:
            self._handleHttpError(e)
        return False

    
    def replyBuddyRequest(self, buddy_userid, accepted=True, message=""):
        print ">replyBuddyRequest"
        uri = "http://%s/v1/buddyrequest/yahoo/%s?sid=%s" % (self.login_data['server'], buddy_userid, self.login_data['sessionId'])
        headers = self.oauth.getHeader()
        headers['Content-type'] = CONTENT_TYPE
        body = json.dumps({"authReason": message.encode("utf-8")})
        req = urllib2.Request(uri, body, headers)
        if not accepted:
            req.get_method = lambda: 'DELETE'
        try:
            o = urllib2.urlopen(req)
            return True
        except urllib2.HTTPError, e:
            print e
            print uri
            self._handleHttpError(e)
        return False
    
    
    def pollNotification(self, sequence=None, count=10):
        if sequence is None:
            sequence = sef.last_sequence + 1
        uri = "http://%s/v1/notifications?sid=%s&seq=%s&count=%s" % (self.login_data['server'], self.login_data['sessionId'], sequence, count)
        headers = self.oauth.getHeader()
        req = urllib2.Request(uri, None, headers)
        try:
            o = urllib2.urlopen(req)
            buff = o.read()
            if len(buff) == 0:
                #idle
                return None
            else:
                resp = json.loads(buff)
                for response in resp['responses']:
                    delegateMethodSig = "on_%s_event" % response.keys()[0]
                    if hasattr(self, delegateMethodSig):
                        getattr(self, delegateMethodSig)(response.values()[0])
                last_notification = resp['responses'][-1]   #a key ()notification type) with value as a dict of key/vals
                self.last_sequence = last_notification.values()[0]['sequence']
                return resp
        except urllib2.HTTPError, e:
            self._handleHttpError(e)
    
    def cometNotification(self, primary_userid=None, sequence=None, count=10, idle=120):
        if primary_userid is None:
            primary_userid = self.login_data['primaryLoginId']
        if sequence is None:
            sequence = self.last_sequence + 1

        uri = "http://%s/v1/pushchannel/%s?sid=%s&seq=%s&count=%s&format=%s&idle=%s&rand=%s" % (self.login_data['notifyServer'], primary_userid, self.login_data['sessionId'], sequence, count, "json", idle, random.randint(0,99999))
        headers = self.oauth.getHeader()
        headers['Cookie'] = 'IM=%s' % self.notify_token
        req = urllib2.Request(uri, None, headers)
        try:
            o = urllib2.urlopen(req)
            buff = o.read()
            if len(buff) == 0:
                return None

            resp = json.loads(buff)
            for response in resp['responses']:
                delegateMethodSig = "on_%s_event" % response.keys()[0]
                if hasattr(self, delegateMethodSig):
                    getattr(self, delegateMethodSig)(response.values()[0])
                else:
                    print "No method %s found. The data is %s" % (delegateMethodSig, response)
            last_notification = resp['responses'][-1]   #a key ()notification type) with value as a dict of key/vals
            self.last_sequence = last_notification.values()[0]['sequence']
            return resp
        except urllib2.HTTPError, e:
            self._handleHttpError(e)

    def _handleHttpError(self, e):
        buff = e.read()
        if len(buff) > 0:
            try:
                data = json.loads(buff)
                print "Error HTTP %s, code: %s detail: %s description: %s" % (e.code, data['error']['code'], data['error']['detail'], data['error']['description'])
                if data['error']['code'] == 28:
                    self.login()
                elif e.code == 401:
                    # token might've expired
                    pass         
            except ValueError:
                print e, buff

        
class YMGoogleerBot(YMSession):
    def on_message_event(self, obj):
        #avoid infinite loop
        if obj['sender'] == self.login_data['primaryLoginId']:
            return
        if obj['msg'] == "dodysw:quit":
            self.shutdown = True
            return
        if obj['msg'] == "dodysw:friends":
            self.fetchContactList()
            print self.contacts
            return
        print "=======%s: %s" % (obj['sender'], obj['msg'])
        self.sendMessage(obj['sender'], "'%s'\n%s" % (self.autotranslate(obj['msg']), self.google(obj['msg'])))
        
    def on_buddyAuthorize_event(self, obj):
        print "=======%s has asked me as buddy" % (obj['sender'])
        self.replyBuddyRequest(obj['sender'], accepted=True, message="Welcome.")
        self.sendMessage(obj['sender'], "Thanks for adding me. Ask me anything and I will google it for you. For help, contact developer at dodysw@gmail.com.")
        
    def on_logOff_event(self, obj):
        print "=======%s logged off" % (obj['buddy'])

    def on_buddyInfo_event(self, obj):
        for buddy in obj['contact']:
            print "=======%s buddy info. Presence: %s msg: %s" % (buddy['sender'], buddy['presenceState'], buddy.get('presenceMessage', ''))    

    def on_buddyStatus_event(self, obj):
        print "=======%s status. Presence: %s msg: %s" % (obj['sender'], obj['presenceState'], obj.get('presenceMessage', ''))

    def on_disconnect_event(self, obj):
        """
        Reason code
        1 = Regen: This user session has been expired because of login elsewhere.
        2 = Idle: This user session has been expired because of idleness.
        3 = Queue Full: This user session has been expired because messages in the session notification queue are not fetched.
        4 = Self-initiated Logoff: When the user does an explicit logoff. 
        """
        print "=======Session disconnected, reason: %s" % obj['reason']
        #force relogin...
        self.login()
        
    def on_offlineMessage_event(self, obj):
        print "=======Offline messages"
        self.sendMessage(obj['sender'], "'%s'\n%s" % (self.autotranslate(obj['msg']), self.google(obj['msg'])))

        for m in obj['messages']:
            print "=======* %s: %s" % (m['message']['sender'], m['message']['msg'])

    def mainLoop(self):
       self.shutdown = False
       while not self.shutdown:
           print "Long running", self.last_sequence
           self.sendKeepAliveIfRequired()
           self.cometNotification()
       self.logout()
        
    @staticmethod
    def echo(query):
        return query
    @staticmethod    
    def google(query):
        o = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (urllib.urlencode({'q' : query.encode("utf-8")})))
        if o.code == 200:
            body = o.read()
            results = json.loads(body)['responseData']['results']
            if results:
                reply = "%s:%s\n%s" % (YMGoogleerBot.unescape(results[0]['titleNoFormatting']), YMGoogleerBot.unescape(results[0]['content']), results[0]['url'])
            else:
                reply = "No result for *%s*" % query
        else:
            reply = "Sorry, couldn't contact google search"
        print "Replied with:%s" % reply
        return reply
    @staticmethod
    def unescape(s):
        return reduce(lambda orig, repl: orig.replace(*repl), (("&lt;", "<"), ("&gt;", ">"), ("&#39;", "'"), ("&quot;", '"'), ("&amp;", "&"), ("<b>", ""), ("</b>", "")), s)
        
    @staticmethod
    def detectlanguage(query):
        o = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&%s' % (urllib.urlencode({'q' : query.encode("utf-8")})))
        if o.code == 200:
            body = o.read()
            langcode = json.loads(body)['responseData']['language']
            return langcode

    @staticmethod
    def autotranslate(query):
        langcode_from = self.detectlanguage(query)
        langcode_to = 'en'
        if langcode_from == 'en':
            langcode_to = 'id'
        o = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&%s&langpair=%s|%s' % (urllib.urlencode({'q' : query.encode("utf-8")}), langcode_from, langcode_to))
        if o.code == 200:
            body = o.read()
            resp = json.loads(body)
            if resp['responseData'] is None:
                translated_text = resp['responseDetails']
            else:    
                translated_text = resp['responseData']['translatedText']
            reply = translated_text
        print "Replied with:%s" % reply
        return reply

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print "How to run: gtym.py <yahoo_userid> <yahoo_password>"
        sys.exit()
    userid, password = sys.argv[1], sys.argv[2]
    googlerBot = YMGoogleerBot(userid, password)
    if googlerBot.login():
        googlerBot.mainLoop()