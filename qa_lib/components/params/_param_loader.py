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

