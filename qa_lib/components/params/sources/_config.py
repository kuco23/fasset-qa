from toml import load
from ._env import Env
from ....utils import cached


class Config(Env):

  @property
  def contracts_path(self):
    return self._config['contracts']['path']

  @property
  def asset_manager_abi_path(self):
    return self._config['contracts']['asset_manager_abi']

  @property
  def minted_uba_core_vault_tranfer_threshold_ratio(self):
    return self._config['core_vault_manager']['minted_uba_core_vault_tranfer_threshold_ratio']

  @property
  def minted_uba_core_vault_return_threshold_ratio(self):
    return self._config['core_vault_manager']['minted_uba_core_vault_return_threshold_ratio']

  @property
  def max_free_lots_factor_to_return_from_core_vault(self):
    return self._config['core_vault_manager']['max_free_lots_factor_to_return_from_core_vault']

  @property
  @cached
  def _config(self):
    with open(self.config_path) as cfg:
      return load(cfg)

