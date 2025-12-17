from pydantic.dataclasses import dataclass

@dataclass
class CliMintResponse:
  mint_id: int
  agent_vault: str
  tx_hash: str

  def __post_init__(self):
    self.mint_id = int(self.mint_id)

@dataclass
class CliRedeemResponse:
  redemption_id: int
  redeemer: str
  amount: int
  agent_vault: str
  reference: str

  def __post_init__(self):
    self.redemption_id = int(self.redemption_id)

@dataclass
class CliRedeemFromCoreVaultResponse:
  lots: int

  def __post_init__(self):
    self.lots = int(self.lots)