from typing import List
from ._agent_bot_cli_parser import AgentBotCliOutputParser
from .._cmd import Cmd


class AgentBotCli(Cmd, AgentBotCliOutputParser):

  def __init__(self, run_dir: str, agent_bot_executable: str, fasset: str, env: dict[str, str]):
    super().__init__(run_dir, env)
    self.fasset = fasset
    self.agent_bot_executable = agent_bot_executable

  def create_agent(self, agent_settings_path: str) -> str:
    raw = self.run(['create', agent_settings_path])
    parsed = self.parse_agent_creation(raw)
    resp = self._ensure_parser_response(parsed)
    return resp['agent_vault']

  def deposit_agent_collaterals(self, agent_vault: str, lots: int):
    raw = self.run(['depositCollaterals', agent_vault, str(lots)])
    parsed = self.parse_deposit_agent_collaterals(raw)
    resp = self._ensure_parser_response(parsed)
    return resp

  def make_agent_available(self, agent_vault: str):
    raw = self.run(['enter', agent_vault])
    parsed = self.parse_agent_available(raw)
    resp = self._ensure_parser_response(parsed)
    return resp

  def transfer_to_core_vault(self, agent_vault: str, amount: int):
    resp = self.run(['transferToCoreVault', agent_vault, str(amount)])
    print(resp)

  def return_from_core_vault(self, agent_vault: str, amount: int):
    resp = self.run(['returnFromCoreVault', agent_vault, str(amount)])
    print(resp)

  def run(self, commands: List[str]):
    commands.extend(['-f', self.fasset])
    return super().run('node', self.agent_bot_executable, commands)

