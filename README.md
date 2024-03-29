# Airbrite

Python bindings for the [Airbrite API](https://github.com/airbrite/airbrite-api).

## Installation

Add this line to your application's requirements file:

    airbrite>=0.2

Or install it yourself as:

    $ pip install airbrite

You can use a virtual environment to install it:

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r REQUIREMENTS

## Tests

To run the unit tests use:

    $ python setup.py test
    $ # ...or...
    $ nosetests tests/unittests

To run the integration tests (which use the network, and take longer than units):

    $ nosetests tests/integration

## Quickstart

Get a feeling of the bindings with a quick tour using the python repl:

    $ virtualenv quicktour
    $ source quicktour/bin/activate
    $ pip install -r REQUIREMENTS
    $ python setup.py install
    $ # ...
    $ python
    >>> import airbrite
    >>> products, paging = airbrite.Product.list(limit=5)
    >>> products
    [<Product (5272a4c833bb650600000060)>, <Product (5272a4ae9b29130400000202)>, <Product (5272a4ad2ca30b04000000cb)>, <Product (5272a4aa43e58b07000000b5)>, <Product (5272a4a84ab33f060000023d)>]
    >>> paging['total']
    207
    >>> shipping = airbrite.Shipment(shipping_address={
    ... "name": "Joe Doe",
    ... "phone": "555 0111",
    ... })
    >>> order = airbrite.Order()
    >>> order.add_item(products[0], quantity=3)
    >>> order.shipments.add(shipping)
    >>> order.save()
    >>> order._id
    >>> exit()
    $ # let's bring it back
    $ python
    >>> import airbrite
    >>> order = airbrite.Order.fetch(_id='5273b4089742b00800000052')
    >>> order.line_items
    [{u'sku': u'7bafb41d-aa48-4698-a42a-0a8dd6dea94c', u'updated_date': u'2013-11-01T13:52:10.671Z', u'updated': 1383313930, u'name': u'Test Product', u'price': 150, u'quantity': 3, u'metadata': {}}]
    >>> order.shipments
    [{u'updated_date': u'2013-11-01T14:42:34.295Z', u'updated': 1383316954, u'user_id': u'5237a347429acf0400000013', u'created': 1383316954, u'order_id': u'5273bdda7dabcd0800000054', u'created_date': u'2013-11-01T14:42:34.295Z', u'shipping_address': {u'phone': u'555 0111', u'name': u'Joe Doe'}, u'_id': u'5273bdda7dabcd0800000055', u'metadata': {}}]
    >>> exit()
    $ deactivate

*NOTE: IDs and data surely won't be the same for you.*

## Usage

### Getting Started

```python
import airbrite
airbrite.api.KEY = "my_secret_key"
```

By default, the `airbrite.api.KEY` will be the test API key.

### Products

#### Create

```python
product = airbrite.Product.create(sku="foo",
                                  price=12345,
                                  name="Foo",
                                  description="An awesome watch",
                                  metadata={...})
# or

product = airbrite.Product(sku="foo",
                           price=12345,
                           name="Foo",
                           description="An awesome watch",
                           metadata={...})
product.save()
```

#### Retrieve

```python
product = airbrite::Product.fetch(_id="foo")

# or

product = airbrite::Product(_id="foo")
product.refresh()
```

#### Update

```python
product = # ... obtain a product
product.name = "My Product"
product.save()
```

#### List

Accepts filters: `limit`, `offset`, `sort`, `order`, `since`, `until`.

```python
products, paging = airbrite.Product.list()
```

### Orders

#### Create

```python
order = airbrite.Order.create(...)

# or

order = airbrite.Order(...)
order.save()
```

#### Retrieve

```python
order = airbrite.Order.fetch(_id="foo")

# or

order = airbrite.Order(_id="foo")
order.refresh
```

#### Update

```python
order = # ... obtain a order
order.metadata = {...}
order.save()
```

#### List

Accepts filters: `limit`, `offset`, `sort`, `order`, `since`, `until`.

```python
orders, paging = airbrite.Order.list()
```

### Payments

Currently, only `charge` payments are supported, at Order creation time.

#### List payments in an order

```python
order = # ... obtain an order
for payment in order.payments:
    # do something with payment
```

#### Add a payment at Order creation

```python
order = # ... obtain an order
payment = airbrite.Payment(amount=amount, card_token=token)
order.payments.add(payment)
order.save()
```

### Shipments

#### Add shipment to an order

```python
order = # ...obtain an order
shipment = airbrite.Shipment(courier='some courier')
order.shipments.add(shipment)
order.save()
```

#### List shipments in an order

```python
order = # ... obtain an order
for shipment in order.shipments:
    # do something with payment
```

#### Remove shipment from an order

```python
order.shipments.remove(old_shipment)
```

### Customers

Can hold name, email and address data.

#### Create

```python
customer = airbrite.Customer.create(...)

# or

customer = airbrite.Customer(...)
customer.save()
```

#### Retrieve

```python
customer = airbrite.Customer.fetch(_id="foo")

# or

customer = airbrite.Customer(_id="foo")
customer.refresh
```

#### Update

```python
customer = # ... obtain a customer
customer.name = 'New Name'
customer.save()
```

### Helpers

#### Persisted?

You can find out if an entity is persisted using the `is_persisted` property, e.g. `order.is_persisted`.

#### Refresh

Calling `refresh` on any "fetchable" entity causes it to fetch itself and replace its contents with the response data from Airbrite. Note that any local changes will be lost. The `_id` (and `order_id` in the case of payments and shipments)property must be set in order to refresh properly.
