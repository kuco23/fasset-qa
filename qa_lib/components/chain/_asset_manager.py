from typing import Tuple
from ._chain_client import ChainClient

class AssetManager:

  def __init__(self, client: ChainClient, abi: object, address: str):
    self.contract = client.get_contract(abi, address)

  def core_vault_available_amount(self) -> Tuple[int, int]:
    return self.contract.coreVaultAvailableAmount().call()

  def maximum_transfer_to_core_vault(self, agent_vault: str) -> Tuple[int, int]:
    return self.contract.maximumTransferToCoreVault(agent_vault).call()

  def agent_info(self, agent_vault: str):
    return self.contract.getAgentInfo(agent_vault).call()


