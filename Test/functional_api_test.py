import base64
import unittest
from models import models
from app import app




class TestCase(unittest.TestCase):
    Api_URL = "http://127.0.0.1:5000/api/v1"
    Event_URL = "{}/event".format(Api_URL)
    User_URL = "{}/user".format(Api_URL)
    Ticket_URL = "{}/ticket".format(Api_URL)
    TicketCancel_URL = "{}/cancelTicket".format(Api_URL)
    TicketUpdate_URL = "{}/updateTicket".format(Api_URL)
    Event_OBJ = {
        "id": "1",
        "name": "string",
        "date": "2022-11-20T13:44:48.149Z",
        "address": "evi",
        "tickets_count": "6"
    }
    auth = ("Admin","1111abcd")
    Login_OBJ = {
        "username": "TheUser",
        "password": '1111abcd'
    }
    User_OBJ = {
        "id": "200",
        "username": "stryi",
        "first_name": "strey",
        "last_name": "Jas",
        "email": "stry@email.com",
        "password": "1111abfcd",
        "phone": "223453722102",
        "role": "admin"

    }
    Ticket_OBJ = {
        "event_id": '2',
        "user_id": '3',
        "status": 'booked',
        "seat": '1'
    }
    Ticket_OBJ_Bad = {
        "id": "5",
        "event_id": "200",
        "user_id": "200",
        "seat": "3",
        "status": "booked"

    }


    def setUp(self):
        self.__test = app.test_client(self)
        
    def test_0_add_new_event(self):
        # tests = app.test_client(self)
        requests = self.__test.post(TestCase.Event_URL, json=TestCase.Event_OBJ, auth=TestCase.auth)
        self.assertEqual(requests.status_code, 200)

    def test_0_get_event(self):
        reques = self.__test.get("{}?{}={}".format(TestCase.Event_URL, "event", "string"), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_1_put_event(self):
        reques = self.__test.put(TestCase.Event_URL, auth=TestCase.auth, json=TestCase.Event_OBJ)
        self.assertEqual(reques.status_code, 200)

    def test_2_get_event(self):
        reques = self.__test.get("{}/{}".format(TestCase.Event_URL, 1), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_4_add_new_user(self):
        reques = self.__test.post(TestCase.User_URL, json=TestCase.User_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_5_add_new_ticket(self):
        reques = self.__test.post(TestCase.Ticket_URL, json=TestCase.Ticket_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_6_get_user_ticket(self):
        reques = self.__test.get("{}/{}/tickets".format(TestCase.User_URL, "stryi"), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_6_add_new_bad_ticket(self):
        reques = self.__test.post(TestCase.Ticket_URL, json=TestCase.Ticket_OBJ_Bad, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_7_get_user(self):
        reques = self.__test.get("{}/{}".format(TestCase.User_URL, "stryi"), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_7_put_user(self):
        reques = self.__test.put("{}".format(TestCase.User_URL), json=TestCase.User_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_8_delete_user(self):
        reques = self.__test.delete("{}/{}".format(TestCase.User_URL, "stryi"), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_7_update_ticket(self):
        reques = self.__test.put("{}/{}".format(TestCase.TicketUpdate_URL, 61), json={"status": "bought"},
                           auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_8_delete_ticket(self):
        reques = self.__test.delete("{}/{}".format(TestCase.TicketCancel_URL, 61), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_9_delete_event(self):
        reques = self.__test.delete("{}/{}".format(TestCase.Event_URL, 1), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 200)

    def test_10_login(self):
        reques = self.__test.get("{}/login".format(TestCase.User_URL), json=TestCase.Login_OBJ)
        self.assertEqual(reques.status_code, 200)
