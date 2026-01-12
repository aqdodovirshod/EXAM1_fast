# apps/Payment/controllers/payment_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.database import get_session
from apps.Payment.services.payment_service import PaymentService
from apps.Payment.schemas.payment import PaymentCreate, PaymentUpdate, PaymentOut

router = APIRouter(prefix="/payments", tags=["Payments"])
service = PaymentService()


@router.post("/", response_model=PaymentOut)
async def create_payment(data: PaymentCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_payment(data, session)


@router.get("/", response_model=list[PaymentOut])
async def get_payments(session: AsyncSession = Depends(get_session)):
    return await service.get_payments(session)


@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(payment_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_payment(payment_id, session)


@router.put("/{payment_id}", response_model=PaymentOut)
async def update_payment(payment_id: int, data: PaymentUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_payment(payment_id, data, session)


@router.delete("/{payment_id}")
async def delete_payment(payment_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_payment(payment_id, session)
    return {"detail": "Payment deleted successfully"}