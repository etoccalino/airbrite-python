import unittest
import airbrite
import mock

from tests.utils import TestClient


class ProductTestCase(unittest.TestCase):
    """Test the actual Product, not its REST endpoint functionality"""
    DATA1 = TestClient.CANNED[airbrite.Product][0]
    DATA2 = TestClient.CANNED[airbrite.Product][1]

    def setUp(self):
        super(ProductTestCase, self).setUp()
        self._client = airbrite.Product.client
        client = TestClient(airbrite.Product)
        airbrite.Product.client = client

    def tearDown(self):
        super(ProductTestCase, self).tearDown()
        airbrite.Product.client = self._client

    def test_endpoint(self):
        self.assertEqual(airbrite.Product.class_url, 'products')
        product = airbrite.Product(**self.DATA1)
        expected = "%(endpoint)s/%(collection)s/%(_id)s" % {
            'endpoint': airbrite.api.END_POINT,
            'collection': 'products',
            '_id': self.DATA1['_id']
        }
        self.assertEqual(product.instance_url(), expected)

    def test_construct(self):
        product = airbrite.Product(**self.DATA1)
        self.assertIsInstance(product, airbrite.Product)
        self.assertEqual(product._id, self.DATA1['_id'])
        self.assertEqual(product.user_id, self.DATA1['user_id'])

    def test_construct_two(self):
        product1 = airbrite.Product(**self.DATA1)
        product2 = airbrite.Product(**self.DATA2)
        self.assertIsInstance(product1, airbrite.Product)
        self.assertIsInstance(product2, airbrite.Product)
        self.assertNotEqual(product1._id, product2._id)
        self.assertEqual(product1.user_id, self.DATA1['user_id'])
        self.assertEqual(product2.user_id, self.DATA1['user_id'])

    def test_fetch(self):
        product = airbrite.Product.fetch(_id=self.DATA1['_id'])
        self.assertIsInstance(product, airbrite.Product)
        self.assertEqual(product._id, self.DATA1['_id'])
        self.assertEqual(product.user_id, self.DATA1['user_id'])

    def test_refresh(self):
        product = airbrite.Product(_id=self.DATA1['_id'])
        product.refresh()
        self.assertIsInstance(product, airbrite.Product)
        self.assertEqual(product._id, self.DATA1['_id'])
        self.assertEqual(product.user_id, self.DATA1['user_id'])

    def test_create(self):
        data = {
            'sku': self.DATA1.get('sku'),
            'price': self.DATA1.get('price'),
            'name': self.DATA1.get('name'),
            'description': self.DATA1.get('description'),
            'metadata': self.DATA1.get('metadata'),
        }
        product = airbrite.Product.create(**data)

        self.assertEqual(product.sku, data['sku'])
        self.assertEqual(product.price, data['price'])

        self.assertEqual(len(airbrite.Product.client._posted), 1)
        created = airbrite.Product.client._posted[0]
        self.assertTrue('_id' in created)
        del created['_id']
        self.assertEqual(created, data)

    def test_save(self):
        data = {
            'sku': self.DATA1.get('sku'),
            'price': self.DATA1.get('price'),
            'name': self.DATA1.get('name'),
            'description': self.DATA1.get('description'),
            'metadata': self.DATA1.get('metadata'),
        }
        product = airbrite.Product(**data)

        self.assertEqual(product.sku, data['sku'])
        self.assertEqual(product.price, data['price'])
        product.save()
        self.assertIsNotNone(product._id)
        self.assertEqual(product.sku, data['sku'])
        self.assertEqual(product.price, data['price'])

    def test_update(self):
        NAME = 'a new name'
        product = airbrite.Product.fetch(_id=self.DATA1['_id'])
        self.assertNotEqual(product.name, NAME)
        product.name = NAME
        product.save()
        self.assertEqual(product.name, NAME)
        self.assertEqual(len(airbrite.Product.client._put), 1)

    def test_is_persisted(self):
        data = {
            'sku': self.DATA1.get('sku'),
            'price': self.DATA1.get('price'),
            'name': self.DATA1.get('name'),
            'description': self.DATA1.get('description'),
            'metadata': self.DATA1.get('metadata'),
        }
        product = airbrite.Product(**data)
        self.assertTrue(not product.is_persisted)

        product.save()
        self.assertEqual(len(airbrite.Product.client._posted), 1)
        self.assertTrue(product.is_persisted)

        product.save()
        self.assertEqual(len(airbrite.Product.client._posted), 1)
        self.assertEqual(len(airbrite.Product.client._put), 1)
        self.assertTrue(product.is_persisted)

    def test_full_list(self):
        products, paging = airbrite.Product.list()
        self.assertEqual(len(products), 2)
        self.assertEqual(paging['count'], 2)
        self.assertEqual(paging['total'], 2)
        self.assertIsInstance(products[0], airbrite.Product)
        self.assertIsInstance(products[1], airbrite.Product)


