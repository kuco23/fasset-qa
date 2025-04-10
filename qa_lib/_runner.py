from time import sleep
from ._context import Context


SLEEP_TIME_S = 60

class AgentCoreVaultMonitor:

  def __init__(self, context: Context):
    self.context = context

  def run(self):
    while True:
      self.run_step()
      sleep(SLEEP_TIME_S)

  def run_step(self):
    agents = self.context.database_manager.fetch_agents()
    for agent in agents:
      try:
        print(f'checking whether agent {agent.vault_address} should interact with core vault')
        self.context.agent_logic.transfer_to_core_vault_if_makes_sense(agent.vault_address)
        self.context.agent_logic.return_from_core_vault_if_makes_sense(agent.vault_address)
      except Exception as err:
        print(f'error running agent vault monitor due to {err}')
