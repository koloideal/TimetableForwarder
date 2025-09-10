from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from timetableforwarder.database.database_models import SubscribedGroup


class SubscribedGroupsDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_group(self, group_id: int, subscribed_group_id: int) -> None:
        stmt = pg_insert(SubscribedGroup).values(
            group_id=group_id,
            subscribed_group=subscribed_group_id
        ).on_conflict_do_update(
            index_elements=['group_id'],
            set_=dict(subscribed_group=subscribed_group_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def remove_group(self, group_id: int) -> bool:
        stmt = delete(SubscribedGroup).where(SubscribedGroup.group_id == group_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_group_by_telegram_id(self, group_id: int) -> Optional[SubscribedGroup]:
        query = select(SubscribedGroup).where(SubscribedGroup.group_id == group_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_groups_by_subscription(self, subscribed_group_id: int) -> List[SubscribedGroup]:
        query = select(SubscribedGroup).where(SubscribedGroup.subscribed_group == subscribed_group_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_all_groups(self) -> List[SubscribedGroup]:
        query = select(SubscribedGroup)
        result = await self.session.execute(query)
        return result.scalars().all()

