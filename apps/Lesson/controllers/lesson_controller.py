from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Lesson.services.lesson_service import LessonService
from apps.Lesson.schemas.lesson import LessonCreate, LessonUpdate, LessonOut
from apps.User.services.permission import teacher_or_admin_required, admin_required

router = APIRouter(prefix="/lessons", tags=["Lessons"])
service = LessonService()


@router.post("/", response_model=LessonOut, dependencies=[Depends(teacher_or_admin_required)])
async def create_lesson(data: LessonCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_lesson(data, session)


@router.get("/", response_model=list[LessonOut])
async def get_lessons(session: AsyncSession = Depends(get_session)):
    return await service.get_lessons(session)


@router.get("/{lesson_id}", response_model=LessonOut)
async def get_lesson(lesson_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_lesson(lesson_id, session)


@router.put("/{lesson_id}", response_model=LessonOut, dependencies=[Depends(teacher_or_admin_required)])
async def update_lesson(lesson_id: int, data: LessonUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_lesson(lesson_id, data, session)


@router.delete("/{lesson_id}", dependencies=[Depends(admin_required)])
async def delete_lesson(lesson_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_lesson(lesson_id, session)
    return {"detail": "Lesson deleted successfully"}