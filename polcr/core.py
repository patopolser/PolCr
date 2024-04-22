from .lexer import *
from .parser import *
from .interpreter import *

FUNCTIONS = {
    "pout": BuiltInFunction("print"),
    "pin": BuiltInFunction("input"),
    "pin_int": BuiltInFunction("input_int"),
    "limpiar": BuiltInFunction("clear"),
    "es_numero": BuiltInFunction("is_number"),
    "es_string": BuiltInFunction("is_string"),
    "es_lista": BuiltInFunction("is_list"),
    "es_funcion": BuiltInFunction("is_function"),
    "redonder": BuiltInFunction("round"),
    "entero": BuiltInFunction("to_int")
}

symbol_table = SymbolTable()
[symbol_table.set(i, FUNCTIONS[i]) for i in FUNCTIONS]

def run(file_name: str, text: str):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    
    if error:   
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error: 
        return None, ast.error

    interpreter = Interpreter()
    context = Context('polser', symbol_table)
    result = interpreter.visit(ast.node, context)

    return result.value, result.error