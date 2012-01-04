import lxml.etree as et
import httplib2
import urllib
import time
try :
    import json
except ImportError:
    import simplejson as json

NS_MAP = {
 'atom': 'http://www.w3.org/2005/Atom',
 'splunk': 'http://dev.splunk.com/ns/rest'
}

class Server:
    def __init__(self, host, username, password, port=8089):
        self.host = host
        self.port = port

        self.h = httplib2.Http()
        self.h.add_credentials(username, password)

    def do(self, method, endpoint, data=None):
        d = data and urllib.urlencode(data) or ''
        url = "https://%s:%s/services/%s" % (self.host, self.port, endpoint)
        
        resp, content = self.h.request(url, method, body=d)
        return content

    def post_xml(self, endpoint, data):
        d = self.do('POST', endpoint, data)
        return et.fromstring(d)

    def get_json(self, endpoint, data):
        d = data and urllib.urlencode(data) or ''
        d = self.do('GET', endpoint + '?' + d)
        if not d:
            return None
        return json.loads(d)

    def get_xml(self, endpoint, data=None):
        d = data and urllib.urlencode(data) or ''
        d = self.do('GET', endpoint + '?' + d)
        return et.fromstring(d)

    def search(self, q, **kwargs):
        data={'search': 'search ' + q}
        data.update(kwargs)
        data = self.post_xml("search/jobs", data)
        return data.findtext("sid")

    def results(self, sid, **kwargs):
        d = {'output_mode': 'json'}
        d.update(kwargs)
        results = self.get_json("search/jobs/%s/events" % sid, d)
        if not results:
            results = []
        return results

    def status(self, sid):
        x =  self.get_xml("search/jobs/%s" % sid)
        r = {}
        for k in x.findall('{%(atom)s}content/{%(splunk)s}dict/{%(splunk)s}key' % NS_MAP):
            name = k.get("name")
            r[name] = k.text
        return r

    def search_sync(self, q, check_interval=0.2, **kwargs):
        sid = self.search(q, **kwargs)
        done = False
        while not done:
            s = self.status(sid)
            done = int(s['isDone'])
            time.sleep(check_interval)
        return self.results(sid, **kwargs)