class ListProductTestCase(unittest.TestCase):

    DATA1 = TestClient.CANNED[airbrite.Product][0]
    DATA2 = TestClient.CANNED[airbrite.Product][1]

    def setUp(self):
        super(ListProductTestCase, self).setUp()
        self._client = airbrite.Product.client

        self.mockClient = mock.MagicMock()
        self.mockClient.get = mock.MagicMock()
        self.mockClient.put = mock.MagicMock()
        self.mockClient.post = mock.MagicMock()
        airbrite.Product.client = self.mockClient

    def tearDown(self):
        super(ListProductTestCase, self).tearDown()
        airbrite.Product.client = self._client

    def test_list_filters(self):
        _, _ = airbrite.Product.list(limit=1, offset=1, sort='field')
        self.mockClient.get.assert_called_once_with(
            airbrite.Product.collection_url(),
            limit=1, offset=1, sort='field')

    def test_list_bad_filters(self):
        self.assertRaises(Exception, airbrite.Product.list,
                          limit=1, offset='two', sort='field')

    def test_full_list(self):
        c = airbrite.Product.client
        airbrite.Product.client = TestClient(airbrite.Product)

        products, paging = airbrite.Product.list()
        self.assertEqual(len(products), 2)
        self.assertEqual(paging['count'], 2)
        self.assertEqual(paging['total'], 2)
        self.assertIsInstance(products[0], airbrite.Product)
        self.assertIsInstance(products[1], airbrite.Product)

        airbrite.Product.client = c


