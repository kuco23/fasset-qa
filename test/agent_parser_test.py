from qa_lib import DependencyManager


AGENT_CREATED_RESPONSE = """
Validating new underlying address rKviPRd33ss5XBCqEWCNb6SuN9Uym5GR8E...
Owner 0x8be281772F7af7FaCe0b9bf298b0A33BF57081f9 with work address 0x36f02a759dFb1aAa4099addfA79D807519A88AAd validating new underlying address rKviPRd33ss5XBCqEWCNb6SuN9Uym5GR8E.
AGENT CREATION UNDERLYING ADDRESS VALIDATION: Validating underlying address for new agent vault. This will take a few minutes.
Stopping wallet monitoring testXRP-m-67e50ede9834f3fd ...
AGENT CREATION UNDERLYING ADDRESS VALIDATION: Succesfully validated underlying address for new agent vault.
Creating agent bot...
CREATING AGENT: Creating new agent vault.
AGENT CREATED: Agent 0xC2C745DcEB7041520d8983397A42d4e116BC792C was created.
Agent bot created.
Owner 0x8be281772F7af7FaCe0b9bf298b0A33BF57081f9 with work address 0x36f02a759dFb1aAa4099addfA79D807519A88AAd created new agent vault at 0xC2C745DcEB7041520d8983397A42d4e116BC792C
"""

COLLATERALS_DEPOSIT_RESPONSE = """
VAULT COLLATERAL DEPOSIT: Deposit of 63.024068 testUSDC vault collateral tokens to agent 0xC2C745DcEB7041520d8983397A42d4e116BC792C was successful.
BUY POOL TOKENS: Agent 0xC2C745DcEB7041520d8983397A42d4e116BC792C bought 20947.608036977388419538 WCFLR worth of pool tokens successfully.
"""

AGENT_ENTERED_AVAILABLE_RESPONSE = """
AGENT ENTERED AVAILABLE: Agent 0xC2C745DcEB7041520d8983397A42d4e116BC792C entered available list.
"""

REQUEST_TRANSFER_TO_CORE_VAULT_RESPONSE = """
TRANSFER TO CORE VAULT STARTED: Transfer to core vault 1898544 started for 0x2087Bc949Fa84D0628E62e36c38d250E63c2A947.
"""

context = DependencyManager()

agent_created = context.agent_bot_cli.parse_agent_creation(AGENT_CREATED_RESPONSE)
assert agent_created.err is False
assert agent_created.origin == AGENT_CREATED_RESPONSE
assert agent_created.resp['agent_vault'] == '0xC2C745DcEB7041520d8983397A42d4e116BC792C'

collaterals_deposited = context.agent_bot_cli.parse_deposit_agent_collaterals(COLLATERALS_DEPOSIT_RESPONSE)
assert collaterals_deposited.err is False
assert collaterals_deposited.origin == COLLATERALS_DEPOSIT_RESPONSE
assert collaterals_deposited.resp['agent_vault'] == '0xC2C745DcEB7041520d8983397A42d4e116BC792C'
assert collaterals_deposited.resp['vault_token'] == 'testUSDC'
assert collaterals_deposited.resp['vault_amount'] == 63.024068
assert collaterals_deposited.resp['native_token'] == 'WCFLR'
assert collaterals_deposited.resp['native_amount'] == 20947.608036977388419538

agent_entered_available = context.agent_bot_cli.parse_agent_available(AGENT_ENTERED_AVAILABLE_RESPONSE)
assert agent_entered_available.err is False
assert agent_entered_available.origin == AGENT_ENTERED_AVAILABLE_RESPONSE
assert agent_entered_available.resp['agent_vault'] == '0xC2C745DcEB7041520d8983397A42d4e116BC792C'

agent_transfer_to_core_vault = context.agent_bot_cli.parse_request_transfer_to_core_vault(REQUEST_TRANSFER_TO_CORE_VAULT_RESPONSE)
assert agent_transfer_to_core_vault.err is False
assert agent_transfer_to_core_vault.origin == REQUEST_TRANSFER_TO_CORE_VAULT_RESPONSE
assert agent_transfer_to_core_vault.resp['redemption_id'] == 1898544
assert agent_transfer_to_core_vault.resp['agent_vault'] == '0x2087Bc949Fa84D0628E62e36c38d250E63c2A947'