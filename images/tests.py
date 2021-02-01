"""Tests the CusDeb API Images application. """

import json

from django.urls import reverse
from rest_framework.views import status

from util.base_test import BaseSingleUserTest


class InitStageTest(BaseSingleUserTest):
    """Tests various functionalities related to the initialization stage. """

    def test_listing_devices(self):
        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user),
                                content_type='application/json')

        header = b'Bearer ' + json.loads(auth.content)['access'].encode()
        url = reverse('list-devices', kwargs={'version': 'v1'})
        response = self.client.get(url, content_type='application/json',
                                   HTTP_AUTHORIZATION=header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