class OrderTestCase(unittest.TestCase):
    """Test the actual Order, not its REST endpoint functionality"""
    DATA1 = TestClient.CANNED[airbrite.Order][0]
    DATA2 = TestClient.CANNED[airbrite.Order][1]

    def setUp(self):
        super(OrderTestCase, self).setUp()
        self._client = airbrite.Order.client
        client = TestClient(airbrite.Order)
        airbrite.Order.client = client

    def tearDown(self):
        super(OrderTestCase, self).tearDown()
        airbrite.Order.client = self._client

    def test_endpoint(self):
        self.assertEqual(airbrite.Order.class_url, 'orders')
        order = airbrite.Order(**self.DATA1)
        expected = "%(endpoint)s/orders/%(_id)s" % {
            'endpoint': airbrite.api.END_POINT,
            '_id': self.DATA1['_id']
        }
        self.assertEqual(order.instance_url(), expected)

    def test_construct(self):
        order = airbrite.Order(**self.DATA1)
        self.assertIsInstance(order, airbrite.Order)
        self.assertEqual(order._id, self.DATA1['_id'])
        self.assertEqual(order.user_id, self.DATA1['user_id'])

    def test_construct_two(self):
        order1 = airbrite.Order(**self.DATA1)
        order2 = airbrite.Order(**self.DATA2)
        self.assertIsInstance(order1, airbrite.Order)
        self.assertIsInstance(order2, airbrite.Order)
        self.assertNotEqual(order1._id, order2._id)
        self.assertEqual(order1.user_id, self.DATA1['user_id'])
        self.assertEqual(order2.user_id, self.DATA1['user_id'])

    def test_fetch(self):
        order = airbrite.Order.fetch(_id=self.DATA1['_id'])
        self.assertIsInstance(order, airbrite.Order)
        self.assertEqual(order._id, self.DATA1['_id'])
        self.assertEqual(order.customer_id, self.DATA1['customer_id'])

    def test_refresh(self):
        order = airbrite.Order(_id=self.DATA1['_id'])
        order.refresh()
        self.assertIsInstance(order, airbrite.Order)
        self.assertEqual(order._id, self.DATA1['_id'])
        self.assertEqual(order.customer_id, self.DATA1['customer_id'])

    def test_create(self):
        data = {
            'customer_id': self.DATA1.get('customer_id'),
            'currency': self.DATA1.get('currency'),
            'line_items': self.DATA1.get('line_items', []),
            'shipping_address': self.DATA1.get('shipping_address', {}),
            'discount': self.DATA1.get('discount', {}),
            'shipping': self.DATA1.get('shipping', {}),
            'tax': self.DATA1.get('tax', {}),
        }
        order = airbrite.Order.create(**data)

        self.assertEqual(order.customer_id, data['customer_id'])
        self.assertEqual(order.currency, data['currency'])

        self.assertEqual(len(airbrite.Order.client._posted), 1)
        created = airbrite.Order.client._posted[0]
        self.assertTrue('_id' in created)
        del created['_id']
        self.assertEqual(created, data)

    def test_save(self):
        data = {
            'customer_id': self.DATA1.get('customer_id'),
            'currency': self.DATA1.get('currency'),
            'line_items': self.DATA1.get('line_items', []),
            'shipping_address': self.DATA1.get('shipping_address', {}),
            'discount': self.DATA1.get('discount', {}),
            'shipping': self.DATA1.get('shipping', {}),
            'tax': self.DATA1.get('tax', {}),
        }
        order = airbrite.Order(**data)

        self.assertEqual(order.customer_id, data['customer_id'])
        self.assertEqual(order.currency, data['currency'])
        order.save()
        self.assertIsNotNone(order._id)
        self.assertEqual(order.customer_id, data['customer_id'])
        self.assertEqual(order.currency, data['currency'])

    def test_update(self):
        DESCRIPTION = 'a new order'
        order = airbrite.Order.fetch(_id=self.DATA1['_id'])
        self.assertNotEqual(order.description, DESCRIPTION)
        order.description = DESCRIPTION
        order.save()
        self.assertEqual(order.description, DESCRIPTION)
        self.assertEqual(len(airbrite.Order.client._put), 1)

    def test_is_persisted(self):
        data = {
            'customer_id': self.DATA1.get('customer_id'),
            'currency': self.DATA1.get('currency'),
            'line_items': self.DATA1.get('line_items', []),
            'shipping_address': self.DATA1.get('shipping_address', {}),
            'discount': self.DATA1.get('discount', {}),
            'shipping': self.DATA1.get('shipping', {}),
            'tax': self.DATA1.get('tax', {}),
        }
        order = airbrite.Order(**data)
        self.assertTrue(not order.is_persisted)

        order.save()
        self.assertEqual(len(airbrite.Order.client._posted), 1)
        self.assertTrue(order.is_persisted)

        order.save()
        self.assertEqual(len(airbrite.Order.client._posted), 1)
        self.assertEqual(len(airbrite.Order.client._put), 1)
        self.assertTrue(order.is_persisted)

    def test_raw_add_to_list_items(self):
        product_data = {'sku': 'some-product', 'quantity': 3}
        order = airbrite.Order()
        self.assertEqual(len(order.line_items), 0)
        order.line_items.append(product_data)
        self.assertEqual(len(order.line_items), 1)
        self.assertEqual(order.line_items[0], product_data)

    def test_add_item(self):
        product = airbrite.Product(sku='some-sku')
        order = airbrite.Order()
        self.assertEqual(len(order.line_items), 0)
        order.add_item(product, 2)
        self.assertEqual(len(order.line_items), 1)
        self.assertEqual(order.line_items[0]['sku'], 'some-sku')

    def test_add_shipment_on_creation(self):
        shipment = airbrite.Shipment(status='in_progress')
        order = airbrite.Order(shipments=[shipment])
        self.assertEqual(len(order.shipments), 1)

    def test_add_shipment(self):
        shipment = airbrite.Shipment(status='in_progress')
        order = airbrite.Order()

        self.assertEqual(len(order.shipments), 0)
        order.shipments.add(shipment)
        self.assertEqual(len(order.shipments), 1)
        self.assertEqual(order.shipments[0].status, 'in_progress')

    def test_add_shipments(self):
        shipment1 = airbrite.Shipment(status='in_progress')
        shipment2 = airbrite.Shipment(status='halted')
        order = airbrite.Order()
        self.assertEqual(len(order.shipments), 0)
        order.shipments.add(shipment1)
        order.shipments.add(shipment2)
        self.assertEqual(len(order.shipments), 2)
        all_status = [s.status for s in order.shipments]
        self.assertTrue('in_progress' in all_status)

    def test_remove_shipment(self):
        shipment1 = airbrite.Shipment(_id='123', status='in_progress')
        shipment2 = airbrite.Shipment(status='pending')
        order = airbrite.Order(shipments=[shipment1, shipment2])
        self.assertIsInstance(order.shipments, airbrite.api.EntityCollection)
        self.assertEqual(len(order.shipments), 2)

        # shipment1 does not have an ID yet
        self.assertRaises(Exception, order.shipments.remove, shipment2)

        # Replace collection, instead of removing a single entry
        order.shipments.remove(shipment1)
        self.assertEqual(len(order.shipments), 1)
        self.assertEqual(shipment2.status, order.shipments[0].status)


