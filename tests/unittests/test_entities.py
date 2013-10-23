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
        self.assertNotEqual(product._id, '')
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
        _, _ = airbrite.Product.list(limit=1, skip=1, sort='field')
        self.mockClient.get.assert_called_once_with(
            airbrite.Product.collection_url(),
            limit=1, skip=1, sort='field')

    def test_list_bad_filters(self):
        self.assertRaises(Exception, airbrite.Product.list,
                          limit=1, skip='two', sort='field')

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
        expected = "%(endpoint)s/%(collection)s/%(_id)s" % {
            'endpoint': airbrite.api.END_POINT,
            'collection': 'orders',
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
            'currency': self.DATA1.get('currenty'),
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
            'currency': self.DATA1.get('currenty'),
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
        self.assertNotEqual(order._id, '')
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
            'currency': self.DATA1.get('currenty'),
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
        _, _ = airbrite.Order.list(limit=1, skip=1, sort='field')
        self.mockClient.get.assert_called_once_with(
            airbrite.Order.collection_url(),
            limit=1, skip=1, sort='field')

    def test_list_bad_filters(self):
        self.assertRaises(Exception, airbrite.Order.list,
                          limit=1, skip='two', sort='field')

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
