from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class CustomImages(Base):
    __tablename__ = "custom_images"

    placeid = Column(String, unique=True, primary_key=True, index = True) 
    photoref = Column(String)
    n_requests = Column(BigInteger, index = True)
    update_timestamp = Column(DateTime)
    photo_url = Column(String)