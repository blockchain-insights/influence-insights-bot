from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from database import OrmBase

class DelegatorStake(OrmBase):
    __tablename__ = "delegator_stakes"

    delegator_key = Column(String, primary_key=True, nullable=False)
    actual_stake = Column(Float, nullable=False)

    # Relationship to DelegatorWeightAllocation
    allocations = relationship("DelegatorWeightAllocation", back_populates="stake")
