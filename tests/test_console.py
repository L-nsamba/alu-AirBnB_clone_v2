#!/usr/bin/python3
"""Tests for console create command"""
import unittest
from unittest.mock import patch
from io import StringIO
import os

from console import HBNBCommand
from models import storage
from models.user import User

class TestConsoleCreate(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        self.storage_file = "file.json"

        # Ensure clean storage
        try:
            os.remove(self.storage_file)
        except FileNotFoundError:
            pass

    def tearDown(self):
        """Clean up after test"""
        try:
            os.remove(self.storage_file)
        except FileNotFoundError:
            pass

    def test_create_with_string_param(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd(
                'create User name="My_little_house"'
            )
            obj_id = output.getvalue().strip()

        key = f"User.{obj_id}"
        self.assertIn(key, storage.all())

        obj = storage.all()[key]
        self.assertEqual(obj.name, "My little house")

    def test_create_with_int_and_float(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd(
                'create User age=25 height=1.75'
            )
            obj_id = output.getvalue().strip()

        obj = storage.all()[f"User.{obj_id}"]
        self.assertEqual(obj.age, 25)
        self.assertEqual(obj.height, 1.75)

    def test_create_with_invalid_params(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd(
                'create User name=House age=12.3.4'
            )
            obj_id = output.getvalue().strip()

        obj = storage.all()[f"User.{obj_id}"]
        self.assertFalse(hasattr(obj, "name"))
        self.assertFalse(hasattr(obj, "age"))

    def test_create_with_escaped_quotes(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd(
                'create User bio="I_love_\\\"Python\\\""'
            )
            obj_id = output.getvalue().strip()

        obj = storage.all()[f"User.{obj_id}"]
        self.assertEqual(obj.bio, 'I love "Python"')
