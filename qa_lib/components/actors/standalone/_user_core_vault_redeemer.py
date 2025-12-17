from .._user_base import BaseUserBot

class UserCoreVaultRedeemerer(BaseUserBot):

  def redeem_from_core_vault_if_possible(self):
    balance = self.fasset.balance_of(self.native_address)
    balance_lots = self.utils.uba_to_lots(balance)
    if balance_lots >= self.params.core_vault_min_redeem_lots:
      self.user_bot_cli.redeem_from_core_vault(self.params.core_vault_min_redeem_lots)

  def mint_if_too_little_fassets(self):
    balance = self.fasset.balance_of(self.native_address)
    balance_lots = self.utils.uba_to_lots(balance)
    if balance_lots < self.params.core_vault_min_redeem_lots:
      to_mint = self.params.core_vault_min_redeem_lots - balance_lots
      self.user_bot_cli.mint(to_mint)

