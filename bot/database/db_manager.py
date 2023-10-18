from sqlalchemy.ext.asyncio import AsyncSession, \
    create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from bot.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base: DeclarativeMeta = declarative_base()


class Database:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True)

    async def get_session(self) -> AsyncSession:
        async_session = async_sessionmaker(bind=self.engine, class_=AsyncSession)
        return async_session()

    async def create_db_and_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db_connect = Database(DATABASE_URL)
