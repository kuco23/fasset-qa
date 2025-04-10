from typing import List
from re import findall


class CmdParser:
  _hex_address_re = '0x[a-fA-F\d]{40}'
  _decimal_num_re = '\d*\.\d*'
  _integer_re = '\d+'

  @staticmethod
  def _ensure_parser_response(output: str) -> object:
    assert not output.err, f'could not parse {output.origin}'
    return output.resp

  @classmethod
  def _standardize_regex_output(cls, rgxs: List[str], msg: str) -> List[str]:
    parses = []
    for rgx in rgxs:
      parses.extend(findall(rgx, msg))
    return cls.flatten(parses)

  @staticmethod
  def flatten(xss):
    resp = []
    for x in xss:
      if isinstance(x, tuple):
        resp.extend(x)
      else:
        resp.append(x)
    return resp