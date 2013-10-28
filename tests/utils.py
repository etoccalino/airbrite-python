"""
A client implements get, put, post and
"""
import copy
from airbrite import Product, Order, Shipment, Customer


class TestClient(object):

    CANNED = {
        Product: [{
            u'_id': u'5237a50459459f0500000007',
            u'created': 1379378436,
            u'created_date': u'2013-09-17T00:40:36.649Z',
            u'description': u'My First Product',
            u'inventory': None,
            u'metadata': {},
            u'name': None,
            u'sku': u'first-product',
            u'updated': 1379378436,
            u'updated_date': u'2013-09-17T00:40:36.649Z',
            u'user_id': u'5237a347429acf0400000013',
            u'weight': None
        }, {
            u'_id': u'5237a50459459f0500000008',
            u'created': 1379378436,
            u'created_date': u'2013-09-17T00:40:36.649Z',
            u'description': u'My Second Product',
            u'inventory': None,
            u'metadata': {},
            u'name': None,
            u'sku': u'second-product',
            u'updated': 1379378436,
            u'updated_date': u'2013-09-17T00:40:36.649Z',
            u'user_id': u'5237a347429acf0400000013',
            u'weight': None
        }],
        Order: [{
            "_id": "524c5b87d1f275040000019e",
            "created": 1380735879,
            "created_date": "2013-10-02T17:44:39.708Z",
            "currency": "usd",
            "customer_id": None,
            "description": None,
            "discount": {},
            "line_items": [
                {
                    "description": "My First Product",
                    "inventory": None,
                    "metadata": {},
                    "name": None,
                    "quantity": 1,
                    "sku": "first-product",
                    "updated": 1379378436,
                    "updated_date": "2013-09-17T00:40:36.649Z",
                    "weight": None
                }
            ],
            "metadata": {},
            "order_number": 3441,
            "shipping": {},
            "shipping_address": None,
            "status": None,
            "tax": {},
            "updated": 1380735879,
            "updated_date": "2013-10-02T17:44:39.708Z",
            "user_id": "5237a347429acf0400000013"
        }, {
            "_id": "524c5b896b19e60600000122",
            "created": 1380735881,
            "created_date": "2013-10-02T17:44:41.662Z",
            "currency": "usd",
            "customer_id": None,
            "description": None,
            "discount": {},
            "line_items": [
                {
                    "description": "My First Product",
                    "inventory": None,
                    "metadata": {},
                    "name": None,
                    "quantity": 1,
                    "sku": "first-product",
                    "updated": 1379378436,
                    "updated_date": "2013-09-17T00:40:36.649Z",
                    "weight": None
                }
            ],
            "metadata": {},
            "order_number": 3442,
            "shipping": {},
            "shipping_address": None,
            "status": None,
            "tax": {},
            "updated": 1380735881,
            "updated_date": "2013-10-02T17:44:41.663Z",
            "user_id": "5237a347429acf0400000013"
        }],
        Shipment: [{
            "_id": "52696f72291468040000003e",
            "created": 1382641522,
            "created_date": "2013-10-24T19:05:22.134Z",
            "metadata": {},
            "order_id": "524c5b896b19e60600000122",
            "shipping_address": None,
            "updated": 1382641522,
            "updated_date": "2013-10-24T19:05:22.134Z",
            "user_id": "5237a347429acf0400000013"
        }, {
            "_id": "52696fa4ba015806000000bc",
            "created": 1382641572,
            "created_date": "2013-10-24T19:06:12.571Z",
            "metadata": {},
            "order_id": "524c5b896b19e60600000122",
            "shipping_address": None,
            "updated": 1382641572,
            "updated_date": "2013-10-24T19:06:12.571Z",
            "user_id": "5237a347429acf0400000013"
        }],
        Customer: [{
            "_id": "52696f72291468040000003e",
            "user_id": "5237a347429acf0400000013",
            "created": 1382641522,
            "created_date": "2013-10-24T19:05:22.134Z",
            "updated": 1382641522,
            "updated_date": "2013-10-24T19:05:22.134Z",
            "metadata": {},
            "name": "test customer 1",
            "email": "no@addr.com",
        }, {
            "_id": "52696f72291468040000003f",
            "user_id": "5237a347429acf0400000014",
            "created": 1382641522,
            "created_date": "2013-10-24T19:05:22.134Z",
            "updated": 1382641522,
            "updated_date": "2013-10-24T19:05:22.134Z",
            "metadata": {},
            "name": "test customer 2",
            "email": "no@addr.com",
        }]
    }

    def __init__(self, hint):
        """The hint helps the test client decide what to return.

        Should be one of the airbrite exposed entities.
        """
        self.hint = hint

        # Cache calls to the server
        self._posted = []
        self._put = []

    def clear_posted(self):
        self._posted = []

    def clear_put(self):
        self._put = []

    def clear(self):
        self.clear_put()
        self.clear_posted()

    def get(self, url, **data):
        # Linsting the products
        if url == self.hint.collection_url(**data):
            return {
                'data': self.CANNED[self.hint],
                'paging': {
                    'count': 2,
                    'has_more': False,
                    'limit': 100,
                    'total': 2,
                },
                'meta': {}
            }
        # If a particular product is requested, return it
        if '_id' in data:
            for product in self.CANNED[self.hint]:
                if product['_id']:
                    return {'data': product}
            raise Exception('unknown _id')
        # If any product is acceptable, return any
        result_data = self.CANNED[self.hint][0]
        return {'data': copy.deepcopy(result_data)}

    def post(self, url, **data):
        # Prepare a version of the data that is acceptable to return
        posted_data = copy.deepcopy(data)
        posted_data['_id'] = self.hint.__name__.lower() + '_test_id'
        # Keep a copy for consultancy
        self._posted.append(posted_data)
        return {'data': posted_data}

    def put(self, url, **data):
        # Prepare a version of the data that is acceptable to return
        put_data = copy.deepcopy(data)
        # Keep a copy for consultancy
        self._put.append(put_data)
        return {'data': put_data}
