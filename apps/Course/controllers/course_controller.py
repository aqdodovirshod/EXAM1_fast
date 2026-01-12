from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Course.services.course_service import CourseService
from apps.Course.schemas.course import CourseCreate, CourseUpdate, CourseOut

router = APIRouter(prefix="/courses", tags=["Courses"])
service = CourseService()


@router.post("/", response_model=CourseOut)
async def create_course(data: CourseCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_course(data, session)


@router.get("/", response_model=list[CourseOut])
async def get_courses(session: AsyncSession = Depends(get_session)):
    return await service.get_courses(session)


@router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_course(course_id, session)


@router.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, data: CourseUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_course(course_id, data, session)


@router.delete("/{course_id}")
async def delete_course(course_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_course(course_id, session)
    return {"detail": "Course deleted successfully"}