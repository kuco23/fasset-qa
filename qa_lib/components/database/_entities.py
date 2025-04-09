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
    final_state: Mapped[str] = mapped_column()