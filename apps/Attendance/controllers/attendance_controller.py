from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Attendance.services.attendance_service import AttendanceService
from apps.Attendance.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceOut

router = APIRouter(prefix="/attendances", tags=["Attendance"])  
service = AttendanceService()


@router.post("/", response_model=AttendanceOut)
async def create_attendance(data: AttendanceCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_attendance(data, session)


@router.get("/", response_model=list[AttendanceOut])
async def get_attendances(session: AsyncSession = Depends(get_session)):
    return await service.get_attendances(session)


@router.get("/{attendance_id}", response_model=AttendanceOut)
async def get_attendance(attendance_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_attendance(attendance_id, session)


@router.put("/{attendance_id}", response_model=AttendanceOut)
async def update_attendance(attendance_id: int, data: AttendanceUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_attendance(attendance_id, data, session)


@router.delete("/{attendance_id}")
async def delete_attendance(attendance_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_attendance(attendance_id, session)
    return {"detail": "Attendance deleted successfully"}