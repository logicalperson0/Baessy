#!/usr/bin/python3
"""class User that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

class Budget(BaseModel, Base):
    """Class Budget with:
    id, data, user_id
    class attributes in it
    """
    # id = ""
    if models.storage_t == 'db':
        __tablename__ = 'budgets'
        user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
        amount = Column(Integer, nullable=False)
        # budget_todate = Column(Integer, nullable=False, default=0)
    else:
        user_id = 0
        amount = 0
        # budget_todate = 0

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
