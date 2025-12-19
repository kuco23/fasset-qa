from typing import List, Optional
from .._cmd import Cmd
from ._user_bot_cli_parser import UserBotCliOutputParser


CR_FEE_BUMP = 0.1

class UserBotCli(Cmd, UserBotCliOutputParser):

  def __init__(self, run_dir: str, node_path: str, user_bot_executable: str, fasset: str, env: dict[str, str]):
    super().__init__(run_dir, env)
    self.node_path = node_path
    self.user_bot_executable = user_bot_executable
    self.fasset = fasset

  def mint(self, lots: int, agent_vault: Optional[str] = None):
    cmd_ext = ['-a', agent_vault] if agent_vault else []
    raw = self.run(['mint', str(lots), '--crFeeBump', str(CR_FEE_BUMP), *cmd_ext])
    parsed = self.parse_user_mint(raw)
    return self._ensure_parser_response(parsed)

  def redeem(self, lots: int):
    raw = self.run(['redeem', str(lots)])
    parsed = self.parse_user_redeem(raw)
    return self._ensure_parser_response(parsed)

  def redeem_from_core_vault(self, lots: int):
    raw = self.run(['redeemFromCoreVault', str(lots)])
    parsed = self.parse_user_redeem_from_core_vault(raw)
    return self._ensure_parser_response(parsed)

  def run(self, commands: List[str]):
    commands.extend(['-f', self.fasset])
    return super().run(self.node_path, self.user_bot_executable, commands)
