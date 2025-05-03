from ..params import ParamLoader
from ..chain import AssetManager, FAsset
from ..cmd import UserBotCli


class UserCoreVaultRedeemerer:

  def __init__(self, params: ParamLoader, fasset: FAsset, asset_manager: AssetManager, user_bot_cli: UserBotCli):
    self.params = params
    self.fasset = fasset
    self.asset_manager = asset_manager
    self.user_bot_cli = user_bot_cli

  def redeem_from_core_vault_if_possible(self):
    balance = self.fasset.balance_of(self.params.user_native_address)
    balance_lots = self.uba_to_lots(balance)
    if balance_lots >= self.params.core_vault_min_redeem_lots:
      self.user_bot_cli.redeem_from_core_vault(self.params.core_vault_min_redeem_lots)

  def mint_if_too_little_fassets(self):
    balance = self.fasset.balance_of(self.params.user_native_address)
    balance_lots = self.uba_to_lots(balance)
    if balance_lots < self.params.core_vault_min_redeem_lots:
      to_mint = self.params.core_vault_min_redeem_lots - balance_lots
      self.user_bot_cli.mint(to_mint)

  def uba_to_lots(self, amount: int) -> int:
    return amount // self.params.lot_size