class ListOrderTestCase(unittest.TestCase):

    DATA1 = TestClient.CANNED[airbrite.Order][0]
    DATA2 = TestClient.CANNED[airbrite.Order][1]

    def setUp(self):
        super(ListOrderTestCase, self).setUp()
        self._client = airbrite.Order.client

        self.mockClient = mock.MagicMock()
        self.mockClient.get = mock.MagicMock()
        self.mockClient.put = mock.MagicMock()
        self.mockClient.post = mock.MagicMock()
        airbrite.Order.client = self.mockClient

    def tearDown(self):
        super(ListOrderTestCase, self).tearDown()
        airbrite.Order.client = self._client

    def test_list_filters(self):
        _, _ = airbrite.Order.list(limit=1, offset=1, sort='field')
        self.mockClient.get.assert_called_once_with(
            airbrite.Order.collection_url(),
            limit=1, offset=1, sort='field')

    def test_list_bad_filters(self):
        self.assertRaises(Exception, airbrite.Order.list,
                          limit=1, offset='two', sort='field')

    def test_full_list(self):
        c = airbrite.Order.client
        airbrite.Order.client = TestClient(airbrite.Order)

        orders, paging = airbrite.Order.list()
        self.assertEqual(len(orders), 2)
        self.assertEqual(paging['count'], 2)
        self.assertEqual(paging['total'], 2)
        self.assertIsInstance(orders[0], airbrite.Order)
        self.assertIsInstance(orders[1], airbrite.Order)

        airbrite.Order.client = c


