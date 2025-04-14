from typing import List
from ._agent_bot_cli_parser import AgentBotCliOutputParser
from .._cmd import Cmd


class AgentBotCli(Cmd, AgentBotCliOutputParser):

  def __init__(self, run_dir: str, node_path: str, agent_bot_executable: str, fasset: str, env: dict[str, str]):
    super().__init__(run_dir, env)
    self.node_path = node_path
    self.agent_bot_executable = agent_bot_executable
    self.fasset = fasset

  def create_agent(self, agent_settings_path: str) -> str:
    raw = self.run(['create', agent_settings_path])
    parsed = self.parse_agent_creation(raw)
    resp = self._ensure_parser_response(parsed)
    return resp['agent_vault']

  def deposit_agent_collaterals(self, agent_vault: str, lots: int):
    raw = self.run(['depositCollaterals', agent_vault, str(lots)])
    parsed = self.parse_deposit_agent_collaterals(raw)
    return self._ensure_parser_response(parsed)

  def make_agent_available(self, agent_vault: str):
    raw = self.run(['enter', agent_vault])
    parsed = self.parse_agent_available(raw)
    return self._ensure_parser_response(parsed)

  def transfer_to_core_vault(self, agent_vault: str, amount: int):
    raw = self.run(['transferToCoreVault', agent_vault, str(amount)])
    parsed = self.parse_request_transfer_to_core_vault(raw)
    return self._ensure_parser_response(parsed)

  def return_from_core_vault(self, agent_vault: str, amount: int):
    resp = self.run(['returnFromCoreVault', agent_vault, str(amount)])
    print(resp)

  def run(self, commands: List[str]):
    commands.extend(['-f', self.fasset])
    return super().run(self.node_path, self.agent_bot_executable, commands)

