from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Student(Base):
    
    __tablename__ = "student"
    
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    age = Column(Integer)