class ShipmentTestCase(unittest.TestCase):
    """Test the actual Shipment, not its REST endpoint functionality"""
    ORDER = TestClient.CANNED[airbrite.Order][0]
    SHIP1 = TestClient.CANNED[airbrite.Shipment][0]
    SHIP2 = TestClient.CANNED[airbrite.Shipment][1]

    def setUp(self):
        super(ShipmentTestCase, self).setUp()
        self._client = airbrite.Shipment.client
        client = TestClient(airbrite.Shipment)
        airbrite.Shipment.client = client

    def tearDown(self):
        super(ShipmentTestCase, self).tearDown()
        airbrite.Shipment.client = self._client

    def test_endpoint(self):
        shipment = airbrite.Shipment(**self.SHIP1)
        expected = "%(endpoint)s/orders/%(order_id)s/shipments/%(_id)s" % {
            'endpoint': airbrite.api.END_POINT,
            'order_id': self.SHIP1['order_id'],
            '_id': self.SHIP1['_id']
        }
        self.assertEqual(shipment.instance_url(), expected)

    def test_construct(self):
        shipment = airbrite.Shipment(**self.SHIP1)
        self.assertIsInstance(shipment, airbrite.Shipment)
        self.assertEqual(shipment._id, self.SHIP1['_id'])
        self.assertEqual(shipment.order_id, self.SHIP1['order_id'])

    def test_construct_two(self):
        shipment1 = airbrite.Shipment(**self.SHIP1)
        shipment2 = airbrite.Shipment(**self.SHIP2)
        self.assertIsInstance(shipment1, airbrite.Shipment)
        self.assertIsInstance(shipment2, airbrite.Shipment)
        self.assertNotEqual(shipment1._id, shipment2._id)
        self.assertEqual(shipment1.order_id, self.SHIP1['order_id'])
        self.assertEqual(shipment2.order_id, self.SHIP1['order_id'])

    def test_comparison(self):
        shipment1 = airbrite.Shipment(**self.SHIP1)
        shipment2 = airbrite.Shipment(**self.SHIP2)
        shipment1_prime = airbrite.Shipment(**self.SHIP1)

        self.assertEqual(shipment1, shipment1_prime)
        self.assertNotEqual(shipment1, shipment2)

        self.assertTrue(shipment1 == shipment1_prime)
        self.assertTrue(shipment1 != shipment2)

    def test_fetch(self):
        shipment = airbrite.Shipment.fetch(_id=self.SHIP1['_id'],
                                           order_id=self.ORDER['_id'])
        self.assertIsInstance(shipment, airbrite.Shipment)
        self.assertEqual(shipment._id, self.SHIP1['_id'])
        self.assertEqual(shipment.order_id, self.SHIP1['order_id'])

    def test_refresh(self):
        shipment = airbrite.Shipment(_id=self.SHIP1['_id'],
                                     order_id=self.SHIP1['order_id'])
        shipment.refresh()
        self.assertIsInstance(shipment, airbrite.Shipment)
        self.assertEqual(shipment._id, self.SHIP1['_id'])
        self.assertEqual(shipment.order_id, self.SHIP1['order_id'])

    def test_create(self):
        data = {
            'order_id': self.SHIP1.get('order_id'),
            'shipping_address': self.SHIP1.get('shipping_address'),
        }
        shipment = airbrite.Shipment.create(**data)

        self.assertEqual(shipment.order_id, data['order_id'])
        self.assertEqual(shipment.shipping_address, data['shipping_address'])

        self.assertEqual(len(airbrite.Shipment.client._posted), 1)
        created = airbrite.Shipment.client._posted[0]
        self.assertTrue('_id' in created)
        del created['_id']
        self.assertEqual(created, data)

    def test_create_without_order(self):
        data = {
            'shipping_address': self.SHIP1.get('shipping_address'),
        }
        self.assertRaises(Exception, airbrite.Shipment.create, **data)

    def test_save(self):
        data = {
            'order_id': self.SHIP1.get('order_id'),
            'shipping_address': self.SHIP1.get('shipping_address'),
        }
        shipment = airbrite.Shipment(**data)

        self.assertEqual(shipment.order_id, data['order_id'])
        self.assertEqual(shipment.shipping_address, data['shipping_address'])
        shipment.save()
        self.assertIsNotNone(shipment._id)
        self.assertEqual(shipment.order_id, data['order_id'])
        self.assertEqual(shipment.shipping_address, data['shipping_address'])

    def test_save_without_order(self):
        data = {
            'shipping_address': self.SHIP1.get('shipping_address'),
        }
        self.assertRaises(Exception, airbrite.Shipment.save, **data)

    def test_update(self):
        DESCRIPTION = 'a new shipment'
        shipment = airbrite.Shipment.fetch(_id=self.SHIP1['_id'],
                                           order_id=self.SHIP1['order_id'])
        self.assertNotEqual(shipment.description, DESCRIPTION)
        shipment.description = DESCRIPTION
        shipment.save()
        self.assertEqual(shipment.description, DESCRIPTION)
        self.assertEqual(len(airbrite.Shipment.client._put), 1)

    def test_is_persisted(self):
        data = {
            'order_id': self.SHIP1.get('order_id'),
            'shipping_address': self.SHIP1.get('shipping_address'),
        }
        shipment = airbrite.Shipment(**data)
        self.assertTrue(not shipment.is_persisted)

        shipment.save()
        self.assertEqual(len(airbrite.Shipment.client._posted), 1)
        self.assertTrue(shipment.is_persisted)

        shipment.save()
        self.assertEqual(len(airbrite.Shipment.client._posted), 1)
        self.assertEqual(len(airbrite.Shipment.client._put), 1)
        self.assertTrue(shipment.is_persisted)


