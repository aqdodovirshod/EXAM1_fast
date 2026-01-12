from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_session
from apps.Student.services.student_service import StudentService
from apps.Student.schemas.student import StudentCreate, StudentUpdate, StudentOut

router = APIRouter(prefix="/students", tags=["Students"])
service = StudentService()

@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
async def create_student(data: StudentCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_student(data, session)

@router.get("/", response_model=list[StudentOut])
async def get_students(session: AsyncSession = Depends(get_session)):
    return await service.get_students(session)

@router.get("/{student_id}", response_model=StudentOut)
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_student(student_id, session)

@router.put("/{student_id}", response_model=StudentOut)
async def update_student(student_id: int, data: StudentUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_student(student_id, data.dict(exclude_unset=True), session)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_student(student_id, session)
    return {"detail": "Student deleted successfully"}