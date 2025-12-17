from .._parser import CmdParser
from ....utils import ParserOutput
from ._agent_bot_cli_types import (
  CliAgentVaultCreatedResponse, CliCollateralsDepositedResponse,
  CliAgentAvailableResponse, CliRequestTransferToCoreVaultResponse
)

class AgentBotCliOutputParser(CmdParser):
  _agent_created_re = rf'AGENT CREATED: Agent ({CmdParser._hex_address_re}) was created.'
  _deposit_collaterals_re = (
    rf'VAULT COLLATERAL DEPOSIT: Deposit of ({CmdParser._decimal_num_re}) (.+?) vault collateral tokens to agent ({CmdParser._hex_address_re}) was successful.\n'
    rf'BUY POOL TOKENS: Agent ({CmdParser._hex_address_re}) bought ({CmdParser._decimal_num_re}) (.+?) worth of pool tokens successfully.'
  )
  _enter_available_re = rf'AGENT ENTERED AVAILABLE: Agent ({CmdParser._hex_address_re}) entered available list'
  _transfer_to_core_vault_re = rf'TRANSFER TO CORE VAULT STARTED: Transfer to core vault ({CmdParser._integer_re}) started for ({CmdParser._hex_address_re})'

  def parse_agent_creation(self, msg: str) -> ParserOutput[CliAgentVaultCreatedResponse]:
    parsed = self._standardize_regex_output([self._agent_created_re], msg)
    if len(parsed) != 1: return ParserOutput(None, msg, True)
    return ParserOutput(CliAgentVaultCreatedResponse(*parsed), msg, False)

  def parse_deposit_agent_collaterals(self, msg: str) -> ParserOutput[CliCollateralsDepositedResponse]:
    parsed = self._standardize_regex_output([self._deposit_collaterals_re], msg)
    if len(parsed) != 6: return ParserOutput(None, msg, True)
    return ParserOutput(CliCollateralsDepositedResponse(*parsed), msg, False)

  def parse_agent_available(self, msg: str) -> ParserOutput[CliAgentAvailableResponse]:
    parsed = self._standardize_regex_output([self._enter_available_re], msg)
    if len(parsed) != 1: return ParserOutput(None, msg, True)
    return ParserOutput(CliAgentAvailableResponse(*parsed), msg, False)

  def parse_request_transfer_to_core_vault(self, msg: str) -> ParserOutput[CliRequestTransferToCoreVaultResponse]:
    parsed = self._standardize_regex_output([self._transfer_to_core_vault_re], msg)
    if len(parsed) != 2: return ParserOutput(None, msg, True)
    return ParserOutput(CliRequestTransferToCoreVaultResponse(*parsed), msg, False)