class CustomerTestCase(unittest.TestCase):
    """Test the actual Customer, not its REST endpoint functionality"""
    DATA1 = TestClient.CANNED[airbrite.Customer][0]
    DATA2 = TestClient.CANNED[airbrite.Customer][1]

    def setUp(self):
        super(CustomerTestCase, self).setUp()
        self._client = airbrite.Customer.client
        client = TestClient(airbrite.Customer)
        airbrite.Customer.client = client

    def tearDown(self):
        super(CustomerTestCase, self).tearDown()
        airbrite.Customer.client = self._client

    def test_endpoint(self):
        self.assertEqual(airbrite.Customer.class_url, 'customers')
        customer = airbrite.Customer(**self.DATA1)
        expected = "%(endpoint)s/customers/%(_id)s" % {
            'endpoint': airbrite.api.END_POINT,
            '_id': self.DATA1['_id']
        }
        self.assertEqual(customer.instance_url(), expected)

    def test_construct(self):
        customer = airbrite.Customer(**self.DATA1)
        self.assertIsInstance(customer, airbrite.Customer)
        self.assertEqual(customer._id, self.DATA1['_id'])
        self.assertEqual(customer.user_id, self.DATA1['user_id'])

    def test_construct_two(self):
        customer1 = airbrite.Customer(**self.DATA1)
        customer2 = airbrite.Customer(**self.DATA2)
        self.assertIsInstance(customer1, airbrite.Customer)
        self.assertIsInstance(customer2, airbrite.Customer)
        self.assertNotEqual(customer1._id, customer2._id)
        self.assertEqual(customer1.user_id, self.DATA1['user_id'])
        self.assertEqual(customer2.user_id, self.DATA2['user_id'])

    def test_fetch(self):
        customer = airbrite.Customer.fetch(_id=self.DATA1['_id'])
        self.assertIsInstance(customer, airbrite.Customer)
        self.assertEqual(customer._id, self.DATA1['_id'])
        self.assertEqual(customer.user_id, self.DATA1['user_id'])
        self.assertEqual(customer.stripe_customer_id,
                         self.DATA1['stripe']['customer_id'])

    def test_refresh(self):
        customer = airbrite.Customer(_id=self.DATA1['_id'])
        customer.refresh()
        self.assertIsInstance(customer, airbrite.Customer)
        self.assertEqual(customer._id, self.DATA1['_id'])
        self.assertEqual(customer.user_id, self.DATA1['user_id'])

    def test_create(self):
        data = {
            'name': self.DATA1.get('name'),
            'description': self.DATA1.get('description'),
            'metadata': self.DATA1.get('metadata'),
        }
        customer = airbrite.Customer.create(**data)
        self.assertEqual(customer.name, data['name'])

        self.assertEqual(len(airbrite.Customer.client._posted), 1)
        created = airbrite.Customer.client._posted[0]
        self.assertTrue('_id' in created)
        del created['_id']
        self.assertEqual(created, data)

    def test_save(self):
        data = {
            'name': self.DATA1.get('name'),
            'description': self.DATA1.get('description'),
            'metadata': self.DATA1.get('metadata'),
        }
        customer = airbrite.Customer(**data)
        self.assertEqual(customer.name, data['name'])
        customer.save()
        self.assertIsNotNone(customer._id)
        self.assertEqual(customer.name, data['name'])

    def test_update(self):
        NAME = 'a new name'
        customer = airbrite.Customer.fetch(_id=self.DATA1['_id'])
        self.assertNotEqual(customer.name, NAME)
        customer.name = NAME
        customer.save()
        self.assertEqual(customer.name, NAME)
        self.assertEqual(len(airbrite.Customer.client._put), 1)

    def test_is_persisted(self):
        data = {
            'sku': self.DATA1.get('sku'),
            'price': self.DATA1.get('price'),
            'name': self.DATA1.get('name'),
            'description': self.DATA1.get('description'),
            'metadata': self.DATA1.get('metadata'),
        }
        customer = airbrite.Customer(**data)
        self.assertTrue(not customer.is_persisted)

        customer.save()
        self.assertEqual(len(airbrite.Customer.client._posted), 1)
        self.assertTrue(customer.is_persisted)

        customer.save()
        self.assertEqual(len(airbrite.Customer.client._posted), 1)
        self.assertEqual(len(airbrite.Customer.client._put), 1)
        self.assertTrue(customer.is_persisted)

    def test_full_list(self):
        customers, paging = airbrite.Customer.list()
        self.assertEqual(len(customers), 2)
        self.assertEqual(paging['count'], 2)
        self.assertEqual(paging['total'], 2)
        self.assertIsInstance(customers[0], airbrite.Customer)
        self.assertIsInstance(customers[1], airbrite.Customer)


