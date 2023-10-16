from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    tgid = Column(Integer, primary_key=True, index=True)


class Table(Base):
    __tablename__ = "Table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tgid = Column(
        Integer,
        ForeignKey(
            "User.tgid",
            onupdate="CASCADE",
            ondelete="CASCADE"
        )
    )
    day_of_week = Column(String(length=15))
    date = Column(Date())
    timestart = Column(String(length=5))
    timeend = Column(String(length=5))
    event = Column(String)
    isrepeat = Column(Integer, default=0)
