from uiassignment.db import Base
from sqlalchemy import Column, String, TIMESTAMP, Integer, Numeric


class UserModel(Base):
    __tablename__ = "users"

    acct = Column(String, primary_key=True, nullable=False)
    pwd = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __init__(self, acct, pwd, fullname, created_at, updated_at):
        self.acct = acct
        self.pwd = pwd
        self.fullname = fullname
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self):
        d = {"acct": self.acct, "pwd": self.pwd, "fullname": self.fullname}

        if self.created_at:
            d["created_at"] = self.created_at
        if self.updated_at:
            d["updated_at"] = self.updated_at

        return d
