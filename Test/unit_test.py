import unittest
from models.models import User, Role



class TestUser(unittest.TestCase):
    user = User(username="username", first_name="firstname", last_name="lastname", email="email@gmail.com",
                phone="123456789293", password="1234abcd", role=Role.admin)

    def test_password(self):
        with self.assertRaises(ValueError) as exeption:
            self.user.password="abc"
        self.assertEqual(str(exeption.exception), "This is not password(8 characters long+, one letter and number")

    def test_username(self):
        with self.assertRaises(ValueError) as exeption:
            self.user.username = "abc"
        self.assertEqual(str(exeption.exception), "Length of username should be less than 30 and more than 5 characters long")

    def test_email(self):
        with self.assertRaises(ValueError) as exeption:
            self.user.email = "abc"
        self.assertEqual(str(exeption.exception), "This is not email")

    def test_phone(self):
        with self.assertRaises(ValueError) as exeption:
            self.user.phone = "abc"
        self.assertEqual(str(exeption.exception), "This is not a phone number")

    def test_first_name(self):
        with self.assertRaises(ValueError) as exeption:
            self.user.first_name = "abc"
        self.assertEqual(str(exeption.exception), "Length of name should be less than 40 and more than 4 characters long")
