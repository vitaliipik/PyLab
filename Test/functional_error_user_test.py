import base64
import unittest
from models import models
from app import app
from flask import jsonify


class TestCase(unittest.TestCase):

    Api_URL = "http://127.0.0.1:5000/api/v1"
    Event_URL = "{}/event".format(Api_URL)
    User_URL = "{}/user".format(Api_URL)
    Login_OBJ = {
        "username": "Admin",
        "password": '1111adcd'
    }
    auth=('Admin','1111abcd')

    def setUp(self):
        self.__test = app.test_client(self)

    def test_1_post_validate_email(self):
        User_OBJ = {
            "first_name": "stjhg",
            "last_name": "therh",
            "username": "fsfasg",
            "email": "st3453m",
            "password": "1111abfcd",
            "phone": "223453722102",
            "role": "admin"

        }
        reques = self.__test.post(TestCase.User_URL, json=User_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400) # add assertion here

    def test_1_post_validate_password(self):
        User_OBJ = {
            "first_name": "stjhg",
            "last_name": "1",
            "username":"fsfasg",
            "email": "strys@email.com",
            "password": "1",
            "phone": "223453722102",
            "role": "admin"

        }
        reques = self.__test.post(TestCase.User_URL,json=User_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_post_validate_username(self):
        User_OBJ = {
            "first_name": "stjhg",
            "last_name": "1",
            "username":"1",
            "email": "strys@email.com",
            "password": "1asf3fsd4g4",
            "phone": "223453722102",
            "role": "admin"

        }
        reques = self.__test.post(TestCase.User_URL,json=User_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)


    def test_1_post_validate_phone(self):
        User_OBJ = {
            "first_name": "stjhg",
            "last_name": "wqrqfg",
            "username":"fsfasg",
            "email": "strys@email.com",
            "password": "1fs3gsdgh4",
            "phone": "22345",
            "role": "admin"

        }
        reques = self.__test.post(TestCase.User_URL,json=User_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_post_user_empty_json(self):
        reques = self.__test.post(TestCase.User_URL, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_bad_post_user(self):
        User_OBJ = {
            "id": "fsafsA",
            "first_name": "strey",
            "last_name": "Jas",
            "email": "stry@email.com",
            "password": "1111abfcd",
            "phone": "223453722102",
            "role": "admin"

        }
        reques = self.__test.post(TestCase.User_URL, json=User_OBJ,auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)
    def test_1_put_without_user_id(self):
        reques = self.__test.put(TestCase.User_URL, json="", auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_put_invalid_input_user(self):
        reques = self.__test.post(TestCase.User_URL, json={"id": "mmmmmm"}, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_2_put_invalid_input_user(self):
        reques = self.__test.post(TestCase.User_URL, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_2_put_invalid_auth_user(self):
        User_OBJ = {

            "first_name": "strey",
            "last_name": "Jas",
            "username":"TheUser",
            "email": "stry@email.com",
            "password": "1111abfcd",
            "phone": "223453722102",
            "role": "user"

        }
        reques = self.__test.put(TestCase.User_URL, json=User_OBJ,auth=("strey","1111abcd"))
        self.assertEqual(reques.json['message'], "Not enough rights to update user")


    def test_2_get_invalid_json_login(self):
        reques = self.__test.post(TestCase.User_URL+'/login', json={"id": "mmmmmm"}, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_get_empty_json_login(self):
        reques = self.__test.get(TestCase.User_URL+'/login', auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_get_invalid_request_body_login(self):
        reques = self.__test.get(TestCase.User_URL+'/login',json=TestCase.auth,auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_get_invalid_json_login(self):
        reques = self.__test.get(TestCase.User_URL+'/login',json=TestCase.Login_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 404)




if __name__ == '__main__':
    unittest.main()
