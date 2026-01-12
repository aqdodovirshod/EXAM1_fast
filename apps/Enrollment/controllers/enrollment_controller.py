from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Enrollment.services.enrollment_service import EnrollmentService
from apps.Enrollment.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentOut

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])
service = EnrollmentService()


@router.post("/", response_model=EnrollmentOut)
async def create_enrollment(data: EnrollmentCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_enrollment(data, session)


@router.get("/", response_model=list[EnrollmentOut])
async def get_enrollments(session: AsyncSession = Depends(get_session)):
    return await service.get_enrollments(session)


@router.get("/{enrollment_id}", response_model=EnrollmentOut)
async def get_enrollment(enrollment_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_enrollment(enrollment_id, session)


@router.put("/{enrollment_id}", response_model=EnrollmentOut)
async def update_enrollment(enrollment_id: int, data: EnrollmentUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_enrollment(enrollment_id, data, session)


@router.delete("/{enrollment_id}")
async def delete_enrollment(enrollment_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_enrollment(enrollment_id, session)
    return {"detail": "Enrollment deleted successfully"}