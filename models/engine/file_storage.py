#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns all objects in storage.
        If cls is provided, returns only objects of that class.
        cls can be a class object or a string name of the class.
        """
        if cls is None:
            return FileStorage.__objects

        if isinstance(cls, str):
            return [obj for obj in FileStorage.__objects.values()
                    if obj.__class__.__name__ == cls]
        else:
            return [obj for obj in FileStorage.__objects.values()
                    if isinstance(obj, cls)]

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {key: val.to_dict() for key, val in FileStorage.__objects.items()}
            json.dump(temp, f)

    def delete(self, obj=None):
        """Deletes obj from storage if it exists"""
        if obj is None:
            return
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }

        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls_name = val['__class__']
                    if cls_name in classes:
                        FileStorage.__objects[key] = classes[cls_name](**val)
        except FileNotFoundError:
            pass