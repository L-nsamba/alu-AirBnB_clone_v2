#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
from models import storage_type


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if storage_type == "db":
        # DBStorage: relationship with City
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete, delete-orphan"
        )
    else:
        # FileStorage: getter property
        @property
        def cities(self):
            """Return list of City instances with state_id equal to current State.id"""
            from models import storage
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list