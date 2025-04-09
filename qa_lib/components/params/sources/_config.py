from typing import List


class Config:

  def __init__(self):
    pass

  @property
  def contracts_path(self):
    return './fasset-bots/packages/fasset-bots-core/fasset-deployment/coston.json'

  @property
  def asset_manager_abi_path(self):
    return './fasset-bots/packages/fasset-bots-core/artifacts/contracts/userInterfaces/IAssetManager.sol/IAssetManager.json'

  @property
  def agent_vault_settings_dir(self) -> List[str]:
    return './config/vaults'
