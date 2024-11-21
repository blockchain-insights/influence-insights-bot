from sqlalchemy import Integer, Column, String
from database import OrmBase


class Subnet(OrmBase):
    __tablename__ = "subnets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subnet_id = Column(Integer, nullable=False)
    subnet_name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False, default=0)