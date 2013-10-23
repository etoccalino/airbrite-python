import unittest
import json
import mock

import airbrite.client


class ClientData (unittest.TestCase):

    def setUp(self):
        super(ClientData, self).setUp()
        self.client = airbrite.client.Client()

    def test_has_endpoint(self):
        self.assertIsNotNone(self.client.endpoint)

    def test_has_api_key(self):
        self.assertIsNotNone(self.client.api_key)

    def test_has_creadentials(self):
        auth = self.client.auth
        self.assertIsNotNone(auth)
        self.assertEqual(len(auth), 2)
        self.assertIsNotNone(auth[0])
        self.assertIsNotNone(auth[1])


class ClientMethods (unittest.TestCase):

    def setUp(self):
        super(ClientMethods, self).setUp()

        self.get_patcher = mock.patch('requests.get')
        self.put_patcher = mock.patch('requests.put')
        self.post_patcher = mock.patch('requests.post')
        self._get = self.get_patcher.start()
        self._put = self.put_patcher.start()
        self._post = self.post_patcher.start()

        self.client = airbrite.client.Client()
        self.url = '/tests'

    def tearDown(self):
        super(ClientMethods, self).tearDown()
        self.get_patcher.stop()
        self.put_patcher.stop()
        self.post_patcher.stop()

    def test_get_by_id(self):
        ret = mock.MagicMock()
        ret.status_code = 200
        ret.json = mock.MagicMock(return_value=dict())
        self._get.return_value = ret

        res = self.client.get(self.url, _id='some_id')
        self.assertIsNotNone(res)
        self.assertIsInstance(res, dict)

        self._get.called_once_with(_id='some_id')

    def test_bad_params(self):
        ret = mock.MagicMock()
        ret.status_code = 404
        self._get.return_value = ret

        self.assertRaises(Exception, self.client.get, self.url)
        self._get.assert_called_once()

    def test_get_all(self):
        ret = mock.MagicMock()
        ret.status_code = 200
        ret.json = mock.MagicMock(return_value={
            'data': [{
            }],
            'meta': {
            },
            'paging': {
            }
        })
        self._get.return_value = ret

        res = self.client.get(self.url)
        self.assertIsNotNone(res)
        self.assertIsInstance(res, dict)
        self.assertTrue('data' in res)
        self.assertTrue('paging' in res)
        self.assertTrue('meta' in res)

        self._get.assert_called_once()

    def test_post_single(self):
        """Test the POST without _id"""
        data = {'key': 'value'}
        ret = mock.MagicMock()
        ret.status_code = 200
        ret.json = mock.MagicMock(return_value={
            'data': data,
            'meta': {}
        })
        self._post.return_value = ret
        self._put.return_value = ret
        res = self.client.post(self.url, **data)

        self.assertIsNotNone(res)
        self.assertIsInstance(res, dict)
        self.assertTrue('meta' in res)
        self.assertTrue('data' in res)
        self.assertEqual('value', res['data']['key'])

        self._post.assert_called_once_with(self.url,
                                           auth=self.client.auth,
                                           headers=self.client.headers,
                                           data=json.dumps(data))
        self._put.assert_not_called()

    def test_put_single(self):
        """Test the POST without _id"""
        data = {'_id': 'some-id', 'key': 'value'}
        ret = mock.MagicMock()
        ret.status_code = 200
        ret.json = mock.MagicMock(return_value={
            'data': data,
            'meta': {}
        })
        self._post.return_value = ret
        self._put.return_value = ret
        res = self.client.put(self.url, **data)

        self.assertIsNotNone(res)
        self.assertIsInstance(res, dict)
        self.assertTrue('meta' in res)
        self.assertTrue('data' in res)
        self.assertEqual('value', res['data']['key'])

        self._put.assert_called_once_with(self.url,
                                          auth=self.client.auth,
                                          headers=self.client.headers,
                                          data=json.dumps(data))
        self._post.assert_not_called()
