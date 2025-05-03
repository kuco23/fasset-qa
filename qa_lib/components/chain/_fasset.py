from ._chain_client import ChainClient

class FAsset:
  def __init__(self, client: ChainClient, abi: object, address: str):
    self.contract = client.get_contract(abi, address)

  def balance_of(self, address: str) -> int:
    return self.contract.functions.balanceOf(address).call()