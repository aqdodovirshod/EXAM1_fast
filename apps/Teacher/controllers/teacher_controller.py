from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Teacher.services.teacher_service import TeacherService
from apps.Teacher.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherOut

router = APIRouter(prefix="/teachers", tags=["Teachers"])
service = TeacherService()

@router.post("/", response_model=TeacherOut)
async def create_teacher(data: TeacherCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_teacher(data, session)

@router.get("/", response_model=list[TeacherOut])
async def get_teachers(session: AsyncSession = Depends(get_session)):
    return await service.get_teachers(session)

@router.get("/{teacher_id}", response_model=TeacherOut)
async def get_teacher(teacher_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_teacher(teacher_id, session)

@router.put("/{teacher_id}", response_model=TeacherOut)
async def update_teacher(teacher_id: int, data: TeacherUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_teacher(teacher_id, data, session)

@router.delete("/{teacher_id}")
async def delete_teacher(teacher_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_teacher(teacher_id, session)
    return {"detail": "Teacher deleted successfully"}