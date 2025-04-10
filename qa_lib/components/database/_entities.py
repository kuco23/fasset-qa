from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
  pass

class Agent(Base):
  __tablename__ = "agent"

  vault_address: Mapped[str] = mapped_column(primary_key=True)

class AgentRedemption(Base):
  __tablename__ = 'agent_redemption'

  id: Mapped[int] = mapped_column(primary_key=True)
  agent_address: Mapped[str] = mapped_column()
  is_transfer_to_core_vault: Mapped[bool] = mapped_column()
  state: Mapped[str] = mapped_column()
  final_state: Mapped[str] = mapped_column()
  request_id: Mapped[int] = mapped_column()
  redeemer_address: Mapped[str] = mapped_column()
  created_at: Mapped[datetime] = mapped_column()

class ReturnFromCoreVault(Base):
  __tablename__ = 'return_from_core_vault'

  id: Mapped[int] = mapped_column(primary_key=True)
  state: Mapped[str] = mapped_column()
  agent_address: Mapped[str] = mapped_column()
  request_id: Mapped[str] = mapped_column()
  payment_reference: Mapped[str] = mapped_column()
  cancelled: Mapped[bool] = mapped_column()
  tx_hash: Mapped[str] = mapped_column()
  created_at: Mapped[datetime] = mapped_column()
