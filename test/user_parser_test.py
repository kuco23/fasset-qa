from qa_lib import Context


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

USER_REDEEM_FROM_CORE_VALT = '''
Asking for redemption from core vault of 10 lots
Asked for redemption of 10 from core vault.
'''

context = Context()

user_minted = context.user_bot.parse_user_mint(USER_MINTED_RESP)
assert user_minted.err is False
assert user_minted.origin == USER_MINTED_RESP
assert user_minted.resp['mint_id'] == 1968972
assert user_minted.resp['agent_address'] == 'rKviPRd33ss5XBCqEWCNb6SuN9Uym5GR8E'
assert user_minted.resp['tx_hash'] == '79F6B66F6038FBD034FFCBBE1D0F8000B59C63227A9979C8C61F5888FC67BDCB'

user_redeem_from_core_vault = context.user_bot.parse_user_redeem_from_core_vault(USER_REDEEM_FROM_CORE_VALT)
assert user_redeem_from_core_vault.err is False
assert user_redeem_from_core_vault.origin == USER_REDEEM_FROM_CORE_VALT
assert user_redeem_from_core_vault.resp['lots'] == 10