from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from dishka import Provider, provide, Scope

from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.database.dao.subscribed_groups_dao import SubscribedGroupsDAO
from timetableforwarder.utils.get_config import load_config, Config


config: Config = load_config()
DB_URL = config.database_url


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self) -> AsyncEngine:
        return create_async_engine(DB_URL)

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with factory() as session:
            yield session


class DAOProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_users_dao(self, session: AsyncSession) -> UsersDAO:
        return UsersDAO(session)

    @provide(scope=Scope.REQUEST)
    def get_subscribed_groups_dao(self, session: AsyncSession) -> SubscribedGroupsDAO:
        return SubscribedGroupsDAO(session)