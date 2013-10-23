import unittest
import uuid

import airbrite.api
import airbrite.client


class ProductCRUDTestCase (unittest.TestCase):

    def test_backend_connection(self):
        """Tests the simplest call that should succeed"""
        self.c = airbrite.client.Client()
        result = self.c.get(airbrite.api.Product.collection_url())
        self.assertIsInstance(result, dict)

    def test_get_products(self):
        products, products_paging = airbrite.api.Product.list()
        self.assertIsInstance(products, list)
        self.assertIsInstance(products_paging, dict)

    def test_create_and_retrieve_product(self):
        sku = str(uuid.uuid4())
        price = 150
        name = 'Test Product'

        # Create the product
        product = airbrite.api.Product(sku=sku, price=price, name=name)
        product.save()
        self.assertIsNotNone(product._id)
        self.assertNotEqual(product._id, '')
        self.assertEqual(product.sku, sku)

        # Fetch it back
        same_product = airbrite.api.Product.fetch(_id=product._id)
        self.assertEqual(same_product.sku, sku)
        self.assertEqual(same_product.name, name)

        # Make sure it's in the list
        products, paging = airbrite.api.Product.list()
        self.assertTrue(not paging.get('has_more'))
        is_there = False
        for product in products:
            if product._id == same_product._id:
                is_there = True
                break
        self.assertTrue(is_there)


class OrderCRUDTestCase (unittest.TestCase):

    DATA = {
        'line_items': [{
            'sku': 'white-tshirt-xl',
            'quantity': 1
        }],
        'payment': [{
            "gateway": "stripe",
            "currency": "usd",
            "charge_token": "ch_2djiAbQIPi1BEL",
        }]
    }

    def test_get_orders(self):
        orders, orders_paging = airbrite.api.Order.list()
        self.assertIsInstance(orders, list)
        self.assertIsInstance(orders_paging, dict)

    def test_create_and_retrieve_order(self):
        # Create the product
        order = airbrite.api.Order(line_items=self.DATA['line_items'],
                                   payment=self.DATA['payment'])
        self.assertIsNone(order._id)
        self.assertEqual(len(order.line_items), 1)
        order.save()
        self.assertIsNotNone(order._id)
        self.assertEqual(len(order.line_items), 1)

        # Fetch it back
        same_order = airbrite.api.Order.fetch(_id=order._id)
        self.assertEqual(len(same_order.line_items), 1)

        # Make sure it's in the list
        is_there, has_more = False, True
        offset, limit = 0, 100
        while not is_there and has_more:
            # Get the next page
            orders, paging = airbrite.api.Order.list(limit=limit,
                                                     offset=offset)
            # Update the params
            has_more = paging.get('has_more', False)
            if has_more:
                offset, limit = paging['offset'], paging['limit']
            # Search for the order in this page
            for order in orders:
                if order._id == same_order._id:
                    is_there = True
                    break
        self.assertTrue(is_there)

    def test_update_products_in_order(self):
        # Create the product
        order = airbrite.api.Order(line_items=self.DATA['line_items'],
                                   payment=self.DATA['payment'])
        order.save()
        self.assertIsNotNone(order._id)

        # Fetch it back
        _id = order._id
        del order
        order = airbrite.api.Order.fetch(_id=_id)
        self.assertEqual(len(order.line_items), 1)

        # Update the order
        p = order.line_items[0]
        quantity = p['quantity']
        new_quantity = quantity + 1
        p['quantity'] = new_quantity
        order.save()
        self.assertEqual(order.line_items[0]['quantity'], new_quantity)

        # Fetch it back, and ensure the order was updated
        _id = order._id
        del order
        order = airbrite.api.Order.fetch(_id=_id)
        self.assertEqual(order.line_items[0]['quantity'], new_quantity)
