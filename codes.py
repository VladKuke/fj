'<' + '+ -' + '*'

'''
<expression> ::= <less> EOF ;

<less>       ::= <plus_minus> { "<" <plus_minus> } ;

<plus_minus> ::= <multiplication> { ("+" | "-") <multiplication> } ;

<multiplication> ::= <factor> { "*" <factor> } ;

<factor>     ::= NUMBER | "(" <less> ")" ;
'''

def parse(self):
        result = self.less()
        if self.current_token.type != TokenType.EOF:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
        return result

    def less(self):
        result = self.plus_minus()
        while self.current_token.type == TokenType.LESS:
            self.consume(TokenType.LESS)
            result = 1 if result < self.plus_minus() else 0
        return result

    def plus_minus(self):
        result = self.nasobenie()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.consume(TokenType.PLUS)
                result += self.nasobenie()
            else:
                self.consume(TokenType.MINUS)
                result -= self.nasobenie()
        return result

    def nasobenie(self):
        result = self.factor()
        while self.current_token.type == TokenType.TIMES:
            self.consume(TokenType.TIMES)
            result *= self.factor()
        return result


    def factor(self):
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.attribute
            self.consume(TokenType.NUMBER)
            return value
        elif self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            result = self.less()
            self.consume(TokenType.RPAREN)
            return result
        else:
            raise SyntaxError(f"Unexpected token{self.current_token}")

from Lexer import TokenType

# reverse (R)(3), concat(2), степень со строчкой(1)


'''
<expression> ::= <power> EOF ;

<power> ::= <concat> { "^" <concat> } ;

<concat> ::= <reverse> { "." <reverse> } ;

<reverse> ::= "R" <reverse> | <atom> ;

<atom> ::= STRING | NUMBER | "(" <power> ")" ;
'''

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def consume(self, expected_token_type):
        if self.current_token.type == expected_token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(
                f"Syntax error: expected token type {expected_token_type}, but found token type {self.current_token.type}"
            )

    def parse(self):
        result = self.power()
        if self.current_token.type != TokenType.EOF:
            raise SyntaxError("jfenjfnef")
        return result

    def power(self):
        result = self.concat()
        while self.current_token.type == TokenType.POWER:
            self.consume(TokenType.POWER)
            result *= self.concat()
        return result

    def concat(self):
        result = self.reverse()
        while self.current_token.type == TokenType.CONCAT:
            self.consume(TokenType.CONCAT)
            result = str(result) + str(self.reverse())
        return result

    def reverse(self):
        if self.current_token.type == TokenType.INVERT:
            self.consume(TokenType.INVERT)
            result = self.reverse()[::-1]
            return result
        else:
            return self.last()


    def last(self):
        if self.current_token.type == TokenType.STRING:
            value = self.current_token.attribute
            self.consume(TokenType.STRING)
            return value
        elif self.current_token.type == TokenType.NUMBER:
            value = self.current_token.attribute
            self.consume(TokenType.NUMBER)
            return value
        elif self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            result = self.power()
            self.consume(TokenType.RPAREN)
            return result
        else:
            raise SyntaxError("kenkenfiefk")


from Lexer import TokenType

'''
expr         ::= implication ;

implication  ::= neg_expr [ "=>" implication ] ;

neg_expr     ::= "~" neg_expr | or_expr ;

or_expr      ::= and_expr { "|" and_expr } ;

and_expr     ::= last { "&" last } ;

last         ::= "true" | "false" | "(" expr ")" ;

'''

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        try:
            self.current_token = self.lexer.next_token()
        except ValueError as e:
            raise SyntaxError(str(e))

    def consume(self, expected_token_type):
        if self.current_token.type == expected_token_type:
            try:
                self.current_token = self.lexer.next_token()
            except ValueError as e:
                raise SyntaxError(str(e))
        else:
            raise SyntaxError(
                f"Syntax error: expected token type {expected_token_type}, "
                f"but found token type {self.current_token.type}"
            )

    def parse(self):
        result = self.parse_impl()
        if self.current_token.type != TokenType.EOF:
            raise SyntaxError(f"Syntax error: expected EOF, but found {self.current_token.type}")
        return result

    def parse_impl(self):
        left = self.parse_neg()
        if self.current_token.type == TokenType.IMPL:
            self.consume(TokenType.IMPL)
            right = self.parse_impl()
            return (not left) or right
        return left

    def parse_neg(self):
        if self.current_token.type == TokenType.NEG:
            self.consume(TokenType.NEG)
            return not self.parse_neg()
        else:
            return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.current_token.type == TokenType.OR:
            self.consume(TokenType.OR)
            right = self.parse_and()
            left = left or right
        return left

    def parse_and(self):
        left = self.last()
        while self.current_token.type == TokenType.AND:
            self.consume(TokenType.AND)
            right = self.last()
            left = left and right
        return left

    def last(self):
        if self.current_token.type == TokenType.CONST:
            value = self.current_token.attribute
            self.consume(TokenType.CONST)
            return value == "true"
        elif self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            value = self.parse_impl()
            self.consume(TokenType.RPAREN)
            return value
        else:
            raise SyntaxError(
                f"Syntax error: expected token type TokenType.CONST or TokenType.LPAREN, "
                f"but found token type {self.current_token.type}"
            )

        from enum import Enum, auto

        class TokenType(Enum):
            A = auto()
            B = auto()
            C = auto()
            EOF = auto()

        class Token:
            def __init__(self, type):
                self.type = type

        class Lexer:
            def __init__(self, input_text):
                self.input = input_text
                self.pos = 0

            def get_next_token(self):
                if self.pos >= len(self.input):
                    return Token(TokenType.EOF)

                char = self.input[self.pos]
                self.pos += 1

                if char == 'a':
                    return Token(TokenType.A)
                elif char == 'b':
                    return Token(TokenType.B)
                elif char == 'c':
                    return Token(TokenType.C)
                else:
                    raise ValueError(f"Invalid character: {char}")

        class DKA:
            def __init__(self):
                self.lexer = None
                self.current_token = None

            def consume(self, expected_type):
                if self.current_token.type == expected_type:
                    self.current_token = self.lexer.get_next_token()
                else:
                    raise SyntaxError(f"Expected {expected_type}, got {self.current_token.type}")

            def check(self, word):
                try:
                    self.lexer = Lexer(word)
                    self.current_token = self.lexer.get_next_token()
                    if len(word) == 0:
                        return False

                    self.rec()

                    if self.current_token.type != TokenType.B:
                        return False
                    self.consume(TokenType.B)

                    return self.current_token.type == TokenType.EOF

                except (SyntaxError, ValueError):
                    return False

            def rec(self):
                if self.lexer.pos >= len(self.lexer.input):
                    return

                if self.current_token.type == TokenType.A:
                    self.consume(TokenType.A)
                    if self.current_token.type != TokenType.B:
                        return False
                    self.consume(TokenType.B)
                elif self.current_token.type == TokenType.C:
                    self.consume(TokenType.C)
                    if self.current_token.type == TokenType.A:
                        self.consume(TokenType.A)
                else:
                    raise SyntaxError(f"Expected {TokenType.A}, got {self.current_token.type}")

                self.rec()