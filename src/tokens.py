from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    INT_KW = auto()
    NOTE_KW = auto()
    STRING_KW = auto()
    REPEAT_KW = auto()
    IF_KW = auto()
    ELSE_KW = auto()
    PLAY_KW = auto()
    REST_KW = auto()
    ID = auto()
    NUM = auto()
    NOTE_VAL = auto()
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    GT = auto()
    LT = auto()
    EQUALS = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMI = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
