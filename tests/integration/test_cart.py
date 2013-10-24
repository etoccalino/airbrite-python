import unittest
import uuid
import airbrite


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

        # Add customer data to the order

        # Add payment data

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

        # Add customer data to the order

        # Add payment data

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
