from typing import List, Optional
from subprocess import Popen, PIPE


class Cmd:
  process: Optional[Popen] = None

  def __init__(self, cwd_path: str, env: dict[str, str]):
    self.cwd_path = cwd_path
    self.env = env

  def run(self, runner: str, executable: str, command: List[str]) -> str:
    self.process = self._execute(runner, executable, command)
    stdout, stderr = self.process.communicate()
    self.process = None
    return stdout.decode('utf-8') + stderr.decode('utf-8')

  def _execute(self, runner: str, executable: str, commands: List[str]) -> Popen:
    return Popen(
      [runner, executable, *commands],
      stdout=PIPE,
      stderr=PIPE,
      cwd=self.cwd_path,
      env=self.env,
      #restore_signals=False,
      #start_new_session=True
    )

