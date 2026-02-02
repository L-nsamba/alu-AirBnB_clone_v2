#!/usr/bin/python3
"""
Unittests for DBStorage engine
"""

import unittest
import MySQLdb
import os
from console import HBNBCommand


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DB storage only")
class TestDBStorage(unittest.TestCase):
    """Tests for DB storage engine using MySQLdb"""

    def setUp(self):
        """Connect to test DB before each test"""
        self.db = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        self.cursor = self.db.cursor()

    def tearDown(self):
        """Close DB connection after each test"""
        self.cursor.close()
        self.db.close()

    def count_rows(self, table):
        """Helper to count rows in a table"""
        self.cursor.execute(f"SELECT COUNT(*) FROM {table};")
        return self.cursor.fetchone()[0]

    def test_create_state(self):
        """Test that creating a State adds a row"""
        before = self.count_rows("states")
        HBNBCommand().onecmd('create State name="California"')
        after = self.count_rows("states")
        self.assertEqual(after, before + 1)

    def test_update_state(self):
        """Test that updating a State changes its name"""
        # Create a new state
        HBNBCommand().onecmd('create State name="Nevada"')
        self.cursor.execute("SELECT id FROM states WHERE name='Nevada';")
        state_id = self.cursor.fetchone()[0]

        # Update the state name
        HBNBCommand().onecmd(f'update State {state_id} name "SilverState"')

        # Verify update
        self.cursor.execute("SELECT name FROM states WHERE id=%s;", (state_id,))
        new_name = self.cursor.fetchone()[0]
        self.assertEqual(new_name, "SilverState")

    def test_delete_state(self):
        """Test that deleting a State removes a row"""
        # Create a new state
        HBNBCommand().onecmd('create State name="Texas"')
        before = self.count_rows("states")

        # Get its id
        self.cursor.execute("SELECT id FROM states WHERE name='Texas';")
        state_id = self.cursor.fetchone()[0]

        # Delete the state
        HBNBCommand().onecmd(f'destroy State {state_id}')

        after = self.count_rows("states")
        self.assertEqual(after, before - 1)

    def test_reload(self):
        """Test that reload repopulates objects from DB"""
        # Create a new state
        HBNBCommand().onecmd('create State name="Florida"')
        self.cursor.execute("SELECT id FROM states WHERE name='Florida';")
        state_id = self.cursor.fetchone()[0]

        # Close and reopen connection to simulate reload
        self.cursor.close()
        self.db.close()
        self.db = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        self.cursor = self.db.cursor()

        # Verify state still exists
        self.cursor.execute("SELECT name FROM states WHERE id=%s;", (state_id,))
        name = self.cursor.fetchone()[0]
        self.assertEqual(name, "Florida")
