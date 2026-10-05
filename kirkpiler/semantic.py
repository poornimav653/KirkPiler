from kirkpiler.ast import (
    NumberLiteral,
    Identifier,
    BinaryExpression,
    VariableDeclaration,
    Assignment,
    IfStatement,
)


class SemanticAnalyzer:
    def __init__(self):
        self.variables = set()

    def analyze(self, statements):
        for statement in statements:
            self.analyze_statement(statement)

    def analyze_statement(self, statement):

        if isinstance(statement, VariableDeclaration):
            if statement.name in self.variables:
                raise SemanticError(
                    f"Variable '{statement.name}' already declared"
                )

            self.variables.add(statement.name)
            self.analyze_expression(statement.value)

        elif isinstance(statement, Assignment):
            if statement.name not in self.variables:
                raise SemanticError(
                    f"Variable '{statement.name}' not declared"
                )

            self.analyze_expression(statement.value)

        elif isinstance(statement, IfStatement):
            self.analyze_expression(statement.condition)

            for statement_in_body in statement.body:
                self.analyze_statement(statement_in_body)

    def analyze_expression(self, expression):

        if isinstance(expression, NumberLiteral):
            return

        if isinstance(expression, Identifier):
            if expression.name not in self.variables:
                raise SemanticError(
                    f"Variable '{expression.name}' not declared"
                )

        elif isinstance(expression, BinaryExpression):
            self.analyze_expression(expression.left)
            self.analyze_expression(expression.right)


class SemanticError(Exception):
    pass