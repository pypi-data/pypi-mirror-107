from exceptionalpy import BaseNotifier, Handler

try:
    import requests
except ImportError:
    print("requests is not installed")
    print("pip3 install requests")
    requests = None


class HTTPNotifier(BaseNotifier):
    def __init__(self, url: str, method: str, auth: tuple = None, verify_ssl: bool = True):
        self.url = url
        self.method = method
        self.auth = auth
        self.verify_ssl = verify_ssl

    def send(self, data: dict):
        if requests is None:
            return False

        requests.request(self.method, self.url, json=data, auth=self.auth, verify=self.verify_ssl)


class HTTPHandler(Handler):
    def __init__(self, url: str, method: str, auth: tuple = None, verify_ssl: bool = True, init: bool = True):
        Handler.__init__(self, init)
        self._notifier = HTTPNotifier(url, method, auth, verify_ssl)


class HTTPGetHandler(HTTPHandler):
    def __init__(self, url: str, auth: tuple = None, verify_ssl: bool = True, init: bool = True):
        HTTPHandler.__init__(self, url, 'GET', auth, verify_ssl, init)


class HTTPPostHandler(HTTPHandler):
    def __init__(self, url: str, auth: tuple = None, verify_ssl: bool = True, init: bool = True):
        HTTPHandler.__init__(self, url, 'POST', auth, verify_ssl, init)
