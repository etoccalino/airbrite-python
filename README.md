# Airbrite

Python bindings for the [Airbrite API](https://github.com/airbrite/airbrite-api).

## Installation

Add this line to your application's requirements file:

    airbrite>=0.2

Or install it yourself as:

    $ pip install airbrite

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
```

# or

```python
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
```

# or

```python
product = airbrite::Product(_id="foo")
product.refresh()
```

#### Update

```python
product = # ... obtain a product
product.name = "Pebble V9"
product.save()
```

#### List

Accepts Filters.

```python
products, paging = airbrite.Product.list()
```

### Orders

#### Create

```python
order = airbrite.Order.create(...)
```

# or

```python
order = airbrite.Order(...)
order.save()
```

#### Retrieve

```python
order = airbrite.Order.fetch(_id="foo")
```

# or

```python
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

Accepts Filters.

```python
orders, paging = airbrite.Order.list()
```


################################ <<< >>> ######################################


### Payments

#### Create

```python
params = {:order_id => "o_id", ...}
payment = airbrite.Payment.create params

# or

payment = airbrite.Payment.new params
payment.save
```

#### Retrieve

```python
payment = airbrite.Payment.fetch :order_id => "o_id", :_id => "foo"

# or

payment = airbrite.Payment.new :order_id => "o_id", :_id => "foo"
payment.refresh
```

#### Update

```python
payment = # ... obtain a payment
payment.metadata = {...}
payment.save
```

#### List

Accepts Filters.

```python
result = airbrite.Payment.list :order_id => "o_id"
payments = result.data
paging = result.paging
```

#### Charge

```python
payment = # ... obtain a payment
payment.charge
```

#### Authorize

```python
payment = # ... obtain a payment
payment.authorize
```

#### Capture

```python
payment = # ... obtain a payment
payment.capture
```

#### Refund

```python
payment = # ... obtain a payment
payment.refund amount
```

### Shipments

#### Create

```python
params = {:order_id => "o_id", ...}
shipment = airbrite.Shipment.create params

# or

shipment = airbrite.Shipment.new params
shipment.save
```

#### Retrieve

```python
shipment = airbrite.Shipment.fetch :order_id => "o_id", :_id => "foo"

# or

shipment = airbrite.Shipment.new :order_id => "o_id", :_id => "foo"
shipment.refresh
```

#### Update

```python
shipment = # ... obtain a shipment
shipment.metadata = {...}
shipment.save
```

#### List

Accepts Filters.

```python
result = airbrite.Shipment.list :order_id => "o_id"
shipments = result.data
paging = result.paging
```

### Customers

#### Create

```python
params = {...}
customer = airbrite.Customer.create params

# or

customer = airbrite.Customer.new params
customer.save
```

#### Retrieve

```python
customer = airbrite.Customer.fetch :_id => "foo"

# or

customer = airbrite.Customer.new :_id => "foo"
customer.refresh
```

#### Update

```python
customer = # ... obtain a customer
customer.metadata = {...}
customer.save
```

#### List

Accepts Filters.

```python
result = airbrite.Customer.list
customers = result.data
paging = result.paging
```

### Tax

#### Calculate

```python
tax = airbrite.Tax.calculate :zip => "94301", :amount => 12345, :nexus_zips => "12345,67890"
```

### Account

#### Retrieve

```python
account = airbrite.Account.fetch
```

### Event

#### Retrieve

```python
event = airbrite.Event.fetch :_id => "foo"

# or

event = airbrite.Event.new :_id => "foo"
event.refresh
```

#### List

Accepts Filters.

```python
result = airbrite.Event.list
events = result.data
paging = result.paging
```

### Filters

All list operations accept filters.  These are:

```python
[:limit, :skip, :sort, :order, :since, :until]
```

They work like so:

```python
events = airbrite.Event.list(
  :limit => 50,
  :skip => 20,
  :sort => :created,
  :order => 1,
  :since => 24.hours.ago,
  :until => 12.hours.ago
)
```

Anything you pass to `[:limit, :skip, :since, :until]` should play nicely with `to_i` (Time objects do). Anything passed to `:sort` should play nicely with `to_s` (symbols do).

You can mix and match them as you please.

### Helpers

#### Persisted?

You can find out if an entity is persisted by asking it, e.g., `order.persisted?`.

#### Refresh

Calling `refresh` on any "fetchable" entity causes it to fetch itself and replace its contents with the response data from Airbrite. Note that any local changes will be lost. The `_id` property must be set in order to refresh properly.

### Errors

There are 4 exception types that can be raised from all API operations described above.  These are:

```python
# Missing api key:
airbrite.MissingApiKey

# 50* http status codes returned from Airbrite:
airbrite.ApiError

# 40* http status codes returned from Airbrite:
airbrite.BadRequestError

# Misc. HTTP client errors such as timeouts and response parse failures:
airbrite.ClientError
```

All exceptions above inherit from `airbrite.AirbriteError` and best attempts are made to record useful messages.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
