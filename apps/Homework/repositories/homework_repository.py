from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Homework.models.homework import Homework

class HomeworkRepository:
    async def create(self, data: dict, session: AsyncSession):
        homework = Homework(**data)
        session.add(homework)
        await session.commit()
        await session.refresh(homework)
        return homework

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Homework).options(
                selectinload(Homework.lesson),
                selectinload(Homework.results),
            )
        )
        return result.scalars().all()

    async def get_by_id(self, homework_id: int, session: AsyncSession):
        return await session.get(
            Homework,
            homework_id,
            options=[
                selectinload(Homework.lesson),
                selectinload(Homework.results),
            ]
        )

    async def update(self, homework_id: int, data: dict, session: AsyncSession):
        homework = await self.get_by_id(homework_id, session)
        if not homework:
            return None

        for key, value in data.items():
            if value is not None and hasattr(homework, key):
                if key == "lesson_id":
                    continue
                setattr(homework, key, value)

        await session.commit()
        await session.refresh(homework)
        return homework

    async def delete(self, homework_id: int, session: AsyncSession):
        homework = await self.get_by_id(homework_id, session)
        if not homework:
            return None
        await session.delete(homework)
        await session.commit()
        return homework