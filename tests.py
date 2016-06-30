#!/usr/bin/env python

import unittest

from timeofday import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_works(self):
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_api_v1_works(self):
        rv = self.app.get('/api/v1')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_ics_works(self):
        rv = self.app.get('/ics')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers['Content-Type'], 'text/calendar')


if __name__ == '__main__':
    unittest.main()
