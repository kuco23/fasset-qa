from .utils import cached, Singleton
from .components.database import DatabaseManager
from .components.chain import ChainClient, AssetManager
from .components.cmd import AgentBotCli, UserBotCli, AgentRunCli
from .components.params import ParamLoader
from .components.logic import AgentLogic


class Context(metaclass=Singleton):

  @property
  @cached
  def params(self):
    return ParamLoader()

  @property
  @cached
  def database_manager(self):
    return DatabaseManager(
      self.params.database_type,
      self.params.database_user,
      self.params.database_pass,
      self.params.database_host,
      self.params.database_port,
      self.params.database_name
    )

  @property
  @cached
  def chain_client(self):
    return ChainClient(
      self.params.rpc_url,
      self.params.rpc_api_key
    )

  @property
  @cached
  def asset_manager(self):
    return AssetManager(
      self.chain_client,
      self.params._asset_manager_abi,
      self.params.get_address('AssetManager_FTestXRP')
    )

  @property
  @cached
  def agent_bot(self):
    return AgentBotCli(
      self.params.run_dir,
      self.params.agent_bot_cli_path,
      self.params.fasset,
      self.params.agent_bot_env
    )

  @property
  @cached
  def user_bot(self):
    return UserBotCli(
      self.params.run_dir,
      self.params.user_bot_cli_path,
      self.params.fasset,
      self.params.user_bot_env
    )

  @property
  @cached
  def run_agent(self):
    return AgentRunCli(
      self.params.run_dir,
      self.params.agent_run_cli_path,
      self.params.agent_bot_env
    )

  @property
  @cached
  def agent_logic(self):
    return AgentLogic(
      self.params,
      self.database_manager,
      self.asset_manager,
      self.agent_bot
    )