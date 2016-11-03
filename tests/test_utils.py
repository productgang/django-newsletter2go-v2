#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-newsletter2go-v2
------------

Tests for `django-newsletter2go-v2` utils module.
"""

from django.test import TestCase

from django_newsletter2go import utils

import responses
import json


class TestDjango_newsletter2go(TestCase):

    def setUp(self):
        pass

    @responses.activate
    def test_auth_token(self):
        def request_callback(request):
            data = json.loads(request.body)
            resp_body = {
                'access_token': '{}-{}-{}'.format(
                    data.get('username'),
                    data.get('password'),
                    request.headers.get('Authorization'),
                ),
            }
            return (200, {}, json.dumps(resp_body))
        responses.add_callback(
            responses.POST, 'https://api.newsletter2go.com/oauth/v2/token',
            callback=request_callback,
            content_type='application/json',
        )
        auth_token = utils.get_n2g_token('AUTH:KEY', 'USERNAME', 'PASSWORD')
        self.assertEquals(auth_token, 'USERNAME-PASSWORD-Basic QVVUSDpLRVk=')

    @responses.activate
    def test_create_mailing(self):
        def request_callback(request):
            resp_body = {
                'value': {'id': '123'},
            }
            return (200, {}, json.dumps(resp_body))
        responses.add_callback(
            responses.POST,
            'https://api.newsletter2go.com/lists/123/newsletters',
            callback=request_callback,
            content_type='application/json',
        )
        pk = utils.create_mailing(
            'access_token', 123, utils.Newsletter(name='Test'))
        self.assertEquals(pk, '123')

    def tearDown(self):
        pass