class ListCustomerTestCase(unittest.TestCase):

    DATA1 = TestClient.CANNED[airbrite.Customer][0]
    DATA2 = TestClient.CANNED[airbrite.Customer][1]

    def setUp(self):
        super(ListCustomerTestCase, self).setUp()
        self._client = airbrite.Customer.client

        self.mockClient = mock.MagicMock()
        self.mockClient.get = mock.MagicMock()
        self.mockClient.put = mock.MagicMock()
        self.mockClient.post = mock.MagicMock()
        airbrite.Customer.client = self.mockClient

    def tearDown(self):
        super(ListCustomerTestCase, self).tearDown()
        airbrite.Customer.client = self._client

    def test_list_filters(self):
        _, _ = airbrite.Customer.list(limit=1, offset=1, sort='field')
        self.mockClient.get.assert_called_once_with(
            airbrite.Customer.collection_url(),
            limit=1, offset=1, sort='field')

    def test_list_bad_filters(self):
        self.assertRaises(Exception, airbrite.Customer.list,
                          limit=1, offset='two', sort='field')

    def test_full_list(self):
        c = airbrite.Customer.client
        airbrite.Customer.client = TestClient(airbrite.Customer)

        customers, paging = airbrite.Customer.list()
        self.assertEqual(len(customers), 2)
        self.assertEqual(paging['count'], 2)
        self.assertEqual(paging['total'], 2)
        self.assertIsInstance(customers[0], airbrite.Customer)
        self.assertIsInstance(customers[1], airbrite.Customer)

        airbrite.Customer.client = c
