#!/usr/bin/python3
"""class User that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from hashlib import md5
from flask_login import UserMixin

class User(UserMixin, BaseModel, Base):
    """Class User with:
    email, password, first_name, last_name
    class attributes in it
    """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(255), nullable=False)
        password = Column(String(255), nullable=False)
        first_name = Column(String(255), nullable=False)
        last_name = Column(String(255), nullable=False)
        expenses = relationship("Expense", backref="user")
        budgets = relationship("Budget", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
