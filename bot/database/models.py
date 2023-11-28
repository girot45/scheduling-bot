from sqlalchemy import MetaData, Table, Date, Column, Integer, \
    String, ForeignKey


metadata = MetaData()

user = Table(
    "User",
    metadata,
    Column("tgid", Integer, primary_key=True),
    Column("username", String(length=255)),
    Column("need_notif", Integer, server_default="1"),
)

table = Table(
    "Table",
    metadata,

    Column("id", Integer, primary_key=True, index=True,
           autoincrement=True),
    Column("tgid", Integer, ForeignKey(user.c.tgid,
                                       onupdate="cascade",
                                       ondelete="cascade")),
    Column("day_of_week", String(length=15)),
    Column("date", Date, nullable=False),
    Column("timestart", String(length=5), nullable=True),
    Column("timeend", String(length=5), nullable=True),
    Column("event", String, nullable=False),
    Column("isrepeat", Integer, server_default="0", nullable=False),
)




