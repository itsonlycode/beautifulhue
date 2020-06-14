import json
import urllib
import urllib.request
import urllib.parse


class Request:

    def _request(self, url, data, action, content_type):

        if ((data or isinstance(data, dict)) and
                action not in ('GET', 'DELETE',)):
            data = json.dumps(data)
            if action == 'PUT':
                opener = urllib.request.build_opener(
                    urllib.request.HTTPHandler)
                # Python3.x's urrlib.request requires a byte encoding
                # for all messages sent through HTTP Requests
                data = data.encode('utf-8')
                req = urllib.request.Request(url, data=data)
                req.add_header('Content-Type', content_type)
                req.get_method = lambda: 'PUT'
                conn = opener.open(req)
            else:
                headers = {'Content-Type': content_type}
                try:
                    req = urllib.request.Request(url, data, headers)
                    conn = urllib.request.urlopen(req)
                except TypeError:
                    # This is for the _lights.find bodyless POST.
                    data = urllib.parse.encode(json.loads(data))
                    data = data.encode('ascii')
                    req = urllib.request.Request(url, data, headers)
                    conn = urllib.request.urlopen(req)
        elif action == 'DELETE':
            opener = urllib.request.build_opener(urllib.request.HTTPHandler)
            req = urllib.request.Request(url)
            req.get_method = lambda: 'DELETE'
            conn = opener.open(req)
        else:
            req = urllib.request.Request(url)
            conn = urllib.request.urlopen(req)
        response = conn.read()
        conn.close()
        try:
            content = json.loads(response)
        except Exception:
            content = response
        # Python 3.x's urllib.request loads HTTP Messages as bytes
        # so first we have to decode the message into a UTF-8 string
        # then convert it into a dictionary using json.loads
        return conn.info().items(), content

    def get(self, url, data=None, content_type='application/json'):
        return self._request(url, data, 'GET', content_type)

    def post(self, url, data={}, content_type='application/json'):
        return self._request(url, data, 'POST', content_type)

    def put(self, url, data={}, content_type='application/json'):
        return self._request(url, data, 'PUT', content_type)

    def delete(self, url, data=None, content_type='application/json'):
        return self._request(url, data, 'DELETE', content_type)
