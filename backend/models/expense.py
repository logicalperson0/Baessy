#!/usr/bin/python3
"""class User that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship

class Expense(BaseModel, Base):
    """Class Expense with:
    id, data, user_id, total_todate
    class attributes in it
    """
    if models.storage_t == 'db':
        __tablename__ = 'expenses'
        user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
        amount = Column(Integer)
        catagory = Column(String(255))
        location = Column(String(255))
        transactions = relationship("Transaction", backref="expense")
    else:
        # id = ""
        user_id = 0
        amount = 0
        catagory = ""
        location = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
