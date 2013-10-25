import requests
import json
import api

import logging
logger = logging.getLogger('airbrite.client')


class Client(object):

    headers = {
        'Content-Type': 'application/json'
    }

    @property
    def api_key(self):
        return api.KEY

    @property
    def endpoint(self):
        return api.END_POINT

    @property
    def auth(self):
        return (api.KEY, api.KEY_PASSWORD)

    def meth(self, method, url, **params):
        logger.debug('calling %s on %s with %s' % (method, url, params))
        req = getattr(requests, method)(url, auth=self.auth,
                                        headers=self.headers,
                                        **params)
        if req.status_code != 200:
            logger.warning('%s() call failed with status code %s, response: %s'
                           % (method, req.status_code, req.json()))
            raise Exception('Bad get parameters: %s' % params)
        return req.json()

    def get(self, url, **params):
        return self.meth('get', url, params=params)

    def post(self, url, **params):
        return self.meth('post', url, data=json.dumps(params))

    def put(self, url, **params):
        return self.meth('put', url, data=json.dumps(params))
