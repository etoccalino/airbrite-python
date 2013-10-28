import unittest
import uuid

import airbrite
import airbrite.client


class ProductCRUDTestCase (unittest.TestCase):

    def test_backend_connection(self):
        """Tests the simplest call that should succeed"""
        self.c = airbrite.client.Client()
        result = self.c.get(airbrite.Product.collection_url())
        self.assertIsInstance(result, dict)

    def test_get_products(self):
        products, products_paging = airbrite.Product.list()
        self.assertIsInstance(products, list)
        self.assertIsInstance(products_paging, dict)

    def test_get_products_with_limit(self):
        products, products_paging = airbrite.Product.list(limit=3)
        self.assertEqual(products_paging['count'], 3)
        self.assertEqual(len(products), 3)

    def test_create_and_retrieve_product(self):
        sku = str(uuid.uuid4())
        price = 150
        name = 'Test Product'

        # Create the product
        product = airbrite.Product(sku=sku, price=price, name=name)
        product.save()
        self.assertIsNotNone(product._id)
        self.assertNotEqual(product._id, '')
        self.assertEqual(product.sku, sku)

        # Fetch it back
        same_product = airbrite.Product.fetch(_id=product._id)
        self.assertEqual(same_product.sku, sku)
        self.assertEqual(same_product.name, name)

        # Make sure it's in the list

        # Make sure it's in the list
        is_there, has_more = False, True
        offset, limit = 0, 100
        while not is_there and has_more:
            # Get the next page
            products, paging = airbrite.Product.list(limit=limit,
                                                     offset=offset)
            # Update the params
            has_more = paging.get('has_more', False)
            if has_more:
                offset, limit = paging['offset'], paging['limit']
            # Search for the order in this page
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
        orders, orders_paging = airbrite.Order.list()
        self.assertIsInstance(orders, list)
        self.assertIsInstance(orders_paging, dict)

    def test_create_order_with_shipment(self):
        shipments_data = [{
            'courier': 'courier one',
            'status': 'in_progress',
        }, {
            'courier': 'courier two',
            'status': 'pending',
        }]
        shipment1 = airbrite.Shipment(**shipments_data[0])
        shipment2 = airbrite.Shipment(**shipments_data[1])
        order = airbrite.Order(shipments=[shipment1, shipment2])
        self.assertEqual(len(order.shipments), 2)
        order.save()

        same_order = airbrite.Order.fetch(_id=order._id)

        self.assertEqual(len(same_order.shipments), 2)

        curier_data = set(s.courier for s in same_order.shipments)
        self.assertTrue(shipments_data[0]['courier'] in curier_data)
        self.assertTrue(shipments_data[1]['courier'] in curier_data)

        status_data = set(s.status for s in same_order.shipments)
        self.assertTrue(shipments_data[0]['status'] in status_data)
        self.assertTrue(shipments_data[1]['status'] in status_data)

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
        same_order = airbrite.Order.fetch(_id=order._id)
        self.assertEqual(len(same_order.line_items), 1)

        # Make sure it's in the list
        is_there, has_more = False, True
        offset, limit = 0, 100
        while not is_there and has_more:
            # Get the next page
            orders, paging = airbrite.Order.list(limit=limit, offset=offset)
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
        # Create the order
        order = airbrite.Order(line_items=self.DATA['line_items'],
                               payment=self.DATA['payment'])
        order.save()
        self.assertIsNotNone(order._id)

        # Fetch it back
        _id = order._id
        del order
        order = airbrite.Order.fetch(_id=_id)
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
        order = airbrite.Order.fetch(_id=_id)
        self.assertEqual(order.line_items[0]['quantity'], new_quantity)
