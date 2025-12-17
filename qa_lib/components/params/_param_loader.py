from json import load
from .sources import Constants, Config, Env
from ...utils import cached


"""
Abstraction over low level parameter fetching,
adding some transformers and utilities.
"""

class ParamLoader(Env, Constants):
  config: Config

  def __init__(self):
    self.config = Config.create(self.config_path)

  def get_address(self, name: str) -> str:
    for contract in self._contracts:
      if contract['name'] == name:
        return contract['address']

  @property
  @cached
  def _contracts(self):
    return load(open(self.config.contracts.path, 'r'))

  @property
  @cached
  def _asset_manager_abi(self):
    return load(open(self.config.contracts.asset_manager_abi, 'r'))['abi']

  @property
  @cached
  def _fasset_abi(self):
    return load(open(self.config.contracts.fasset_abi, 'r'))['abi']
