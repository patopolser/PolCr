from .ext import *

import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters + "ñÑ"
LETTERS_DIGITS = LETTERS + DIGITS

class Lexer:
    def __init__(self, file_name: str, text: str):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:

            if self.current_char in ' \t':
                self.advance()

            elif self.current_char in ";\n":
                tokens.append(Token(TOKENS[";\n"], pos= self.pos))
                self.advance()

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())

            elif self.current_char in TOKENS and self.current_char not in EXCLUDE_TOKENS:
                tokens.append(Token(TOKENS[self.current_char], pos= self.pos))
                self.advance()

            elif self.current_char == '!':
                token, error = self.make_not_equals()

                if error: 
                    return [], error

                tokens.append(token)

            elif self.current_char == '~':
                token, error = self.make_arrow()

                if error: 
                    return [], error

                tokens.append(token)


            elif self.current_char == '=':
                tokens.append(self.make_equals())

            elif self.current_char == '<':
                tokens.append(self.make_less_than())

            elif self.current_char == '>':
                tokens.append(self.make_greater_than())

            elif self.current_char == '"':
                tokens.append(self.make_string())

            else:
                return [], IllegalCharError(self.pos.copy(), "'" + str(self.current_char) + "'")

        tokens.append(Token(TOKENS["EOF"], pos= self.pos))
        return tokens, None

    def make_number(self) -> Token:
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TOKENS['INT'], int(num_str), self.pos)
        else:
            return Token(TOKENS['FLOAT'], float(num_str), self.pos)

    def make_identifier(self):        
        id_str = ""

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        token_type = TOKENS['KEYWORD'] if id_str in KEYWORDS else TOKENS['IDENTIFIER']
        return Token(token_type, id_str, self.pos)

    def make_arrow(self):
        pos = self.pos.copy()
        self.advance()

        if self.current_char == '>':
            self.advance()
            return Token(TOKENS["~>"], pos= pos), None

        self.advance()

        return None, ExpectedCharError(self.pos, "'>' (after '~')")

    def make_not_equals(self):
        pos = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TOKENS["!="], pos= pos), None

        self.advance()

        return None, ExpectedCharError(self.pos, "'=' (after '!')")
    
    def make_equals(self):
        token_type = TOKENS["="]
        pos = self.pos.copy()
        self.advance()
        
        if self.current_char == '=':
            self.advance()
            token_type = TOKENS["=="]

        return Token(token_type, pos= pos)

    def make_less_than(self):
        token_type = TOKENS["<"]
        pos = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = TOKENS["<="]

        return Token(token_type, pos= pos)

    def make_greater_than(self):
        token_type = TOKENS[">"]
        pos = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = TOKENS[">="]

        return Token(token_type, pos= pos)

    def make_string(self):
        string = ''
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):

            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)

            else:
                if self.current_char == '\\':
                    escape_character = True

                else:
                    string += self.current_char

            self.advance()
            escape_character = False
        
        self.advance()
        return Token(TOKENS["STRING"], string, self.pos)