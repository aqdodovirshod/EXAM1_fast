from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from apps.Payment.repositories.payment_repository import PaymentRepository
from apps.Student.models.student import Student
from apps.Parent.models.parent import Parent
from apps.Payment.schemas.payment import PaymentCreate, PaymentUpdate, PaymentOut

class PaymentService:
    def __init__(self):
        self.repo = PaymentRepository()

    async def create_payment(self, data: PaymentCreate, session: AsyncSession):
        if data.period_end < data.period_start:
            raise HTTPException(status_code=400, detail="period_end must be after period_start")

        student = await session.get(Student, data.student_id)
        if not student:
            raise HTTPException(status_code=400, detail="Student not found")

        parent = await session.get(Parent, data.parent_id)
        if not parent:
            raise HTTPException(status_code=400, detail="Parent not found")

        payment = await self.repo.create(data.dict(), session)

        return PaymentOut(
            id=payment.id,
            amount=payment.amount,
            payment_date=payment.payment_date,
            period_start=payment.period_start,
            period_end=payment.period_end,
            student_id=payment.student_id,
            parent_id=payment.parent_id,
            status=payment.status,
        )

    async def get_payments(self, session: AsyncSession):
        payments = await self.repo.get_all(session)
        return [
            PaymentOut(
                id=p.id,
                amount=p.amount,
                payment_date=p.payment_date,
                period_start=p.period_start,
                period_end=p.period_end,
                student_id=p.student_id,
                parent_id=p.parent_id,
                status=p.status,
            )
            for p in payments
        ]

    async def get_payment(self, payment_id: int, session: AsyncSession):
        payment = await self.repo.get_by_id(payment_id, session)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        return PaymentOut(
            id=payment.id,
            amount=payment.amount,
            payment_date=payment.payment_date,
            period_start=payment.period_start,
            period_end=payment.period_end,
            student_id=payment.student_id,
            parent_id=payment.parent_id,
            status=payment.status,
        )

    async def update_payment(self, payment_id: int, data: PaymentUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True, exclude={"student_id", "parent_id"})
        payment = await self.repo.update(payment_id, update_data, session)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        return PaymentOut(
            id=payment.id,
            amount=payment.amount,
            payment_date=payment.payment_date,
            period_start=payment.period_start,
            period_end=payment.period_end,
            student_id=payment.student_id,
            parent_id=payment.parent_id,
            status=payment.status,
        )

    async def delete_payment(self, payment_id: int, session: AsyncSession):
        payment = await self.repo.delete(payment_id, session)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment