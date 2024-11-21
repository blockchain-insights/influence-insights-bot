from sqlalchemy import Column, String, Integer, Date
from database import OrmBase

class DelegatorNumber(OrmBase):
    __tablename__ = "delegator_numbers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    validator_key = Column(String, nullable=False)
    delegator_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
