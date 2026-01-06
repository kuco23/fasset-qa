from toml import load
from pydantic.dataclasses import dataclass
from dacite import from_dict


@dataclass
class ConfigContracts:
  path: str
  asset_manager_abi: str
  fasset_abi: str

@dataclass
class ConfigCoreVaultManager:
  minted_uba_core_vault_tranfer_threshold_ratio: float
  minted_uba_core_vault_return_threshold_ratio: float
  max_free_lots_factor_to_return_from_core_vault: float

@dataclass
class ConfigCoreVaultRedeemerBot:
  interact_cycle_sleep_seconds: int

@dataclass
class CoreVaultAgentInteracerBot:
  interact_cycle_sleep_seconds: int

@dataclass
class ConfigLoadTest:
  cycle_sleep_secs: int
  fasset_user_config_file_path: str
  fasset_user_secrets_file_path: str
  user_target_xrp_balance: int
  user_target_nat_balance: int
  user_min_xrp_balance: int
  user_min_nat_balance: int

@dataclass
class ConfigOs:
  node_path: str

@dataclass
class Config:
  contracts: ConfigContracts
  core_vault_manager: ConfigCoreVaultManager
  core_vault_redeemer_bot: ConfigCoreVaultRedeemerBot
  core_vault_agent_interacter_bot: CoreVaultAgentInteracerBot
  load_test: ConfigLoadTest
  os: ConfigOs

  @classmethod
  def create(cls, config_path: str):
    return from_dict(data_class=Config, data=cls._load_config_toml(config_path))

  @staticmethod
  def _load_config_toml(config_path: str):
    with open(config_path, 'r') as f:
      return load(f)
