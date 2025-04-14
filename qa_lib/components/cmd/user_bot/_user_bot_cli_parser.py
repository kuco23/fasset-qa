from re import search
from ....utils import ParserOutput
from .._parser import CmdParser


class UserBotCliOutputParser(CmdParser):
  _user_minted_re_1 = r'Paying on the underlying chain for reservation (\d+?) to address (r[\w\d]+?)\.\.\.'
  _user_minted_re_2 = r'Waiting for proof of underlying payment transaction ([\w\d]+?)\.\.\.'
  _user_minted_re_match = 'Done'

  def parse_user_mint(self, msg: str) -> ParserOutput:
    done = search(self._user_minted_re_match, msg)
    parses = self._standardize_regex_output([self._user_minted_re_1, self._user_minted_re_2], msg)
    if not done or len(parses) != 3:
      return ParserOutput(resp=dict(), origin=msg, err=True)
    mint_id, agent_address, tx_hash = parses
    return ParserOutput(resp={
      'mint_id': int(mint_id),
      'agent_address': agent_address,
      'tx_hash': tx_hash
    }, origin=msg, err=False)