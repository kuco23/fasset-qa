from .._cmd import Cmd


class AgentRunCli(Cmd):
  process: str

  def __init__(self, run_dir: str, agent_run_executable: str, env: dict[str, str]):
    super().__init__(run_dir, env)
    self.agent_run_executable = agent_run_executable

  def run_agent(self):
    super().run('node', self.agent_run_executable, [])
