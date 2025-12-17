from typing import List
from time import sleep
from random import choice
from attrs import frozen
from qa_lib.utils import logger
from qa_lib.components.params import ParamLoader
from ..standalone import UserMinterAndRedeemer
from ...chain import RippleWallet, RippleClient, NativeWallet, NativeClient


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
  users: List[UserMinterAndRedeemer]

  def fund_users(self):
    root_xrp_balance = self.ripple_rpc.get_balance(self.ripple_root.wallet.address)
    root_nat_balance = self.native_rpc.get_balance(self.native_root.wallet.address)

    xrp_fund = self.params.config.load_test.user_xrp_fund * XRP_DROP_FACTOR
    nat_fund = self.params.config.load_test.user_nat_fund * NAT_WEI_FACTOR

    assert root_xrp_balance > xrp_fund * len(self.users), 'distributor has too little XRP balance'
    assert root_nat_balance > nat_fund * len(self.users), 'distributor has too little NAT balance'

    for user in self.users:
      user_xrp_balance = self.ripple_rpc.get_balance(user.underlying_address)
      if user_xrp_balance < xrp_fund:
        fund = xrp_fund - user_xrp_balance
        logger.info(f'funding user {user.user_id} with {fund} {self.params.asset_name}')
        self.ripple_root.send_tx(xrp_fund - user_xrp_balance, user.underlying_address)
        logger.info(f'successfully funded user {user.user_id} with {fund} {self.params.asset_name}')
      user_nat_balance = self.native_rpc.get_balance(user.native_address)
      if user_nat_balance < nat_fund:
        fund = nat_fund - user_nat_balance
        logger.info(f'funding user {user.user_id} with {fund} {self.params.native_token_name}')
        self.native_root.send_tx(fund, user.native_address)
        logger.info(f'successfully funded user {user.user_id} with {fund} {self.params.native_token_name}')

  def mint_redeem(self):
    while True:
      for user in self.users:
        agent_vault = choice(self.params.load_test_agent_vaults)
        user.mint(agent_vault, MAX_MINTED_LOTS)
        user.redeem_all()
      sleep(10)

  def withdraw_from_users(self):
    for user in self.users:
      user.redeem_all()

  def run(self):
    self.fund_users()
    self.mint_redeem()
    self.withdraw_from_users()

