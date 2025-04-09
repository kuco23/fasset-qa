from qa_lib import Context

context = Context()

context.agent_logic.create_agent('./config/vaults/vault1.json')
#context.agent_bot.deposit_agent_collaterals('0xC2C745DcEB7041520d8983397A42d4e116BC792C', 1)
#print([obj.vault_address for obj in context.database_manager.fetch_agents()])

#context.agent_bot.make_agent_available('0xC2C745DcEB7041520d8983397A42d4e116BC792C')

#context.agent_bot.transfer_to_core_vault('0xC2C745DcEB7041520d8983397A42d4e116BC792C')

#context.agent_bot.transfer_to_core_vault('0xC2C745DcEB7041520d8983397A42d4e116BC792C', 30.176514)