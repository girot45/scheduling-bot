from sqlalchemy import Column, String, Integer, Date, BIGINT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    tgid = Column(BIGINT, primary_key=True, index=True)
    username = Column(String(length=255))
    need_notif = Column(Integer, default=1)


class Table(Base):
    __tablename__ = "Table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tgid = Column(BIGINT)
    day_of_week = Column(String(length=15))
    date = Column(Date)
    timestart = Column(String(length=5), nullable=True)
    timeend = Column(String(length=5), nullable=True)
    event = Column(String)
    isrepeat = Column(Integer, default=0)
