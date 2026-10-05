from dataclasses import dataclass


class ASTNode:
    pass


@dataclass
class NumberLiteral(ASTNode):
    value: int


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class BinaryExpression(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class VariableDeclaration(ASTNode):
    name: str
    value: ASTNode

@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    body: list