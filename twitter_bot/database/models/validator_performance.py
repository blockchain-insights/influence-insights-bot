from sqlalchemy import Column, String, Integer, Float, DateTime
from database import OrmBase
from datetime import datetime

class ValidatorPerformance(OrmBase):
    __tablename__ = "validator_performance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    validator_key = Column(String, nullable=False)  # Validator's unique key
    stake = Column(Float, nullable=False)  # COMAI stake
    stake_usd = Column(Float, nullable=False)  # Stake value in USD
    daily_rewards = Column(Float, nullable=False)  # Daily rewards in COMAI
    daily_rewards_usd = Column(Float, nullable=False)  # Daily rewards in USD
    fee_percentage = Column(Float, nullable=False)  # Fee percentage
    subnet_registrations = Column(Integer, nullable=False)  # Number of subnet registrations
    delegator_count = Column(Integer, nullable=False)  # Number of delegators
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)  # DateTime for last update
