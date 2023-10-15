from sqlalchemy.ext.asyncio import AsyncSession, \
    create_async_engine, async_sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///./db.db"


class Database:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True)

    async def get_session(self) -> AsyncSession:
        async_session = async_sessionmaker(bind=self.engine, class_=AsyncSession)
        return async_session()


db_connect = Database(DATABASE_URL)


