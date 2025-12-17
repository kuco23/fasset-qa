import attrs
from time import sleep
from .._dependency_manager import DependencyManager


@attrs.frozen
class SimpleUser:
  context: DependencyManager

  def run(self):
    while True:
      self.run_step()
      sleep(self.context.params.core_vault_redeemer_bot_sleep_cycle)

  def run_step(self):
    try:
      print(f'checking whether user {self.context.params.user_native_address} can redeem with core vault')
      self.context.simple_user_bot.mint_or_redeem()
    except Exception as err:
      print(f'error running agent vault monitor due to {err}')