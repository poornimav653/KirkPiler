from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()

    # Names
    IDENTIFIER = auto()
    PIN = auto()

    # Keywords
    PIN_KW = auto()
    UART = auto()
    FN = auto()
    LET = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    INT = auto()
    BOOL = auto()
    INPUT = auto()
    OUTPUT = auto()

    # Symbols
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()

    # Operators
    EQUAL = auto()
    ARROW = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()

    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()

    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    AND_AND = auto()
    OR_OR = auto()
    NOT = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: object
    line: int
    column: int