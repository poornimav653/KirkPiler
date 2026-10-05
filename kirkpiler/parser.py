from kirkpiler.tokens import TokenType
from kirkpiler.ast import (
    NumberLiteral,
    Identifier,
    BinaryExpression,
    VariableDeclaration,
    Assignment,
    IfStatement,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current_token()
        self.position += 1
        return token

    def expect(self, token_type):
        token = self.current_token()

        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, "
                f"but got {token.type} "
                f"at {token.line}:{token.column}"
            )

        return self.advance()

    def parse(self):
        statements = []

        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())

        return statements
    
    def parse_assignment(self):
    # Read variable name
        name_token = self.expect(TokenType.IDENTIFIER)

    # Consume '='
        self.expect(TokenType.EQUAL)

    # Parse the value
        value = self.parse_expression()

    # Consume ';'
        self.expect(TokenType.SEMICOLON)

        return Assignment(
            name_token.value,
            value
        )





    def parse_statement(self):
        if self.current_token().type == TokenType.LET:
            return self.parse_variable_declaration()

        if self.current_token().type==TokenType.IF:
            return self.parse_if_statement()
        if self.current_token().type==TokenType.IDENTIFIER:
            return self.parse_assignment()

        raise SyntaxError(
            f"Unexpected token "
            f"{self.current_token().type}"
        )
    def parse_if_statement(self):
        self.expect(TokenType.IF)

        condition = self.parse_expression()
        self.expect(TokenType.LEFT_BRACE)

    # Parse statements inside the block
        body = []

        while self.current_token().type != TokenType.RIGHT_BRACE:
            body.append(self.parse_statement())

    # Consume '}'
        self.expect(TokenType.RIGHT_BRACE)

        return IfStatement(
            condition,
            body
        )

    def parse_variable_declaration(self):
        self.expect(TokenType.LET)

        name_token = self.expect(TokenType.IDENTIFIER)

        self.expect(TokenType.EQUAL)

        value = self.parse_expression()

        self.expect(TokenType.SEMICOLON)

        return VariableDeclaration(
            name_token.value,
            value
        )

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        expression = self.parse_term()

        while self.current_token().type in (
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.EQUAL_EQUAL,
        ):
            operator = self.advance()

            right = self.parse_term()

            expression = BinaryExpression(
                expression,
                operator.value,
                right
            )

        return expression

    def parse_term(self):
        expression = self.parse_factor()

        while self.current_token().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self.advance()

            right = self.parse_factor()

            expression = BinaryExpression(
                expression,
                operator.value,
                right
            )

        return expression

    def parse_factor(self):
        expression = self.parse_primary()

        while self.current_token().type in (
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.PERCENT,
        ):
            operator = self.advance()

            right = self.parse_primary()

            expression = BinaryExpression(
                expression,
                operator.value,
                right
            )

        return expression

    def parse_primary(self):
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberLiteral(token.value)

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value)

        if token.type == TokenType.LEFT_PAREN:
            self.advance()

            expression = self.parse_expression()

            self.expect(TokenType.RIGHT_PAREN)

            return expression

        raise SyntaxError(
            f"Expected expression, "
            f"but got {token.type} "
            f"at {token.line}:{token.column}"
        )