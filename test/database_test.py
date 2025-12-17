from sqlalchemy.orm import Session
from qa_lib import DependencyManager
from qa_lib.components.database._entities import ReturnFromCoreVault, AgentRedemption


def get_all_transfers(context: DependencyManager, agent_vault):
  with Session(context.database_manager.engine, expire_on_commit=False) as session:
    return session.query(AgentRedemption).filter(
      AgentRedemption.is_transfer_to_core_vault == True, AgentRedemption.agent_address == agent_vault
    ).all()

context = DependencyManager()

resp = get_all_transfers(context, '0x2087Bc949Fa84D0628E62e36c38d250E63c2A947')
resp2 = context.database_manager.open_core_vault_returns('0x2087Bc949Fa84D0628E62e36c38d250E63c2A947')
print(list(map(lambda x: x.__dict__, resp)))
print(list(map(lambda x: x.__dict__, resp2)))