from django.test import TestCase
from django.urls import reverse

from accounts.models import MyUser
from accounts.views import api_response

# Create your tests here.

class AccountsViewTests(TestCase):
    """测试accounts模块的视图"""
    def setUp(self):
        self.base_inviter = MyUser.objects.create(username="admin")
        self.register_url = reverse('accounts:register')

    def test_register_user(self):
        data = {'username': 'tmp'}
        response = self.client.post(self.register_url, data=data, content_type='application/json')
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['code'], 201)

        u = MyUser.objects.all().latest('id')
        self.assertEqual(u.username, data['username'])
        self.assertEqual(u.invitedby, 0)
    
    def test_register_user_by_inviter(self):
        data = {'username': 'tmp', 'invite': self.base_inviter.invite}
        response = self.client.post(self.register_url, data=data, content_type='application/json')
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['code'], 201)

        u = MyUser.objects.all().latest('id')
        self.assertEqual(u.username, data['username'])
        self.assertEqual(u.invitedby, self.base_inviter.pk)
    
    def test_register_user_with_invalid_data(self):
        data = {'inv': "xxx"}
        response = self.client.post(self.register_url, data=data, content_type='application/json')
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['code'], 400)


class ToolsTests(TestCase):
    """测试工具函数"""

    def test_api_response_with_message_and_result(self):
        ret = api_response(200, "OK", {"name": "张三", "age": 18})
        self.assertEqual(ret["code"], 200)
        self.assertEqual(ret["status"], "success")
        self.assertEqual(ret["message"], "OK")
        self.assertEqual(ret["result"], {"name": "张三", "age": 18})

    def test_api_response_with_only_code(self):
        ret = api_response(200)
        self.assertEqual(ret["code"], 200)
        self.assertEqual(ret["status"], "success")
        self.assertEqual(ret["message"], "")
        self.assertEqual(ret["result"], {})

        ret = api_response(301)
        self.assertEqual(ret["code"], 301)
        self.assertEqual(ret["status"], "success")
        self.assertEqual(ret["message"], "")
        self.assertEqual(ret["result"], {})

        ret = api_response(400)
        self.assertEqual(ret["code"], 400)
        self.assertEqual(ret["status"], "error")
        self.assertEqual(ret["message"], "")
        self.assertEqual(ret["result"], {})

        ret = api_response(404)
        self.assertEqual(ret["code"], 404)
        self.assertEqual(ret["status"], "error")
        self.assertEqual(ret["message"], "")
        self.assertEqual(ret["result"], {})

        ret = api_response(500, "")
        self.assertEqual(ret["code"], 500)
        self.assertEqual(ret["status"], "fail")
        self.assertEqual(ret["message"], "")
        self.assertEqual(ret["result"], {})

    def test_api_response_with_message(self):
        ret = api_response(200, "OK")
        self.assertEqual(ret["code"], 200)
        self.assertEqual(ret["status"], "success")
        self.assertEqual(ret["message"], "OK")
        self.assertEqual(ret["result"], {})

    def test_api_response_with_custome_code(self):
        ret = api_response(999, "自定义返回码")
        self.assertEqual(ret["code"], 999)
        self.assertEqual(ret["status"], "success")
        self.assertEqual(ret["message"], "自定义返回码")
        self.assertEqual(ret["result"], {})

    def test_api_response_with_nothing(self):
        ret = api_response()
        self.assertEqual(ret["code"], 200)
        self.assertEqual(ret["status"], "success")
        self.assertEqual(ret["message"], "")
        self.assertEqual(ret["result"], {})