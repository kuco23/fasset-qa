from random import randint
from qa_lib.utils import logger
from .._user_base import BaseUserBot


MINT_FREE_LOT_RATIO = 8
MIN_MINTED_LOTS = 1

class UserMinterAndRedeemer(BaseUserBot):

  def mint(self, agent_vault: str, max_minted_lots: int):
    xrp_balance = self.ripple_client.get_balance(self.underlying_address)
    xrp_balance_lots = self.utils.uba_to_lots(xrp_balance)
    if xrp_balance_lots > MIN_MINTED_LOTS:
      agent_info = self.asset_manager.agent_info(agent_vault)
      agent_free_lots = agent_info['freeCollateralLots']
      if agent_free_lots >= MINT_FREE_LOT_RATIO:
        mint_lots = self.get_mint_amount(agent_free_lots, xrp_balance_lots, max_minted_lots)
        logger.info(f'user {self.user_id} with balance {xrp_balance_lots} lots of {self.fassetn} minting {mint_lots} lots of {self.fassetn}')
        resp = self.user_bot_cli.mint(mint_lots, agent_vault)
        logger.info(f'user {self.user_id} minted with crt id {resp.mint_id}')
      else:
        logger.info(f'user {self.user_id} skipped minting due to agent having {agent_free_lots} < {MINT_FREE_LOT_RATIO} free lots')
    else:
      logger.info(f'user {self.user_id} skipped minting due to insufficient balance of {xrp_balance} {self.assetn}')

  def redeem_all(self):
    fxrp_balance = self.fasset.balance_of(self.native_address)
    fxrp_balance_lots = self.utils.uba_to_lots(fxrp_balance)
    if fxrp_balance_lots > 0:
      logger.info(f'user {self.user_id} redeeming {fxrp_balance_lots} lots of {self.fassetn}')
      resp = self.user_bot_cli.redeem(fxrp_balance_lots)
      logger.info(f'user {self.user_id} redeemed {resp.amount} {self.fassetn} with request id {resp.redemption_id}')
    else:
      logger.info(f'user {self.user_id} skipped redeeming due to insufficient balance of {fxrp_balance} {self.fassetn}')

  def get_mint_amount(self, free_lots: int, balance_lots: int, cap_lots: int):
    return randint(MIN_MINTED_LOTS, min(free_lots // MINT_FREE_LOT_RATIO, balance_lots - 1, cap_lots))

  @property
  def fassetn(self):
    return self.params.fasset_name

  @property
  def assetn(self):
    return self.params.asset_name