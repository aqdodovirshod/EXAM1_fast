from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Parent.services.parent_service import ParentService
from apps.Parent.schemas.parent import ParentCreate, ParentUpdate, ParentOut
from apps.User.services.permission import admin_required


router = APIRouter(prefix="/parents", tags=["Parents"])
service = ParentService()


@router.post("/", response_model=ParentOut)
async def create_parent(data: ParentCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_parent(data, session)


@router.get("/", response_model=list[ParentOut])
async def get_parents(session: AsyncSession = Depends(get_session)):
    return await service.get_parents(session)


@router.get("/{parent_id}", response_model=ParentOut)
async def get_parent(parent_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_parent(parent_id, session)


@router.put("/{parent_id}", response_model=ParentOut)
async def update_parent(parent_id: int, data: ParentUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_parent(parent_id, data, session)


@router.delete("/{parent_id}", dependencies=[Depends(admin_required)])
async def delete_parent(parent_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_parent(parent_id, session)
    return {"detail": "Parent deleted successfully"}