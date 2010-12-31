Splunky
=======

splunky is a stupid simple library for running queries against the Splunk API.
It does not need the splunk SDK installed.

API Usage
---------

    import splunky
    p=splunky.Server(host=host, username=username, password=pw)

    for r in p.search_sync('hoursago=1 error'):
        print r['_raw']


CLI Usage
---------

    splunky-search 'hoursago=48 SPANTREE' -s splunk.example.com
