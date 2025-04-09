from dataclasses import dataclass


@dataclass
class ParserOutput:
  resp: object
  origin: str
  err: bool