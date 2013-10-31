import unittest
import uuid
import airbrite


def get_card_token():
    """Return a card token using test Stripe API key and test card data"""
    import stripe
    stripe.api_key = 'sk_test_mkGsLqEW6SLnZa487HYfJVLf'
    card = {
        'number': '4242424242424242',
        'exp_month': 12,
        'exp_year': 2014,
        'cvc': '123'
    }
    return stripe.Token.create(card=card).id


class CartTestCase (unittest.TestCase):
    "Test a workflow akin to that of a shopping cart"

    def test_simple_cart(self):
        DATA = {
            'products': [{
                'name': 'Product One',
                'sku': str(uuid.uuid4()),
                'price': 50,
            }, {
                'name': 'Product Two',
                'sku': str(uuid.uuid4()),
                'price': 100,
            }]
        }

        # Create the products
        product1_data = DATA['products'][0]
        product2_data = DATA['products'][1]
        product1 = airbrite.Product.create(**product1_data)
        product2 = airbrite.Product.create(**product2_data)
        self.assertIsNotNone(product1._id)
        self.assertIsNotNone(product2._id)

        # Create an order, WITHOUT saving it to the backend
        order = airbrite.Order()

        # Add 2 of product1, and 1 of product2
        order.add_item(product1, 2)
        self.assertEqual(len(order.line_items), 1)
        order.add_item(product2, 1)
        self.assertEqual(len(order.line_items), 2)

        # Create the order in the backend
        order.save()
        self.assertIsNotNone(order._id)

        # Fetch it back, and see the products in the order
        _id = order._id
        del order
        order = airbrite.Order.fetch(_id=_id)
        self.assertEqual(len(order.line_items), 2)
        SKUs = [p['sku'] for p in order.line_items]
        self.assertTrue(product1.sku in SKUs)
        self.assertTrue(product2.sku in SKUs)

    def test_shipment_cart(self):
        DATA = {
            'products': [{
                'name': 'Product One',
                'sku': str(uuid.uuid4()),
                'price': 50,
            }, {
                'name': 'Product Two',
                'sku': str(uuid.uuid4()),
                'price': 100,
            }]
        }

        # Create the products
        product1_data = DATA['products'][0]
        product2_data = DATA['products'][1]
        product1 = airbrite.Product.create(**product1_data)
        product2 = airbrite.Product.create(**product2_data)
        self.assertIsNotNone(product1._id)
        self.assertIsNotNone(product2._id)

        # Create an order, WITHOUT saving it to the backend
        order = airbrite.Order()

        # Add 2 of product1, and 1 of product2
        order.add_item(product1, 2)
        self.assertEqual(len(order.line_items), 1)
        order.add_item(product2, 1)
        self.assertEqual(len(order.line_items), 2)

        # Add shipment data to the order
        shipment = airbrite.Shipment(metadata={'note': 'stubbed shipment'})
        order.shipments.add(shipment)

        # Create the order in the backend
        order.save()
        self.assertIsNotNone(order._id)

        # Fetch it back, and see the products in the order
        _id = order._id
        del order
        order = airbrite.Order.fetch(_id=_id)

        self.assertEqual(len(order.line_items), 2)
        SKUs = [p['sku'] for p in order.line_items]
        self.assertTrue(product1.sku in SKUs)
        self.assertTrue(product2.sku in SKUs)

        self.assertEqual(len(order.shipments), 1)

    def test_payment_cart(self):
        product_data = {
            'name': 'Product One',
            'sku': str(uuid.uuid4()),
            'price': 50,
        }
        amount = 995
        card_token = get_card_token()

        # Create the products
        product = airbrite.Product.create(**product_data)
        self.assertIsNotNone(product._id)

        # Create an order, WITHOUT saving it to the backend
        order = airbrite.Order()

        # Add a product
        order.add_item(product, 2)
        self.assertEqual(len(order.line_items), 1)

        # Add payment data
        payment = airbrite.Payment(amount=amount, card_token=card_token)
        order.payments.add(payment)

        order.save()

        # Fetch it back, and see the products in the order
        _id = order._id
        del order
        order = airbrite.Order.fetch(_id=_id)

        # Check that the product order is good
        self.assertEqual(len(order.line_items), 1)
        self.assertEqual(product.sku, order.line_items[0]['sku'])

        # Check the payment data
        self.assertEqual(len(order.payments), 1)
        self.assertEqual(order.payments[0].amount, amount)

    def test_customer_cart(self):
        DATA = {
            'product': {
                'name': 'Product One',
                'sku': str(uuid.uuid4()),
                'price': 50,
            },
            'customer': {
                'name': 'Joe Doe',
                'email': 'no@addr.com',
            }
        }

        # Create a product
        product = airbrite.Product.create(**DATA['product'])
        self.assertIsNotNone(product._id)

        # Create an order, WITHOUT saving it to the backend
        order = airbrite.Order()

        # Add 2 of product, and 1 of product2
        order.add_item(product, 2)
        self.assertEqual(len(order.line_items), 1)

        # Create the customer and associate with order
        customer = airbrite.Customer.create(**DATA['customer'])
        self.assertIsNotNone(customer._id)
        order.customer_id = customer._id

        # Create the order in the backend
        order.save()
        self.assertIsNotNone(order._id)
        self.assertEqual(order.customer_id, customer._id)

        # Fetch it back, and see the products in the order
        _id = order._id
        del order
        order = airbrite.Order.fetch(_id=_id)

        # Check that the product order is good
        self.assertEqual(len(order.line_items), 1)
        self.assertEqual(product.sku, order.line_items[0]['sku'])

        self.assertEqual(len(order.line_items), 1)
        SKUs = [p['sku'] for p in order.line_items]
        self.assertTrue(product.sku in SKUs)

        self.assertEqual(order.customer_id, customer._id)
