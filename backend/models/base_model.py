#!/usr/bin/python3

"""
    Base class that defines common attributes/methods
    for other classes.
"""
from datetime import datetime
import models
import uuid
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    """
        Definition of Basemodel class.
    """
    if models.storage_t == "db":
        id = Column(String(255), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)


    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """
            Prints a string representation of the
            class name, id, and dictionary.
        """
        return("[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__))

    def save(self):
        """
            Updates the public instance attribute
            `updated_at` with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
            Returns a dictionary containing all keys/values
            of __dict__ of the instance.
        """
        myDict = dict(self.__dict__)
        myDict["__class__"] = self.__class__.__name__
        myDict["created_at"] = self.created_at.isoformat()
        myDict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in myDict:
            del myDict["_sa_instance_state"]
        return myDict

    def delete(self):
        """Del the current instance from DB storage"""
        models.storage.delete(self)
