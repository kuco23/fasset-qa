from time import sleep
from .._context import Context


RUN_CYCLE_SLEEP_SECONDS = 300

class UserCoreVaultRedeemer:

  def __init__(self, context: Context):
    self.context = context

  def run(self):
    while True:
      self.run_step()
      sleep(self.context.params.core_vault_redeemer_bot_sleep_cycle)

  def run_step(self):
    try:
      print(f'checking whether user {self.context.params.user_native_address} can redeem with core vault')
      self.context.user_core_vault_redeemer.mint_if_too_little_fassets()
      self.context.user_core_vault_redeemer.redeem_from_core_vault_if_possible()
    except Exception as err:
      print(f'error running agent vault monitor due to {err}')