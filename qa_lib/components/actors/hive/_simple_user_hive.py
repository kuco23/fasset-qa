from typing import List
from random import choice
from time import sleep
from attrs import frozen
from qa_lib.utils import logger
from qa_lib.components.params import ParamLoader
from qa_lib.components.chain import RippleWallet, RippleClient, NativeWallet, NativeClient, FAsset
from ..standalone import UserMinterAndRedeemer


MAX_MINTED_LOTS = 4
XRP_DROP_FACTOR = 10 ** 6
NAT_WEI_FACTOR = 10 ** 18

@frozen
class SimpleUserHive:
  params: ParamLoader
  ripple_rpc: RippleClient
  ripple_root: RippleWallet
  native_rpc: NativeClient
  native_root: NativeWallet
  fasset: FAsset
  users: List[UserMinterAndRedeemer]

  def fund(self):
    root_xrp_balance = self.ripple_rpc.get_balance(self.ripple_root.wallet.address)
    root_nat_balance = self.native_rpc.get_balance(self.native_root.wallet.address)

    xrp_target = self.params.config.load_test.user_target_xrp_balance * XRP_DROP_FACTOR
    nat_target = self.params.config.load_test.user_target_nat_balance * NAT_WEI_FACTOR

    assert root_xrp_balance > xrp_target * len(self.users), 'distributor has too little XRP balance'
    assert root_nat_balance > nat_target * len(self.users), 'distributor has too little NAT balance'

    xrp_min = self.params.config.load_test.user_min_xrp_balance * XRP_DROP_FACTOR
    nat_min = self.params.config.load_test.user_min_nat_balance * NAT_WEI_FACTOR

    for user in self.users:
      user_xrp_balance = self.ripple_rpc.get_balance(user.underlying_address)
      user_fxrp_balance = self.fasset.balance_of(user.native_address)
      if user_xrp_balance <= xrp_min and user_fxrp_balance <= xrp_min:
        fund = xrp_target - user_xrp_balance
        logger.info(f'funding user {user.user_id} with {fund} {self.params.asset_name}')
        self.ripple_root.send_tx(xrp_target - user_xrp_balance, user.underlying_address)
        logger.info(f'successfully funded user {user.user_id} with {fund} {self.params.asset_name}')
      user_nat_balance = self.native_rpc.get_balance(user.native_address)
      if user_nat_balance <= nat_min:
        fund = nat_target - user_nat_balance
        logger.info(f'funding user {user.user_id} with {fund} {self.params.native_token_name}')
        self.native_root.send_tx(fund, user.native_address)
        logger.info(f'successfully funded user {user.user_id} with {fund} {self.params.native_token_name}')

  def run_thread(self, i: int):
    while True:
      try:
        self.run_user_step(i)
      except Exception as e:
        logger.error(f'error when running user {i}:', e)
      sleep(self.params.config.load_test.cycle_sleep_secs)

  def run_user_step(self, i: int):
    user = self.users[i]
    agent_vault = choice(self.params.load_test_agent_vaults)
    user.mint(agent_vault, MAX_MINTED_LOTS)
    user.redeem_all()

  def on_finish(self):
    for user in self.users:
      user.redeem_all()

