#!/usr/bin/python3
"""class User that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

class Catagory(BaseModel, Base):
    """Class Expense with:
    id, data, user_id, total_todate
    class attributes in it
    """
    if models.storage_t == 'db':
        __tablename__ = 'catagories'
        name = Column(String(255))
    else:
        # id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
