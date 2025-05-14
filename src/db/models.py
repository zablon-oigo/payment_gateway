from sqlalchemy import Column, Integer, String, BigInteger, Date
from datetime import date
from db.base_class import Base

class Payment(Base):
    number = Column(BigInteger, nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_id = Column(String(100), nullable=False)
    created_at = Column(Date, default=date.today, nullable=False) 
