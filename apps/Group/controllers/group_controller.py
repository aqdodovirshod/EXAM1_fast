from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Group.services.group_service import GroupService
from apps.Group.schemas.group import GroupCreate, GroupUpdate, GroupOut
from apps.User.services.permission import teacher_or_admin_required,admin_required

router = APIRouter(prefix="/groups", tags=["Groups"])
service = GroupService()


@router.post("/", response_model=GroupOut, dependencies=[Depends(teacher_or_admin_required)])
async def create_group(data: GroupCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_group(data, session)


@router.get("/", response_model=list[GroupOut])
async def get_groups(session: AsyncSession = Depends(get_session)):
    return await service.get_groups(session)


@router.get("/{group_id}", response_model=GroupOut)
async def get_group(group_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_group(group_id, session)


@router.put("/{group_id}", response_model=GroupOut, dependencies=[Depends(teacher_or_admin_required)])
async def update_group(group_id: int, data: GroupUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_group(group_id, data, session)


@router.delete("/{group_id}", dependencies=[Depends(admin_required)])
async def delete_group(group_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_group(group_id, session)
    return {"detail": "Group deleted successfully"}