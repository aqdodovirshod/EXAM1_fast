from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_session
from apps.Role.models.role import Role
from apps.Role.schemas.role import RoleCreate, RoleRead
from apps.Role.services.role_service import RoleService

role_router = APIRouter(prefix="/roles", tags=["roles"])

@role_router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(data: RoleCreate, session: AsyncSession = Depends(get_session)):
    return await RoleService.create_role(data=data, session=session)

@role_router.get("/", response_model=list[RoleRead])
async def list_roles(session: AsyncSession = Depends(get_session)):
    return await RoleService.get_roles(session=session)