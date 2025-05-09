from os import getcwd

class Constants:

  @property
  def run_dir(self) -> str:
    return getcwd()

  @property
  def agent_bot_cli_path(self) -> str:
    return './fasset-bots/packages/fasset-bots-cli/dist/src/cli/agent-bot.js'

  @property
  def user_bot_cli_path(self) -> str:
    return './fasset-bots/packages/fasset-bots-cli/dist/src/cli/user-bot.js'

  @property
  def agent_run(self) -> str:
    return './fasset-bots/packages/fasset-bots-cli/dist/src/run/run-agent'

  ##########################################################
  # should be configured dynamicaly

  @property
  def fasset(self) -> str:
    return 'FTestXRP'

  @property
  def lot_size(self) -> int:
    return 20000000

  @property
  def token_decimals(self) -> int:
    return 6