from web3 import Web3, HTTPProvider
from web3.contract import Contract
from web3.middleware import ExtraDataToPOAMiddleware


class NativeClient:

  def __init__(self, rpc_url: str, api_key: str):
    self.rpc_url = rpc_url
    self.api_key = api_key
    self.client = Web3(self._provider())
    self.client.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

  def get_contract(self, abi: object, address: str) -> Contract:
    return self.client.eth.contract(abi=abi, address=address, decode_tuples=True)

  def get_balance(self, address: str) -> int:
    return self.client.eth.get_balance(address)

  def _provider(self):
    return HTTPProvider(self.rpc_url, {
      'headers': {
        **HTTPProvider.get_request_headers(),
        'x-apikey': self.api_key
      }
    })
