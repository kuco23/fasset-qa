from typing import List, Optional
from .._cmd import Cmd
from ._user_bot_cli_parser import UserBotCliOutputParser


class UserBotCli(Cmd, UserBotCliOutputParser):

  def __init__(self, run_dir: str, user_bot_executable: str, fasset: str, env: dict[str, str]):
    super().__init__(run_dir, env)
    self.fasset = fasset
    self.user_bot_executable = user_bot_executable

  def mint(self, lots: int, agent_vault: Optional[str] = None):
    cmd_ext = ['-a', agent_vault] if agent_vault else []
    resp = self.run(['mint', str(lots), *cmd_ext])
    print(resp)

  def run(self, commands: List[str]):
    commands.extend(['-f', self.fasset])
    return super().run('node', self.user_bot_executable, commands)
