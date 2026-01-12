from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Payment.models.payment import Payment

class PaymentRepository:
    async def create(self, data: dict, session: AsyncSession):
        payment = Payment(**data)
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Payment).options(
                selectinload(Payment.student),
                selectinload(Payment.parent)
            )
        )
        return result.scalars().all()

    async def get_by_id(self, payment_id: int, session: AsyncSession):
        return await session.get(
            Payment,
            payment_id,
            options=[selectinload(Payment.student), selectinload(Payment.parent)]
        )

    async def update(self, payment_id: int, data: dict, session: AsyncSession):
        payment = await self.get_by_id(payment_id, session)
        if not payment:
            return None

        for key, value in data.items():
            if value is not None and hasattr(payment, key):
                setattr(payment, key, value)

        await session.commit()
        await session.refresh(payment)
        return payment

    async def delete(self, payment_id: int, session: AsyncSession):
        payment = await self.get_by_id(payment_id, session)
        if not payment:
            return None
        await session.delete(payment)
        await session.commit()
        return payment