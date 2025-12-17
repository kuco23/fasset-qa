from re import search
from ....utils import ParserOutput
from .._parser import CmdParser
from ._user_bot_cli_types import CliMintResponse, CliRedeemResponse, CliRedeemFromCoreVaultResponse

class UserBotCliOutputParser(CmdParser):
  _user_minted_re_1 = r'Paying on the underlying chain for reservation (\d+?) to address (r[\w\d]+?)\.\.\.'
  _user_minted_re_2 = r'Waiting for proof of underlying payment transaction ([\w\d]+?)\.\.\.'
  _user_minted_re_match = 'Done'
  _user_redeem_re_1 = (
    r"id=(\d+)\s+"
    r"to=(r[A-Za-z0-9]+)\s+"
    r"amount=(\d+)\s+"
    r"agentVault=(0x[0-9a-fA-F]+)\s+"
    r"reference=(0x[0-9a-fA-F]+)"
  )
  _user_redeem_from_core_vault = r'Asked for redemption of (\d+?) from core vault.'

  def parse_user_mint(self, msg: str) -> ParserOutput[CliMintResponse]:
    done = search(self._user_minted_re_match, msg)
    parses = self._standardize_regex_output([self._user_minted_re_1, self._user_minted_re_2], msg)
    if not done or len(parses) != 3: return ParserOutput(None, msg, True)
    return ParserOutput(CliMintResponse(*parses), msg, False)

  def parse_user_redeem(self, msg: str) -> ParserOutput[CliRedeemResponse]:
    parses = self._standardize_regex_output([self._user_redeem_re_1], msg)
    if len(parses) != 5: return ParserOutput(None, msg, True)
    return ParserOutput(CliRedeemResponse(*parses), msg, False)

  def parse_user_redeem_from_core_vault(self, msg: str) -> ParserOutput[CliRedeemFromCoreVaultResponse]:
    parses = self._standardize_regex_output([self._user_redeem_from_core_vault], msg)
    if len(parses) != 1: return ParserOutput(None, msg, True)
    return ParserOutput(CliRedeemFromCoreVaultResponse(*parses), msg, False)