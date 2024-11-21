from sqlalchemy import Column, String, Integer, Float, Date
from database import OrmBase

class ValidatorStake(OrmBase):
    __tablename__ = "validator_stakes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    validator_key = Column(String, nullable=False)
    actual_stake = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
