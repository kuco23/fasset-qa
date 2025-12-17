from xrpl import CryptoAlgorithm
from xrpl.account import get_next_valid_seq_number
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.models import Memo, Payment, Response, Tx
from xrpl.transaction import sign, submit_and_wait
from xrpl.wallet import Wallet
from ._ripple_client import RippleClient


class RippleWallet:
  key_gen_algorithm = CryptoAlgorithm.SECP256K1

  def __init__(self, rpc: RippleClient, owner_seed: str):
    self.rpc = rpc
    self.wallet = Wallet.from_seed(owner_seed, algorithm=self.key_gen_algorithm)

  def get_tx(self, tx_hash: str) -> Response:
    return self.rpc.client.request(Tx(transaction=tx_hash))

  def send_tx(
    self,
    amount: str | int,
    destination: str,
    memos: str | list[str] | None = None,
    last_ledger_sequence: int | None = None,
) -> Response:

    if last_ledger_sequence is None:
        last_ledger_sequence = get_latest_validated_ledger_sequence(self.rpc.client) + 20

    built_memos = None

    if isinstance(memos, str):
        built_memos = [Memo(memo_data=memos)]
    elif memos is not None:
        built_memos = [Memo(memo_data=m) for m in memos]

    payment_tx = Payment(
        account=self.wallet.address,
        amount=str(amount),
        destination=destination,
        memos=built_memos,
        last_ledger_sequence=last_ledger_sequence,
        sequence=get_next_valid_seq_number(self.wallet.address, self.rpc.client),
        fee="10",
    )

    payment_response = submit_and_wait(sign(payment_tx, self.wallet), self.rpc.client)
    return self.get_tx(payment_response.result["hash"])