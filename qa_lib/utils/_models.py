from typing import TypeVar, Generic
from abc import ABC
from dataclasses import dataclass

class ParserResponse(ABC):
    pass

T = TypeVar("T", bound=ParserResponse)

@dataclass
class ParserOutput(Generic[T]):
  resp: T
  origin: str
  err: bool