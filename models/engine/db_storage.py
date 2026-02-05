#!/usr/bin/python3
"""DBStorage engine"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage:
    """Database storage engine"""

    __engine = None
    __session = None
    

    def __init__(self):
        """Initialize DBStorage"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
            pool_pre_ping=True
        )

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the database"""
        objects = {}
        classes = [User, State, City, Amenity, Place, Review]

        # Make sure session fetches latest from DB
        self.__session.expire_all()

        if cls:
            for obj in self.__session.query(cls).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        else:
            for cl in classes:
                for obj in self.__session.query(cl).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj

        return objects


    def new(self, obj):
        """Add obj to current session"""
        self.__session.add(obj)

    def save(self):
        """Commit current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session() 

