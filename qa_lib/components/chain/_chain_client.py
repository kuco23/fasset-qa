from web3 import Web3, HTTPProvider


class ChainClient:

  def __init__(self, rpc_url: str, api_key: str):
    self._rpc_url = rpc_url
    self._api_key = api_key
    self._client = Web3(HTTPProvider(rpc_url, {
      'headers': {
        **HTTPProvider.get_request_headers(),
        'x-apikey': api_key
      }
    }))

  def get_contract(self, abi: object, address: str):
    contract = self._client.eth.contract(abi=abi, address=address)
    return contract.functions
