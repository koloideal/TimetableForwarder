from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from timetableforwarder.database.database_models import User

class UsersDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        is_subscribed: bool = False,
        subscribed_group: Optional[int] = None,
    ) -> User:
        new_user = User(
            user_id=user_id,
            username=username,
            is_subscribed=is_subscribed,
            subscribed_group=subscribed_group,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(**kwargs)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()
        
    async def ban_user(self, user_id: int) -> Optional[User]:
        return await self.update_user(user_id=user_id, is_banned=True)

    async def unban_user(self, user_id: int) -> Optional[User]:
        return await self.update_user(user_id=user_id, is_banned=False)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False

