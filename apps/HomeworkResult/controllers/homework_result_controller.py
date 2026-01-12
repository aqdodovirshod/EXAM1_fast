from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.HomeworkResult.services.homework_result_service import HomeworkResultService
from apps.HomeworkResult.schemas.homework_result import HomeworkResultCreate, HomeworkResultUpdate, HomeworkResultOut
from apps.User.services.permission import teacher_or_admin_required

router = APIRouter(prefix="/homework-results", tags=["HomeworkResults"])
service = HomeworkResultService()


@router.post("/", response_model=HomeworkResultOut, dependencies=[Depends(teacher_or_admin_required)])
async def create_homework_result(data: HomeworkResultCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_homework_result(data, session)


@router.get("/", response_model=list[HomeworkResultOut])
async def get_homework_results(session: AsyncSession = Depends(get_session)):
    return await service.get_homework_results(session)


@router.get("/{result_id}", response_model=HomeworkResultOut)
async def get_homework_result(result_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_homework_result(result_id, session)


@router.put("/{result_id}", response_model=HomeworkResultOut, dependencies=[Depends(teacher_or_admin_required)])
async def update_homework_result(result_id: int, data: HomeworkResultUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_homework_result(result_id, data, session)


@router.delete("/{result_id}", dependencies=[Depends(teacher_or_admin_required)])
async def delete_homework_result(result_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_homework_result(result_id, session)
    return {"detail": "Homework result deleted successfully"}