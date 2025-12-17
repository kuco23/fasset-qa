import attrs
from time import sleep
from .._dependency_manager import DependencyManager


RUN_CYCLE_SLEEP_SECONDS = 300

@attrs.frozen
class AgentCoreVaultHandler:
  context: DependencyManager

  def run(self):
    while True:
      self.run_step()
      sleep(self.context.params.core_vault_interacter_bot_sleep_cycle)

  def run_step(self):
    agents = self.context.database_manager.fetch_agents()
    for agent in agents:
      try:
        print(f'checking whether agent {agent.vault_address} should interact with core vault')
        self.context.agent_core_vault_interact.transfer_to_core_vault_if_makes_sense(agent.vault_address)
        self.context.agent_core_vault_interact.return_from_core_vault_if_makes_sense(agent.vault_address)
      except Exception as err:
        print(f'error running agent vault monitor due to {err}')