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

    $ python setup.py install
    $ # ...
    $ python
    >>> import airbrite
    >>> products, paging = airbrite.Product.list(limit=5)
    >>> products
        [<Product (5272a4c833bb650600000060)>, <Product (5272a4ae9b29130400000202)>, <Product (5272a4ad2ca30b04000000cb)>, <Product (5272a4aa43e58b07000000b5)>, <Product (5272a4a84ab33f060000023d)>]
    >>> paging['total']
    207
    >>>

*NOTE: IDs and numbers surely won't be the same for you. That's not a problem.*

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
