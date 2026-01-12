from fastapi import Depends, HTTPException, status
from apps.User.services.user_dependency import get_current_user
from apps.User.models.user import User


async def admin_required(user: User = Depends(get_current_user)):
    if not user.role or user.role.name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    return user


async def teacher_required(user: User = Depends(get_current_user)):
    if not user.role or user.role.name.lower() != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher role required"
        )
    return user


async def parent_required(user: User = Depends(get_current_user)):
    if not user.role or user.role.name.lower() != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Parent role required"
        )
    return user


async def student_required(user: User = Depends(get_current_user)):
    if not user.role or user.role.name.lower() != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student role required"
        )
    return user


async def teacher_or_admin_required(user: User = Depends(get_current_user)):
    if not user.role or user.role.name.lower() not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher or Admin role required"
        )
    return user
