from time import sleep
from eth_account import Account
from eth_account.signers.local import LocalAccount, SignedTransaction
from ._native_client import NativeClient

NONCE_INCREASE_SLEEP = 1

class NativeWallet:

  def __init__(self, client: NativeClient, private_key: str):
    self.web3 = client
    self.wallet: LocalAccount = Account.from_key(private_key)

  def send_tx(self, amount: int, to: str):
    nonce = self.web3.client.eth.get_transaction_count(self.wallet.address)
    transaction = {
      'to': to,
      'value': amount,
      'gas': 21000,
      'maxFeePerGas': self.web3.client.eth.gas_price * 2,
      'maxPriorityFeePerGas': self.web3.client.eth.max_priority_fee,
      'nonce': nonce,
      'chainId': 114
    }
    raw_tx: SignedTransaction = self.web3.client.eth.account.sign_transaction(transaction, self.wallet.key)
    self.web3.client.eth.send_raw_transaction(raw_tx.raw_transaction)
    self._wait_for_nonce_increase(nonce)

  def _wait_for_nonce_increase(self, nonce: int):
    while self.web3.client.eth.get_transaction_count(self.wallet.address) == nonce:
      sleep(NONCE_INCREASE_SLEEP)