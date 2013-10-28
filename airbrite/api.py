# TODO: define a manager to handle paging for the resources.

from datetime import datetime
from copy import copy
import logging
import calendar


END_POINT = 'https://api.airbrite.io/v2'
_TEST_API_KEY = 'sk_test_a805be8b2add854f09976b3b5c0f5bd06c14617c'

# Initialize to the test API key and password
KEY = _TEST_API_KEY
KEY_PASSWORD = ''

import client


###############################################################################

class APIAttribute (object):
    """Manage the instance internal _data attribute"""

    def __init__(self, attribute_api_name, default=None):
        self.default = default
        self.name = attribute_api_name

    def __get__(self, instance, owner):
        if self.name not in instance._data:
            instance._data[self.name] = copy(self.default)
        return instance._data[self.name]

    def __set__(self, instance, value):
        if self.name not in instance._data:
            raise AttributeError('%s has no API attribute "%s"'
                                 % (instance, self.name))
        instance._data[self.name] = value


class DateAPIAttribute (APIAttribute):
    # TODO fix datetime and ISO conversions to match exacly

    def __get__(self, instance, owner):
        """Returns a datetime object."""
        timestamp = super(DateAPIAttribute, self).__get__(instance, owner)
        # Transform the timestamp to a datetime object
        return datetime.fromtimestamp(timestamp)

    def __set__(self, instance, value):
        # Transform the datetime object to a timestamp
        timestamp = calendar.timegm(value.utctimetuple())
        super(DateAPIAttribute, self).__set__(instance, timestamp)

        # Update the corresponding API attribute for *_date (ISO 8601), if any
        _date_name = self.name + '_date'
        if _date_name in instance._data:
            iso_date = value.isoformat()
            instance._data[_date_name] = iso_date


###############################################################################

class EntityCollection (list):
    """Proxy to an underlying list and transform entities on the fly"""

    def __init__(self, entity, values=[]):
        self.entity = entity
        self.reset(values)

    def reset(self, values):
        """Takes a list of entities to set the proxied collection"""
        # Ensure it receives a list object
        if type(values) is not list:
            raise TypeError('must receive a list object')

        # Ensure each object in the list is-a entity
        if values and type(values[0]) is not dict:
            raise TypeError('must receive a list of dict objects')

        self.collection = values

    def add(self, entity):
        if not isinstance(entity, self.entity):
            raise TypeError('must receive a %s object' % self.entity)
        self.collection.append(entity.to_dict())

    def remove(self, entity):
        if not isinstance(entity, self.entity):
            raise TypeError('must receive a %s object' % self.entity)
        if not entity._id:
            raise ValueError('%s object does not have an _id' % self.entity)
        self.collection.remove(entity.to_dict())

    def __len__(self):
        return len(self.collection)

    def __getitem__(self, index):
        return self.entity(**self.collection.__getitem__(index))

    def __setitem__(self, index, value):
        if not isinstance(value, self.entity):
            raise TypeError('must receive a %s object' % self.entity)
        self.collection[index] = value.to_dict()

    def __delitem__(self, index):
        self.collection.__delitem__(index)

    def __iter__(self):
        for datum in self.collection:
            yield self.entity(**datum)
        raise StopIteration()


class APICollectionAttribute (object):
    """Describe a Entity objects collection backed by airbrite"""

    def __init__(self, name, entity):
        self.name = name
        self.entity = entity

    def __get__(self, instance, owner):
        if self.name not in instance._data:
            instance._data[self.name] = []
        return EntityCollection(self.entity, instance._data[self.name])

    def __set__(self, instance, values):
        if isinstance(values, EntityCollection):
            # Reset the values to those proxied by the collection
            instance._data[self.name] = values.collection
        else:

            if isinstance(values, list):
                # If pass a list of objects, get the list of data dicts
                if values and isinstance(values[0], self.entity):
                    values = [v.to_dict() for v in values]

                # Set the list of values
                instance._data[self.name] = values

            # In any other case, error out
            else:
                raise TypeError('must receive a list of %s'
                                ' or a EntityCollection' % self.entity)

###############################################################################


class Entity (object):
    """Base class for airbrite objects"""

    _id = APIAttribute('_id')
    user_id = APIAttribute('user_id')
    created = DateAPIAttribute('created')
    updated = DateAPIAttribute('updated')
    description = APIAttribute('description')
    metadata = APIAttribute('metadata', default={})

    client = client.Client()
    class_url = ''

    logger = logging.getLogger('airbrite.entities')

    def instance_url(self):
        if not self._id:
            raise Exception('must have _id to have a URL')
        return "%s/%s" % (self.collection_url(), self._id)

    @classmethod
    def collection_url(cls, **kwargs):
        return "%s/%s" % (END_POINT, cls.class_url)

    def __init__(self, **kwargs):
        self.replace(kwargs)

    def replace(self, data={}):
        self._data = data

    def to_dict(self):
        return self._data

    def __eq__(self, other):
        if self._id and hasattr(other, '_id'):
            return self._id == other._id
        return False

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return repr(self.to_dict())


