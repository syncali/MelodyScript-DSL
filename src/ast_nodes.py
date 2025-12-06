from dataclasses import dataclass
from typing import List, Optional

from src.tokens import TokenType


class Node:
    pass


@dataclass
class NumberNode(Node):
    value: int


@dataclass
class IdentifierNode(Node):
    name: str


@dataclass
class NoteNode(Node):
    name: str


@dataclass
class BinOpNode(Node):
    left: Node
    operator: TokenType
    right: Node


@dataclass
class VarDeclNode(Node):
    var_type: TokenType
    name: str
    value: Node


@dataclass
class AssignmentNode(Node):
    name: str
    value: Node


@dataclass
class PlayNode(Node):
    note: Node
    duration: Node


@dataclass
class BlockNode(Node):
    statements: List[Node]
