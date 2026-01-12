from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.HomeworkResult.models.homework_result import HomeworkResult

class HomeworkResultRepository:
    async def create(self, data: dict, session: AsyncSession):
        result_obj = HomeworkResult(**data)
        session.add(result_obj)
        await session.commit()
        await session.refresh(result_obj)
        return result_obj

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(HomeworkResult).options(
                selectinload(HomeworkResult.student),
                selectinload(HomeworkResult.homework),
            )
        )
        return result.scalars().all()

    async def get_by_id(self, result_id: int, session: AsyncSession):
        return await session.get(
            HomeworkResult,
            result_id,
            options=[
                selectinload(HomeworkResult.student),
                selectinload(HomeworkResult.homework),
            ]
        )

    async def update(self, result_id: int, data: dict, session: AsyncSession):
        result_obj = await self.get_by_id(result_id, session)
        if not result_obj:
            return None

        for key, value in data.items():
            if value is not None and hasattr(result_obj, key):
                if key in {"student_id", "homework_id"}:
                    continue
                setattr(result_obj, key, value)

        await session.commit()
        await session.refresh(result_obj)
        return result_obj

    async def delete(self, result_id: int, session: AsyncSession):
        result_obj = await self.get_by_id(result_id, session)
        if not result_obj:
            return None
        await session.delete(result_obj)
        await session.commit()
        return result_obj