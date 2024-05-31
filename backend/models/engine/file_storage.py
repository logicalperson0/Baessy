#!/usr/bin/python3
"""Class that serializes instances to a JSON file
and deserializes JSON file to instances
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.expense import Expense
from models.budget import Budget
from models.tag import Tag
from models.transaction import Transaction
from models.catagory import Catagory

#from models.state import State
#from models.city import City
#from models.amenity import Amenity


class FileStorage:
    """Class that serializes and deserializes from a json file
    """
    __file_path = "budgetr.json"
    __objects = {}

    """dicts = {'BaseModel': BaseModel}"""

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    """
    def all(self):
        return (FileStorage.__objects)
    """

    def new(self, obj):
        """sets in __objects the obj with key"""
        obj_key = obj.__class__.__name__ + '.' + obj.id

        FileStorage.__objects[obj_key] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        dicts = {}

        for k, v in self.__objects.items():
            dicts[k] = v.to_dict()

        with open(FileStorage.__file_path, "w") as to_file:
            json.dump(dicts, to_file)

    def reload(self):
        """deserializes the JSON file to __objects if it exists"""
        """from models.base_model import BaseModel"""

        dicts = {'BaseModel': BaseModel, 'User': User, 'Tag': Tag,
                   'Catagory':Catagory, 'Expense': Expense,
                   'Budget': Budget, 'Transaction': Transaction}
        """
        dicts = {'BaseModel': BaseModel, 'User': User,
                 'ExpenseT': ExpenseT, 'BudgetT': BudgetT}
        """

        if os.path.exists(self.__file_path) is True:
            with open(self.__file_path, "r") as from_file:
                js = json.load(from_file)
                for k, v in js.items():
                    self.__objects[k] = dicts[v["__class__"]](**v)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
