from pydantic.dataclasses import dataclass

@dataclass
class CliAgentVaultCreatedResponse:
  agent_vault: str

@dataclass
class CliCollateralsDepositedResponse:
  agent_vault: str
  vault_token: str
  vault_amount: float
  native_token: str
  native_amount: float

  def __post_init__(self):
    self.vault_amount = float(self.vault_amount)
    self.native_amount = float(self.native_amount)

@dataclass
class CliAgentAvailableResponse:
  agent_vault: str

@dataclass
class CliRequestTransferToCoreVaultResponse:
  redemption_id: int
  agent_vault: str

  def __post_init__(self):
    self.redemption_id = int(self.redemption_id)