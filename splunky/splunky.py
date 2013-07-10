import lxml.etree as et
import requests
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

        self.s = requests.session()
        self.s.auth = (username, password)
        self.s.verify = False

    def makeurl(self, endpoint):
        url = "https://%s:%s/services/%s" % (self.host, self.port, endpoint)
        return url

    def post_xml(self, endpoint, data):
        url = self.makeurl(endpoint)
        d = self.s.post(url, data=data)
        return et.fromstring(str(d.text))

    def get_json(self, endpoint, data):
        data['output_mode'] = 'json'
        url = self.makeurl(endpoint)
        d = self.s.get(url, params=data)
        if not d.text:
            return None
        return json.loads(str(d.text))

    def get_xml(self, endpoint, data=None):
        url = self.makeurl(endpoint)
        d = self.s.get(url, params=data)
        return et.fromstring(str(d.text))

    def search(self, q, **kwargs):
        data={'search': 'search ' + q}
        data.update(kwargs)
        data = self.post_xml("search/jobs", data)
        return data.findtext("sid")

    def results(self, sid, **kwargs):
        results = self.get_json("search/jobs/%s/events" % sid, kwargs)
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

    def search_sync(self, q, **kwargs):
        data={'search': 'search ' + q}
        data.update(kwargs)
        return self.get_json("search/jobs/export", data)
