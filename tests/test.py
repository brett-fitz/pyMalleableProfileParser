from mpp.profile import MalleableProfile
import unittest

path = __file__[:-7]


class TestMalleableProfileParser(unittest.TestCase):
    amazon = MalleableProfile(f'{path}amazon.profile')

    def test_amazon_profile_option(self):
        self.assertEqual(self.amazon.jitter.value, '0')

    def test_amazon_profile_statement(self):
        self.assertEqual(self.amazon.http_get.client.Host.value, 'www.amazon.com')

    def test_amazon_profile_validation(self):
        self.assertTrue(isinstance(self.amazon.validate(), bool))

    bing_maps = MalleableProfile(f'{path}bing_maps.profile')

    def test_bing_maps_profile_option(self):
        self.assertEqual(bing_maps.sleeptime.value, '38500')

    def test_bing_maps_profile_statement(self):
        self.assertEqual(self.bing_maps.http_get.client.metadata.base64.value, '')

    def test_bing_maps_profile_validation(self):
        self.assertTrue(bing_maps.validate())

    mayo_clinic = MalleableProfile(f'{path}mayoclinic.profile')

    def test_mayo_clinic_profile_option(self):
        self.assertEqual(
            self.mayo_clinic.useragent.value,
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        )

    def test_mayo_clinic_profile_statement(self):
        self.assertEqual(self.mayo_clinic.stage.transform_x86.ReflectiveLoader.replace,'')

    def test_mayo_clinic_profile_validation(self):
        self.assertTrue(isinstance(self.mayo_clinic.validate(), list))
