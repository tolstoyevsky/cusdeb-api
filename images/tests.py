import json

from django.urls import reverse
from rest_framework.views import status

from images.models import (
    BuildType,
    BuildTypeName,
    CodeName,
    DeviceName,
    Device,
    DistroName,
    OS,
    Port,
)
from util.base_test import BaseSingleUserTest


class InitStageTest(BaseSingleUserTest):
    def setUp(self):
        super().setUp()

        #
        # Supported operating systems
        #

        debian = DistroName.objects.create(name='Debian')
        buster = CodeName.objects.create(name='Buster')

        ubuntu = DistroName.objects.create(name='Ubuntu')
        bionic = CodeName.objects.create(name='Bionic Beaver')

        port = Port.objects.create(name='armhf')

        debian_buster = OS.objects.create(name=debian, codename=buster,
                                          version='10', port=port, active=True)
        ubuntu_bionic = OS.objects.create(name=ubuntu, codename=bionic,
                                          version='18.04', port=port,
                                          active=True)

        #
        # Supported devices
        #

        rpi = DeviceName.objects.create(name='Raspberry Pi')
        opi = DeviceName.objects.create(name='Orange Pi')
        dev1 = Device.objects.create(name=rpi, generation='3', model='Model B',
                                     active=True)
        dev1.supported_os.add(debian_buster, ubuntu_bionic)
        dev2 = Device.objects.create(name=opi, generation='', model='PC Plus',
                                     active=False)
        dev2.supported_os.add(debian_buster, ubuntu_bionic)

        #
        # Build types
        #

        build_type_name = BuildTypeName.objects.create(name='Classic image')
        build_type1 = BuildType.objects.create(device=dev1, os=debian_buster)
        build_type1.build_type.add(build_type_name)
        build_type2 = BuildType.objects.create(device=dev1, os=ubuntu_bionic)
        build_type2.build_type.add(build_type_name)

    def test_listing_devices(self):
        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user),
                                content_type='application/json')

        header = b'Bearer ' + json.loads(auth.content)['access'].encode()
        url = reverse('list-devices', kwargs={'version': 'v1'})
        response = self.client.get(url, content_type='application/json',
                                   HTTP_AUTHORIZATION=header)

        # Note that Orange Pi doesn't appear in the following list because the
        # device is not active.

        expected = [{
            "id": 1,
            "name": "Raspberry Pi",
            "generation": "3",
            "model": "Model B",
            "os": [
                {
                    "id": 1,
                    "name": "Debian",
                    "codename": "Buster",
                    "version": "10",
                    "port": "armhf",
                    "build_type": ["Classic image"]
                }, {
                    "id": 2,
                    "name": "Ubuntu",
                    "codename": "Bionic Beaver",
                    "version": "18.04",
                    "port": "armhf",
                    "build_type": ["Classic image"]
                }
            ]
        }]

        self.assertEqual(json.loads(response.content), expected)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listing_devices_unauthorized(self):
        url = reverse('list-devices', kwargs={'version': 'v1'})
        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
