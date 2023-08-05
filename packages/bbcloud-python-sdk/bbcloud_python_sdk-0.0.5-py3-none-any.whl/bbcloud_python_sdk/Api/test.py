import logging
import unittest

from bbcloud_python_sdk.Api import BBCloud
from bbcloud_python_sdk.Api.Models.SDK import SDK
from bbcloud_python_sdk.Api.Models.User import User

logging.getLogger().setLevel(logging.INFO)

BBCloud.config(
    host='xxx',
    token='xxx'
)


class MyTestCase(unittest.TestCase):

    def test_create(self):
        sdk = SDK({
            'name': '测试SDK',
            'key': 'TestKey',
            'url': 'https://testing-v3.bbcloud.babybus.com/business/sdk/ios',
            'mainstay': 'Test',
            'purpose': '用于测试',
            'access': '测试的',
            'detail': '测试的',
            'platforms_id': 1
        }).create()
        self.assertEqual(sdk.name, '测试SDK')

    def test_get(self):
        users = User().page(1).page_size(10).get()
        self.assertEqual(len(users), 10)

    def test_find(self):
        sdk = SDK().where('name', '测试SDK').first()
        self.assertEqual(sdk.name, '测试SDK')

    def test_delete(self):
        sdk = SDK().where('name', '测试SDK').first()
        self.assertEqual(sdk.delete(), True)

    def test_delete_all(self):
        res = SDK().where('id', '>=', 72).where('id', '<=', '78').delete()
        self.assertEqual(res, True)

    def test_change(self):
        sdk = SDK().find(78)
        sdk.name = '修改SDK名字测试3'
        sdk.save()
        sdk2 = SDK().find(78)
        self.assertEqual(sdk2.name, '修改SDK名字测试3')


if __name__ == '__main__':
    unittest.main()
