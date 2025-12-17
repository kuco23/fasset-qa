from typing import Tuple
from ._native_client import NativeClient

class AssetManager:

  def __init__(self, client: NativeClient, abi: object, address: str):
    self.contract = client.get_contract(abi, address)

  def core_vault_available_amount(self) -> Tuple[int, int]:
    return self.contract.functions.coreVaultAvailableAmount().call()

  def maximum_transfer_to_core_vault(self, agent_vault: str) -> Tuple[int, int]:
    return self.contract.functions.maximumTransferToCoreVault(agent_vault).call()

  def agent_info(self, agent_vault: str):
    return self.contract.functions.getAgentInfo(agent_vault).call()._asdict()
