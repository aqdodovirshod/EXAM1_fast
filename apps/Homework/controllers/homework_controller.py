from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Homework.services.homework_service import HomeworkService
from apps.Homework.schemas.homework import HomeworkCreate, HomeworkUpdate, HomeworkOut
from apps.User.services.permission import teacher_or_admin_required

router = APIRouter(prefix="/homeworks", tags=["Homeworks"])
service = HomeworkService()


@router.post("/", response_model=HomeworkOut, dependencies=[Depends(teacher_or_admin_required)])
async def create_homework(data: HomeworkCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_homework(data, session)


@router.get("/", response_model=list[HomeworkOut])
async def get_homeworks(session: AsyncSession = Depends(get_session)):
    return await service.get_homeworks(session)


@router.get("/{homework_id}", response_model=HomeworkOut)
async def get_homework(homework_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_homework(homework_id, session)


@router.put("/{homework_id}", response_model=HomeworkOut, dependencies=[Depends(teacher_or_admin_required)])
async def update_homework(homework_id: int, data: HomeworkUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_homework(homework_id, data, session)


@router.delete("/{homework_id}", dependencies=[Depends(teacher_or_admin_required)])
async def delete_homework(homework_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_homework(homework_id, session)
    return {"detail": "Homework deleted successfully"}