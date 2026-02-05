#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models


# Association table for Many-to-Many relationship between Place and Amenity
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"),
    primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
    primary_key=True, nullable=False)
)

class Place(BaseModel, Base):
    """A place to stay"""
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # DBStorage: relationship with Amenity
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        viewonly=False
    )

    # FileStorage: getter and setter for amenities
    @property
    def amenities(self):
        """Return list of Amenity instances linked to this Place"""
        from models.amenity import Amenity
        amenity_list = []
        for amenity in models.storage.all(Amenity).values():
            if amenity.id in self.amenity_ids:
                amenity_list.append(amenity)
        return amenity_list

    @amenities.setter
    def amenities(self, obj):
        """Add an Amenity.id to amenity_ids if obj is Amenity"""
        from models.amenity import Amenity
        if isinstance(obj, Amenity):
            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)



