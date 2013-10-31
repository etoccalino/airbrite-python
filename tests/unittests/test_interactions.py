import unittest
import airbrite

from utils import TestClient


class OrderAndShipment (unittest.TestCase):

    # def setUp(self):
    #     super(OrderAndShipment, self).setUp()
    #     airbrite.Order.client = TestClient(airbrite.Order)
    #     airbrite.Shipment.client = TestClient(airbrite.Shipment)

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
        self.assertTrue('halted' in all_status)

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


class OrderAndPayment (unittest.TestCase):

    def setUp(self):
        self.ORDER = TestClient.CANNED[airbrite.Order][0].copy()
        self.PAY = TestClient.CANNED[airbrite.Payment][0].copy()

    def test_add_to_order(self):
        del self.PAY['order_id']
        order = airbrite.Order(**self.ORDER)
        payment = airbrite.Payment(**self.PAY)

        self.assertEqual(len(order.payments), 0)
        order.payments.add(payment)
        self.assertEqual(len(order.payments), 1)

    def test_remove_to_order(self):
        del self.PAY['order_id']
        order = airbrite.Order(**self.ORDER)
        payment = airbrite.Payment(**self.PAY)

        self.assertEqual(len(order.payments), 0)
        order.payments.add(payment)
        self.assertEqual(len(order.payments), 1)

        del payment
        payment = airbrite.Payment(**self.PAY)

        self.assertEqual(len(order.payments), 1)
        order.payments.remove(payment)
        self.assertEqual(len(order.payments), 0)


class OrderAndCustomer (unittest.TestCase):

    def setUp(self):
        super(OrderAndCustomer, self).setUp()
        self.ORDER = TestClient.CANNED[airbrite.Order][0].copy()
        self.CUSTOMER = TestClient.CANNED[airbrite.Customer][0].copy()
        airbrite.Order.client = TestClient(airbrite.Order)
        airbrite.Shipment.client = TestClient(airbrite.Shipment)

    def test_add_customer_by_id(self):
        customer_id = self.CUSTOMER['_id']
        del self.ORDER['customer_id']
        order = airbrite.Order(customer_id=customer_id, **self.ORDER)
        self.assertIsNotNone(order.customer_id)
