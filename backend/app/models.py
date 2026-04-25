from sqlalchemy import Column, Integer, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(ARRAY(Float)) 