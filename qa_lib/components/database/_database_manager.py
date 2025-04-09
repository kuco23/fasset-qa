from typing import List
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from ._entities import Agent, AgentRedemption

class DatabaseManager:

  def __init__(self, db_type: str, db_user: str, db_pass: str, db_host: str, db_port: int, db_name: str):
    url = URL.create(db_type, db_user, db_pass, db_host, db_port, db_name)
    self.engine = create_engine(url, echo=False)
    if not database_exists(url):
        create_database(url)

  def fetch_agents(self) -> List[Agent]:
    with Session(self.engine, expire_on_commit=False) as session:
      return session.query(Agent).all()

  def agent_executing_transfer_to_core_vault(self, agent_vault: str) -> bool:
    with Session(self.engine, expire_on_commit=False) as session:
      return session.query(AgentRedemption).filter(
        AgentRedemption.agent_address == agent_vault and
        AgentRedemption.is_transfer_to_core_vault == True and
        AgentRedemption.final_state == None
      )
