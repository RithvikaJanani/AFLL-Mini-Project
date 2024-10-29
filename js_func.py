import ply.lex as lex
import ply.yacc as yacc

# ============= LEXER ====================

# List of token names
tokens = [
    'FUNCTION', 'ID', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMA', 'NUMBER', 'STRING', 'SEMICOLON'
]

# Token definitions for function declaration
def t_FUNCTION(t):
    r'function'
    return t

# Regular expression for identifiers (function names, parameters)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','

# Token for number literals
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Token for string literals (single and double quotes)
def t_STRING(t):
    r'\".*?\"|\'(.*?)\''
    t.value = t.value[1:-1]  # Strip the quotes
    return t

# Ignoring spaces and tabs
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# ============= PARSER ====================

# Parsing rules for JavaScript function declarations
def p_function_declaration(p):
    '''function_declaration : FUNCTION ID LPAREN params RPAREN LBRACE RBRACE'''
    print(f"Parsed function declaration: {p[2]}({p[4]}) {{ }}")

def p_params(p):
    '''params : ID
              | ID COMMA params
              | empty'''
    if len(p) == 2:  # Only one parameter
        p[0] = p[1]  # Single parameter
    elif len(p) == 4:  # Multiple parameters
        p[0] = f"{p[1]}, {p[3]}"  # Combine parameters
    else:
        p[0] = ''  # No parameters

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    if p is None:
        print("Syntax error at EOF")
    else:
        print(f"Syntax error at '{p.value}'")

# Build the parser
parser = yacc.yacc()

# ============= MAIN LOOP ====================
while True:
    try:
        s = input('Enter JavaScript function declaration: ')
    except EOFError:
        break
    if not s: continue
    print(f"Input: '{s}'")
    lexer.input(s)  # Feed input to lexer
    for token in lexer:
        print(f"Token: {token.type}, Value: {token.value}")
    parser.parse(s)  # Parse the input
