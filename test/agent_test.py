from qa_lib import Context

context = Context()

# 0x2087Bc949Fa84D0628E62e36c38d250E63c2A947
#context.agent_logic.create_agent('./config/vaults/vault1.json')
#context.agent_bot.deposit_agent_collaterals('0xC2C745DcEB7041520d8983397A42d4e116BC792C', 1)
#print([obj.vault_address for obj in context.database_manager.fetch_agents()])

#context.agent_bot.make_agent_available('0xC2C745DcEB7041520d8983397A42d4e116BC792C')

#print(context.asset_manager.maximum_transfer_to_core_vault('0xC2C745DcEB7041520d8983397A42d4e116BC792C'))
""" addr = context.agent_bot.create_agent('./config/vaults/vault2.json')
print(addr)
deposit_info = context.agent_bot.deposit_agent_collaterals(addr, 10)
print(deposit_info)
available = context.agent_bot.make_agent_available(addr)
print(available)
mint = context.user_bot.mint(7, addr)
print(mint) """

#max_trcv, _ = context.asset_manager.maximum_transfer_to_core_vault(addr)
""" trcv = context.agent_bot.transfer_to_core_vault('0x2087Bc949Fa84D0628E62e36c38d250E63c2A947', 90)
print(trcv) """