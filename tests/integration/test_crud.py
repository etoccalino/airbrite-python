import unittest
import uuid

import airbrite.api
import airbrite.client


import logging
logging.basicConfig(level=logging.DEBUG)


class ProductCRUDTestCase (unittest.TestCase):

    logger = logging.getLogger('test.products')

    def test_backend_connection(self):
        """Tests the simplest call that should succeed"""
        self.c = airbrite.client.Client()
        result = self.c.get(airbrite.api.Product.collection_url())
        self.assertIsInstance(result, dict)

    def test_get_products(self):
        products, products_paging = airbrite.api.Product.list()
        self.assertIsInstance(products, list)
        self.assertIsInstance(products_paging, dict)

    def test_CRUD_single_product(self):
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
