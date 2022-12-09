import base64
import unittest
from models import models
from app import app


class TestCase(unittest.TestCase):
    Api_URL = "http://127.0.0.1:5000/api/v1"
    Event_URL = "{}/event".format(Api_URL)
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
    Ticket_OBJ = {
        "event_id": '999999',
        "user_id": '3',
        "status": 'booked',
        "seat": '4'
    }

    auth = ('Admin', '1111abcd')

    def setUp(self):
        self.__test = app.test_client(self)

    def test_0_get_event(self):
        reques = self.__test.get("{}?{}={}".format(TestCase.Event_URL, "event", ""), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 404)

    def test_1_get_event_error(self):
        reques = self.__test.get("{}?{}={}".format(TestCase.Event_URL, "", ""), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_get_event_not_auth(self):
        reques = self.__test.get("{}?{}={}".format(TestCase.Event_URL, "", ""))
        self.assertEqual(reques.status_code, 401)

    def test_1_post_event_empty_json(self):
        reques = self.__test.post(TestCase.Event_URL, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_put_without_event_id(self):
        reques = self.__test.put(TestCase.Event_URL, json="", auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_post_validate_ticket_seat(self):
        Ticket_OBJ = {
            "event_id": '2',
            "user_id": '3',
            "status": 'booked',
            "seat": '9999'
        }
        reques = self.__test.post(TestCase.Ticket_URL, json=Ticket_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_put_without_json(self):
        reques = self.__test.put(TestCase.Event_URL, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_put_invalid_json(self):
        reques = self.__test.put(TestCase.Event_URL, json={"id": "saf"}, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_put_invalid_input_event(self):
        reques = self.__test.put(TestCase.Event_URL, json={"id": "mmmmmm"}, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_1_post_invalid_input_event(self):
        reques = self.__test.post(TestCase.Event_URL, json={"id": "mmmmmm"}, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_3_post_ticket_empty_json(self):
        reques = self.__test.post(TestCase.Ticket_URL, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_3_post_ticket_id_not_exist(self):
        reques = self.__test.post(TestCase.Ticket_URL, json=TestCase.Ticket_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_3_post_ticket_seat_not_exist(self):
        Ticket_OBJ = {
            "event_id": '2',
            "user_id": '3',
            "status": 'booked',
            "seat": '4'
        }
        reques = self.__test.post(TestCase.Ticket_URL, json=Ticket_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_4_post_ticket_seat_not_exist(self):
        Ticket_OBJ = {
            "event_id": '2',
            "user_id": '3',
            "status": 'booked',
        }
        reques = self.__test.post(TestCase.Ticket_URL, json=Ticket_OBJ, auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_2_bad_url(self):
        reques = self.__test.get("{}?{}={}".format("", "", ""), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_7_get_event(self):
        reques = self.__test.get("{}/{}".format(TestCase.Event_URL, "9999"), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 404)

    def test_8_del_event(self):
        reques = self.__test.delete("{}/{}".format(TestCase.Event_URL, "9999"), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)

    def test_8_del_event_bad_id(self):
        reques = self.__test.delete("{}/{}".format(TestCase.Event_URL, "daf"), auth=TestCase.auth)
        self.assertEqual(reques.status_code, 400)
