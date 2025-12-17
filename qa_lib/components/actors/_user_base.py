from attrs import frozen
from json import load
from qa_lib.components.common import CommonUtils
from qa_lib.components.params import ParamLoader
from qa_lib.components.chain import RippleClient, AssetManager, FAsset
from qa_lib.components.cmd import UserBotCli


@frozen
class BaseUserBot:
  user_id: str
  params: ParamLoader
  utils: CommonUtils
  ripple_client: RippleClient
  fasset: FAsset
  asset_manager: AssetManager
  user_bot_cli: UserBotCli

  @property
  def secrets(self):
    secrets_path = self.user_bot_cli.env['FASSET_USER_SECRETS']
    return load(open(secrets_path, 'r'))

  @property
  def native_address(self) -> str:
    return self.secrets['user']['native']['address']

  @property
  def underlying_address(self) -> str:
    return self.secrets['user'][self.params.asset_name]['address']