from xrpl.clients import JsonRpcClient
from xrpl.models import AccountInfo


class RippleClient:

  def __init__(self, rpc_url: str, rpc_api_key: str) -> None:
    self.client = JsonRpcClient(rpc_url)

  def get_balance(self, xrpl_address: str) -> int:
    response = self.client.request(AccountInfo(account=xrpl_address))
    return int(response.result["account_data"]["Balance"])

