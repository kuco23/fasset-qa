from typing import Tuple
from ..params import ParamLoader
from ..database import DatabaseManager
from ..chain import AssetManager
from ..cmd import AgentBotCli


MINTED_UBA_CORE_VAULT_TRANSFER_THRESHOLD_RATIO = 0.75
MINTED_UBA_CORE_VAULT_RETURN_THRESHOLD_RATIO = 0.25
MAX_FREE_LOTS_FACTOR_TO_RETURN_FROM_CORE_VAULT = 0.5

class AgentLogic:

  def __init__(self, params: ParamLoader, database: DatabaseManager, asset_manager: AssetManager, agent_bot: AgentBotCli):
    self.params = params
    self.database = database
    self.asset_manager = asset_manager
    self.agent_bot = agent_bot

  def create_agent(self, settings_path: str, deposit_for_lots: int = 0, make_available: bool = False):
    agent_vault = self.agent_bot.create_agent(settings_path)
    if deposit_for_lots > 0:
      self.agent_bot.deposit_agent_collaterals(agent_vault, deposit_for_lots)
      if make_available:
        self.agent_bot.make_agent_available(agent_vault)

  def transfer_to_core_vault_if_makes_sense(self, agent_vault: str):
    transfer_open = self.agent_has_open_transfer_to_core_vault_requests(agent_vault)
    if transfer_open: return
    optimal_transfer_to_core_vault_uba = self.optimal_agent_transfer_to_core_vault_uba(agent_vault)
    if optimal_transfer_to_core_vault_uba > 0:
      optimal_transfer_to_core_vault_tok = self.uba_to_tokens(optimal_transfer_to_core_vault_uba)
      print(f'transferring {optimal_transfer_to_core_vault_tok} {self.params.fasset} to core vault for agent vault {agent_vault}')
      self.agent_bot.transfer_to_core_vault(agent_vault, optimal_transfer_to_core_vault_tok)

  def return_from_core_vault_if_makes_sense(self, agent_vault: str):
    return_open = self.agent_has_open_return_from_core_vault_requests(agent_vault)
    if return_open: return
    optimal_return_from_core_vault_uba = self.optimal_agent_return_from_core_vault_uba(agent_vault)
    optimal_return_from_core_vault_lots = self.uba_to_lots(optimal_return_from_core_vault_uba)
    if optimal_return_from_core_vault_lots > 0:
      print(f'returning {optimal_return_from_core_vault_lots} lots of {self.params.fasset} from core vault for agent vault {agent_vault}')
      self.agent_bot.return_from_core_vault(agent_vault, optimal_return_from_core_vault_lots)

  def optimal_agent_transfer_to_core_vault_uba(self, agent_vault: str) -> int:
    """Define the optimal value to transfer to core vault for the given agent"""
    agent_info = self.asset_manager.agent_info(agent_vault)
    minted_uba, free_uba = self.get_agent_minted_and_free_uba(agent_info)

    total_uba = free_uba + minted_uba
    if total_uba == 0: return 0
    minted_ratio = minted_uba / total_uba

    if minted_ratio > MINTED_UBA_CORE_VAULT_TRANSFER_THRESHOLD_RATIO:
      max_transfer, _  = self.asset_manager.maximum_transfer_to_core_vault(agent_vault)
      return max_transfer

    return 0

  def optimal_agent_return_from_core_vault_uba(self, agent_vault: str):
    """Define the optimal value to return from core vault for the given agent"""
    agent_info = self.asset_manager.agent_info(agent_vault)
    minted_uba, free_uba = self.get_agent_minted_and_free_uba(agent_info)

    total_uba = free_uba + minted_uba
    if total_uba == 0: return 0
    minted_ratio = minted_uba / total_uba

    if minted_ratio < MINTED_UBA_CORE_VAULT_RETURN_THRESHOLD_RATIO:
      _, core_vault_balance = self.asset_manager.core_vault_available_amount()
      max_returned_uba = int(free_uba / MAX_FREE_LOTS_FACTOR_TO_RETURN_FROM_CORE_VAULT)
      return min(core_vault_balance, max_returned_uba)

    return 0

  def get_agent_minted_and_free_uba(self, agent_info) -> Tuple[int, int]:
    minted_uba = agent_info['mintedUBA']
    free_lots = agent_info['freeCollateralLots']
    free_uba = free_lots * self.params.lot_size
    return minted_uba, free_uba

  def agent_has_open_transfer_to_core_vault_requests(self, agent_vault: str):
    requests = self.database.open_core_vault_transfers(agent_vault)
    return len(requests) > 0

  def agent_has_open_return_from_core_vault_requests(self, agent_vault: str):
    requests = self.database.open_core_vault_returns(agent_vault)
    return len(requests) > 0

  def uba_to_tokens(self, amount: int) -> float:
    return amount / 10 ** self.params.token_decimals

  def uba_to_lots(self, amount: int) -> int:
    return amount // self.params.lot_size