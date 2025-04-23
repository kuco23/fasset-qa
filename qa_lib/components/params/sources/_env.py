from os import environ
from dotenv import load_dotenv


class Env:
  loaded: bool = False

  def __init__(self):
    if not Env.loaded:
      load_dotenv()
    Env.loaded = True

  @property
  def database_type(self) -> str:
    return environ.get('DB_TYPE')

  @property
  def database_user(self) -> str:
    return environ.get('DB_USER')

  @property
  def database_pass(self) -> str:
    return environ.get('DB_PASS')

  @property
  def database_name(self) -> str:
    return environ.get('DB_NAME')

  @property
  def database_host(self) -> str:
    return environ.get('DB_HOST')

  @property
  def database_port(self) -> int:
    return int(environ.get('DB_PORT'))

  @property
  def rpc_url(self) -> str:
    return self._required('RPC_URL')

  @property
  def rpc_api_key(self) -> str:
    return environ.get('RPC_API_KEY')

  @property
  def node_path(self) -> str:
    return self._required('NODE_PATH')

  @property
  def fasset_bot_config_path(self) -> str:
    return self._required('FASSET_BOT_CONFIG')

  @property
  def fasset_bot_secrets_path(self) -> str:
    return self._required('FASSET_BOT_SECRETS')

  @property
  def fasset_user_config_path(self) -> str:
    return self._required('FASSET_USER_CONFIG')

  @property
  def fasset_user_secrets_path(self) -> str:
    return self._required('FASSET_USER_SECRETS')

  @property
  def config_path(self) -> str:
    return environ.get('CONFIG') or './config.toml'

  @staticmethod
  def _required(name: str) -> str:
    var = environ.get(name)
    assert var is not None, f'environment variable {name} not found!'
    return var
