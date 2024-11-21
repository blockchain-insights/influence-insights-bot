from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import OrmBase

class DelegatorWeightAllocation(OrmBase):
    __tablename__ = "delegator_weight_allocations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    delegator_key = Column(String, ForeignKey("delegator_stakes.delegator_key", use_alter=True), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    subnet_id = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('weight >= 1 AND weight <= 100', name='weight_range_check'),
    )

    # Relationship back to DelegatorStake
    stake = relationship("DelegatorStake", back_populates="allocations", lazy="joined")
