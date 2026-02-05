#!/usr/bin/python3
""" Unit tests for User model """
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """ Tests for User class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        new = self.value()
        self.assertEqual(type(new.password), str)

    def test_inheritance(self):
        """ User should inherit from BaseModel """
        new = self.value()
        self.assertTrue(hasattr(new, "id"))
        self.assertTrue(hasattr(new, "created_at"))
        self.assertTrue(hasattr(new, "updated_at"))

    def test_to_dict_contains_keys(self):
        """ to_dict should include expected keys """
        new = self.value()
        d = new.to_dict()
        self.assertIn("id", d)
        self.assertIn("created_at", d)
        self.assertIn("updated_at", d)
        self.assertIn("__class__", d)