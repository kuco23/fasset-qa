from qa_lib.utils import logger
from .._user_base import BaseUserBot


MINT_FREE_LOT_RATIO = 10

class UserMinterAndRedeemer(BaseUserBot):

  def mint(self, agent_vault: str, max_minted_lots: int):
    xrp_balance = self.ripple_client.get_balance(self.underlying_address)
    xrp_balance_lots = self.utils.uba_to_lots(xrp_balance)
    if xrp_balance_lots > 1:
      agent_info = self.asset_manager.agent_info(agent_vault)
      agent_free_lots = agent_info['freeCollateralLots']
      if agent_free_lots >= MINT_FREE_LOT_RATIO:
        mint_lots = min(agent_free_lots // MINT_FREE_LOT_RATIO, xrp_balance_lots)
        mint_lots = max(mint_lots, max_minted_lots)
        logger.info(f'user {self.user_id} started minting {mint_lots} lots')
        resp = self.user_bot_cli.mint(mint_lots, agent_vault)
        logger.info(f'user {self.user_id} successfully minted {mint_lots} lots: {resp}')
      else:
        logger.info(f'user {self.user_id} skipped minting due to agent having {agent_free_lots} < {MINT_FREE_LOT_RATIO} free lots')
    else:
      logger.info(f'user {self.user_id} skipped minting due to insufficient balance of {xrp_balance} {self.params.asset_name}')

  def redeem_all(self):
    fxrp_balance = self.fasset.balance_of(self.native_address)
    fxrp_balance_lots = self.utils.uba_to_lots(fxrp_balance)
    if fxrp_balance_lots > 0:
      logger.info(f'user {self.user_id} started redeeming {fxrp_balance_lots} {self.params.fasset_name}')
      resp = self.user_bot_cli.redeem(fxrp_balance_lots)
      logger.info(f'user {self.user_id} successfully redeemed: {resp}')
    else:
      logger.info(f'user {self.user_id} skipped redeeming due to insufficient balance of {fxrp_balance} {self.params.fasset_name}')