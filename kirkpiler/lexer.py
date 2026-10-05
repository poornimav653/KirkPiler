from kirkpiler.tokens import Token, TokenType


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def current_char(self):
        if self.position >= len(self.source):
            return "\0"

        return self.source[self.position]

    def peek(self):
        if self.position + 1 >= len(self.source):
            return "\0"

        return self.source[self.position + 1]

    def advance(self):
        char = self.current_char()

        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def tokenize(self):
        tokens = []

        while self.current_char() != "\0":
            char = self.current_char()

            # Ignore spaces and tabs
            if char in " \t\r":
                self.advance()
                continue

            # New line
            if char == "\n":
                self.advance()
                continue

            # Number
            if char.isdigit():
                tokens.append(self.read_number())
                continue

            # Identifier or keyword
            if char.isalpha() or char == "_":
                tokens.append(self.read_identifier())
                continue

            # Single-character tokens
            if char == "+":
                tokens.append(
                    Token(TokenType.PLUS, "+", self.line, self.column)
                )
                self.advance()
                continue

            if char == "-":
                tokens.append(
                    Token(TokenType.MINUS, "-", self.line, self.column)
                )
                self.advance()
                continue

            if char == "*":
                tokens.append(
                    Token(TokenType.STAR, "*", self.line, self.column)
                )
                self.advance()
                continue

            if char == "/":
                tokens.append(
                    Token(TokenType.SLASH, "/", self.line, self.column)
                )
                self.advance()
                continue

            if char == "%":
                tokens.append(
                    Token(TokenType.PERCENT, "%", self.line, self.column)
                )
                self.advance()
                continue

            # Equal / Equal Equal
            if char == "=":
                start_line = self.line
                start_column = self.column

                if self.peek() == "=":
                    self.advance()
                    self.advance()

                    tokens.append(
                        Token(
                            TokenType.EQUAL_EQUAL,
                            "==",
                            start_line,
                            start_column
                        )
                    )
                else:
                    tokens.append(
                        Token(
                            TokenType.EQUAL,
                            "=",
                            start_line,
                            start_column
                        )
                    )
                    self.advance()

                continue

            # Greater / Greater Equal
            if char == ">":
                start_line = self.line
                start_column = self.column

                if self.peek() == "=":
                    self.advance()
                    self.advance()

                    tokens.append(
                        Token(
                            TokenType.GREATER_EQUAL,
                            ">=",
                            start_line,
                            start_column
                        )
                    )
                else:
                    tokens.append(
                        Token(
                            TokenType.GREATER,
                            ">",
                            start_line,
                            start_column
                        )
                    )
                    self.advance()

                continue

            # Less / Less Equal
            if char == "<":
                start_line = self.line
                start_column = self.column

                if self.peek() == "=":
                    self.advance()
                    self.advance()

                    tokens.append(
                        Token(
                            TokenType.LESS_EQUAL,
                            "<=",
                            start_line,
                            start_column
                        )
                    )
                else:
                    tokens.append(
                        Token(
                            TokenType.LESS,
                            "<",
                            start_line,
                            start_column
                        )
                    )
                    self.advance()

                continue

            if char == ";":
                tokens.append(
                    Token(TokenType.SEMICOLON, ";", self.line, self.column)
                )
                self.advance()
                continue

            if char == "(":
                tokens.append(
                    Token(TokenType.LEFT_PAREN, "(", self.line, self.column)
                )
                self.advance()
                continue

            if char == ")":
                tokens.append(
                    Token(TokenType.RIGHT_PAREN, ")", self.line, self.column)
                )
                self.advance()
                continue

            if char == "{":
                tokens.append(
                    Token(TokenType.LEFT_BRACE, "{", self.line, self.column)
                )
                self.advance()
                continue

            if char == "}":
                tokens.append(
                    Token(TokenType.RIGHT_BRACE, "}", self.line, self.column)
                )
                self.advance()
                continue

            # Unknown character
            raise SyntaxError(
                f"Unexpected character '{char}' "
                f"at {self.line}:{self.column}"
            )

        tokens.append(
            Token(TokenType.EOF, None, self.line, self.column)
        )

        return tokens

    def read_number(self):
        start_line = self.line
        start_column = self.column

        digits = ""

        while self.current_char().isdigit():
            digits += self.advance()

        return Token(
            TokenType.NUMBER,
            int(digits),
            start_line,
            start_column
        )

    def read_identifier(self):
        start_line = self.line
        start_column = self.column

        text = ""

        while (
            self.current_char().isalnum()
            or self.current_char() == "_"
        ):
            text += self.advance()

        keywords = {
            "let": TokenType.LET,
            "fn": TokenType.FN,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "return": TokenType.RETURN,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "int": TokenType.INT,
            "bool": TokenType.BOOL,
            "input": TokenType.INPUT,
            "output": TokenType.OUTPUT,
            "uart": TokenType.UART,
            "pin": TokenType.PIN_KW,
        }

        token_type = keywords.get(
            text,
            TokenType.IDENTIFIER
        )

        return Token(
            token_type,
            text,
            start_line,
            start_column
        )