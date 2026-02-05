#!/usr/bin/python3
"""Create all tables in MySQL database for AirBnB"""
import os
from models.engine.db_storage import DBStorage

# Set environment variables
os.environ['HBNB_TYPE_STORAGE'] = 'db'
os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
os.environ['HBNB_MYSQL_HOST'] = 'localhost'
os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'
os.environ['HBNB_ENV'] = 'test'  # optional, drops tables first

# Initialize storage and create tables
storage = DBStorage()
storage.reload()

print("✅ Tables created successfully!")
