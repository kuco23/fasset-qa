from qa_lib import DependencyManager
from qa_lib.components.cmd import UserBotCliOutputParser


USER_MINTED_RESP = '''
Reserving collateral...
Paying on the underlying chain for reservation 1968972 to address rKviPRd33ss5XBCqEWCNb6SuN9Uym5GR8E...
Stopping wallet monitoring testXRP-m-ef8525a4bc1a277a ...
Waiting for transaction finalization...
Waiting for proof of underlying payment transaction 79F6B66F6038FBD034FFCBBE1D0F8000B59C63227A9979C8C61F5888FC67BDCB...
Executing payment...
Done
Initializing environment...
Environment successfully initialized.
'''

USER_REDEEMED_RESP = '''
Asking for redemption of 4 lots
Triggered 1 payment requests (addresses, block numbers and timestamps are on underlying chain):
    id=96848  to=rEwx9TT3cHJ7cg3EtdtCm4aei9iduDFpqa  amount=39800000  agentVault=0x55c815260cBE6c45Fe5bFe5FF32E3C7D746f14dC  reference=0x4642505266410002000000000000000000000000000000000000000000017a50  firstBlock=13255207  lastBlock=13255716  lastTimestamp=1765895161
Initializing environment...
Environment successfully initialized.
'''

USER_REDEEM_FROM_CORE_VALT = '''
Asking for redemption from core vault of 10 lots
Asked for redemption of 10 from core vault.
'''

context = DependencyManager()

cli: UserBotCliOutputParser = context.simple_user_bots[0].user_bot_cli

user_minted = cli.parse_user_mint(USER_MINTED_RESP)
assert user_minted.err is False
assert user_minted.origin == USER_MINTED_RESP
assert user_minted.resp['mint_id'] == 1968972
assert user_minted.resp['agent_address'] == 'rKviPRd33ss5XBCqEWCNb6SuN9Uym5GR8E'
assert user_minted.resp['tx_hash'] == '79F6B66F6038FBD034FFCBBE1D0F8000B59C63227A9979C8C61F5888FC67BDCB'

user_redeemed = cli.parse_user_redeem(USER_REDEEMED_RESP)
assert user_redeemed.err is False
assert user_redeemed.origin == USER_REDEEMED_RESP
assert user_redeemed.resp['redemption_id'] == 96848
assert user_redeemed.resp['redeemer'] == 'rEwx9TT3cHJ7cg3EtdtCm4aei9iduDFpqa'
assert user_redeemed.resp['amount'] == 39800000
assert user_redeemed.resp['agent_vault'] == '0x55c815260cBE6c45Fe5bFe5FF32E3C7D746f14dC'
assert user_redeemed.resp['reference'] == '0x4642505266410002000000000000000000000000000000000000000000017a50'

user_redeem_from_core_vault = cli.parse_user_redeem_from_core_vault(USER_REDEEM_FROM_CORE_VALT)
assert user_redeem_from_core_vault.err is False
assert user_redeem_from_core_vault.origin == USER_REDEEM_FROM_CORE_VALT
assert user_redeem_from_core_vault.resp['lots'] == 10

