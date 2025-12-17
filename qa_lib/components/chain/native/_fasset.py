from ._native_client import NativeClient

class FAsset:
  def __init__(self, client: NativeClient, abi: object, address: str):
    self.contract = client.get_contract(abi, address)

  def balance_of(self, address: str) -> int:
    return self.contract.functions.balanceOf(address).call()