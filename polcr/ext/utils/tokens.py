from polcr.ext.utils.position import Position

TOKENS = {
    ';\n': 'NEWLINE',
    'INT':'INT',
    'FLOAT':'FLOAT',
    'STRING': 'STRING',

    '+':'PLUS',
    '-':'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '^': 'POW',
    '%': 'REST',

    '==': 'EQUALS_TO',
    '!=': 'NOT_EQUALS_TO',
    '<': 'LESS_THAN',
    '>': 'GREATER_THAN',
    '<=': 'LESS_EQ_THAN',
    '>=': 'GREATER_EQ_THAN',
    
    '(': 'LPAREN',
    ')': 'RPAREN',
    '[': 'LSQUARE',
    ']': 'RSQUARE',
    '=': 'EQ',
    ',': 'COMMA',
    '~>': 'ARROW',
    'IDENTIFIER': 'IDENTIFIER',
    'KEYWORD': 'KEYWORD',
    'EOF': 'EOF'
}

ARITHMETIC = {
    '+':'PLUS',
    '-':'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '^': 'POW',
    '%': 'REST',
}

COMPARISION = {
    '==': 'EQUALS_TO',
    '!=': 'NOT_EQUALS_TO',
    '<': 'LESS_THAN',
    '>': 'GREATER_THAN',
    '<=': 'LESS_EQ_THAN',
    '>=': 'GREATER_EQ_THAN',
}


EXCLUDE_TOKENS = ["<", ">", "<=", ">=", "=", ";\n"]

KEYWORDS = [
	'polser',
    "y",
    "o",
    "no",
    "si",
    "entonces",
    "sino_si",
    "sino",
    "desde",
	"hasta",
	"paso",
	"mientras",
    "funcion",
    "fin",
    "devolver",
    "continuar",
    "salir"
]

class Token:
    def __init__(self, type_: str, value: str = None, pos: Position = None):
        self.type = type_
        self.value = value
        self.pos = pos.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value
    
    def __repr__(self):
        if self.value: 
            return f'{self.type}:{self.value}'
            
        return f'{self.type}'