class Fetchable (object):
    """Mixin to get `fetch` and `refresh` functionality"""

    @classmethod
    def fetch(cls, **kwargs):
        instance = cls(**kwargs)
        instance.refresh()
        return instance

    def refresh(self):
        if not self.is_persisted:
            raise Exception('refreshing non-saved airbrite entity')
        data = self.client.get(self.instance_url())
        self.replace(data['data'])


class Listable (object):
    """Mixin to get `list`"""

    FILTERS = [('limit', int), ('offset', int), ('sort', str),
               ('order', str), ('since', int), ('until', int)]

    @classmethod
    def _filters(cls, **kwargs):
        try:
            filters = dict(((_f, _t(kwargs[_f]))
                            for (_f, _t) in cls.FILTERS if _f in kwargs))
        except ValueError:
            raise Exception('bad value for filters')
        return filters

    @classmethod
    def list(cls, **kwargs):
        req = cls.client.get(cls.collection_url(**kwargs),
                             **cls._filters(**kwargs))
        cls.logger.debug('list() got from backend: %s' % req['data'])
        results = [cls(**data) for data in req['data']]
        paging = req['paging']
        return results, paging


class Persistable (object):
    """Mixin to get `create`, `save` and `is_persisted` functionality"""

    @classmethod
    def create(cls, **kwargs):
        data = cls.client.post(cls.collection_url(**kwargs), **kwargs)
        cls.logger.debug('create() got from backend: %s' % data)
        return cls(**data['data'])

    def save(self, **kwargs):
        if not self.is_persisted:
            data = self.client.post(self.collection_url(**kwargs),
                                    **self.to_dict())
        else:
            data = self.client.put(self.instance_url(), **self.to_dict())
        self.logger.debug('save() from backend: %s' % data)
        self.replace(data['data'])

    @property
    def is_persisted(self):
        return self._id and not self._id == ''


###############################################################################

class Product (Fetchable, Listable, Persistable, Entity):

    class_url = 'products'

    name = APIAttribute('name')
    sku = APIAttribute('sku')
    price = APIAttribute('price', default=None)

    def __repr__(self):
        return "<Product (%s)>" % str(getattr(self, '_id', '?'))


class Shipment (Fetchable, Listable, Persistable, Entity):

    order_id = APIAttribute('order_id')
    courier = APIAttribute('courier', default='')
    shipping_address = APIAttribute('shipping_address', default={})
    tracking = APIAttribute('tracking')
    method = APIAttribute('method')
    status = APIAttribute('status')

    class_url = 'orders/%(order_id)s/shipments'

    @classmethod
    def collection_url(cls, order_id=order_id, **kwargs):
        relative_url = cls.class_url % {'order_id': order_id}
        return "%s/%s" % (END_POINT, relative_url)

    def instance_url(self):
        if not self._id:
            raise Exception('must have _id to have a URL')
        if not self.order_id:
            raise Exception('must have order_id to have a URL')
        return "%s/%s" % (self.collection_url(order_id=self.order_id),
                          self._id)

    @classmethod
    def create(cls, **kwargs):
        order_id = kwargs.get('order_id', None)
        if not order_id:
            raise Exception('need an order_id to create a shipment')
        return super(Shipment, cls).create(**kwargs)

    def save(self):
        if not self.order_id:
            raise Exception('saving a shipment requires a valid order_id')
        super(Shipment, self).save(order_id=self.order_id)

    @property
    def is_persisted(self):
        if self.order_id:
            return super(Shipment, self).is_persisted
        return False


class Customer (Fetchable, Listable, Persistable, Entity):

    user_id = APIAttribute('user_id')
    name = APIAttribute('name')
    email = APIAttribute('email')
    address = APIAttribute('address', default={})
    addresses = APIAttribute('addresses', default=[])

    # Contains name, line1, line2, city, state, zip, country, phone
    default_address = APIAttribute('default_address', default={})

    card_token = APIAttribute('card_token')
    stripe = APIAttribute('strip')
    stripe_customer_id = APIAttribute('stripe_customer_id')
    match = APIAttribute('match')

    class_url = 'customers'


class Order (Fetchable, Listable, Persistable, Entity):

    customer_id = APIAttribute('customer_id')
    currency = APIAttribute('currency')  # 3-letter ISO currency code
    order_number = APIAttribute('order_number', default=-1)
    status = APIAttribute('status')

    # Contains sku, quantity
    line_items = APIAttribute('line_items', default=[])

    # Contains name, line1, line2, city, state, zip, country, phone
    # Country must by a 2-letter ISO country code
    shipping_address = APIAttribute('shipping_address', default={})

    # Contains cost (integer)
    discount = APIAttribute('discount', default={})

    # Contains cost (integer)
    shipping = APIAttribute('shipping', default={})

    # Contains cost (integer)
    tax = APIAttribute('tax', default={})

    # Optional shipments connection (object)
    # TODO: make this attribute a nested entity collection
    shipments = APICollectionAttribute('shipments', Shipment)

    class_url = 'orders'

    def __init__(self, **kwargs):
        shipments = kwargs.pop('shipments', [])
        super(Order, self).__init__(**kwargs)
        self.shipments = shipments

    def add_item(self, product, quantity=1):
        self.line_items.append({
            'sku': product.sku,
            'quantity': quantity,
        })

    def __repr__(self):
        return "<Order (%s)>" % str(getattr(self, '_id', '?'))
