from eth_account import Account
from eth_account.signers.local import LocalAccount, SignedTransaction
from ._native_client import NativeClient


class NativeWallet:

  def __init__(self, client: NativeClient, private_key: str):
    self.client = client
    self.wallet: LocalAccount = Account.from_key(private_key)

  def send_tx(self, amount: int, to: str):
    nonce = self.client._client.eth.get_transaction_count(self.wallet.address)
    transaction = {
      'to': to,
      'value': amount,
      'gas': 21000,
      'gasPrice': 25000000000,
      'nonce': nonce,
      'chainId': 114
    }
    raw_tx: SignedTransaction = self.client._client.eth.account.sign_transaction(transaction, self.wallet.key)
    self.client._client.eth.send_raw_transaction(raw_tx.raw_transaction)