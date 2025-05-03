from json import load
from .sources import Constants, Config
from ...utils import cached


"""
Abstraction over low level parameter fetching,
adding some transformers and utilities.
"""

class ParamLoader(Constants, Config):

  def get_address(self, name: str) -> str:
    for contract in self._contracts:
      if contract['name'] == name:
        return contract['address']

  @property
  @cached
  def _contracts(self):
    return load(open(self.contracts_path, 'r'))

  @property
  @cached
  def _asset_manager_abi(self):
    return load(open(self.asset_manager_abi_path, 'r'))['abi']

  @property
  @cached
  def _fasset_abi(self):
    return load(open(self.fasset_abi_path, 'r'))['abi']

  @property
  @cached
  def user_secrets(self):
    return load(open(self.fasset_user_secrets_path, 'r'))

  @property
  def user_native_address(self) -> str:
    return self.user_secrets['user']['native']['address']

  @property
  def user_underlying_address(self) -> str:
    return self.user_secrets['user'][self.asset_name]['address']

  @property
  def agent_bot_env(self) -> dict[str, str]:
    return {
      'FASSET_BOT_CONFIG': self.fasset_bot_config_path,
      'FASSET_BOT_SECRETS': self.fasset_bot_secrets_path
    }

  @property
  def user_bot_env(self) -> dict[str, str]:
    return {
      'FASSET_USER_CONFIG': self.fasset_user_config_path,
      'FASSET_USER_SECRETS': self.fasset_user_secrets_path
    }
