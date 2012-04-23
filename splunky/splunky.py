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

        self.s = requests.session(auth=(username,password),verify=False)

    def makeurl(self, endpoint):
        url = "https://%s:%s/services/%s" % (self.host, self.port, endpoint)
        return url

    def post_xml(self, endpoint, data):
        url = self.makeurl(endpoint)
        d = self.s.post(url, data=data)
        return et.fromstring(d.raw.read())

    def get_json(self, endpoint, data):
        data['output_mode'] = 'json'
        url = self.makeurl(endpoint)
        d = self.s.get(url, params=data)
        t = d.raw.read()
        if not t:
            return None
        return json.loads(t)

    def get_xml(self, endpoint, data=None):
        url = self.makeurl(endpoint)
        d = self.s.get(url, params=data)
        return et.fromstring(d.raw.read())

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

    def search_sync(self, q, check_interval=0.2, **kwargs):
        sid = self.search(q, **kwargs)
        done = False
        while not done:
            s = self.status(sid)
            done = int(s['isDone'])
            time.sleep(check_interval)
        return self.results(sid, **kwargs)
