import ply.lex as lex
import ply.yacc as yacc

# ============= LEXER ====================

# List of token names
tokens = [
    'VAR', 'LET', 'CONST',  # JavaScript variable types
    'ID', 'ASSIGN', 'NUMBER', 'STRING', 'BOOLEAN', 'SEMICOLON'
]

# Token definitions for variable types in JavaScript
def t_VAR(t):
    r'var'
    return t

def t_LET(t):
    r'let'
    return t

def t_CONST(t):
    r'const'
    return t

t_ASSIGN = r'='
t_SEMICOLON = r';'

# Token for boolean literals
def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == "true" else False
    return t

# Regular expression for identifiers (variable names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Token for number literals (including integers and decimals)
def t_NUMBER(t):
    r'\d+(\.\d+)?'  # Allows for integers and decimal numbers
    t.value = float(t.value) if '.' in t.value else int(t.value)
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

# Parsing rules for JavaScript variable declarations
def p_var_declaration(p):
    '''var_declaration : VAR ID SEMICOLON
                       | LET ID SEMICOLON
                       | CONST ID SEMICOLON
                       | VAR ID ASSIGN NUMBER SEMICOLON
                       | LET ID ASSIGN NUMBER SEMICOLON
                       | CONST ID ASSIGN NUMBER SEMICOLON
                       | VAR ID ASSIGN STRING SEMICOLON
                       | LET ID ASSIGN STRING SEMICOLON
                       | CONST ID ASSIGN STRING SEMICOLON
                       | VAR ID ASSIGN BOOLEAN SEMICOLON
                       | LET ID ASSIGN BOOLEAN SEMICOLON
                       | CONST ID ASSIGN BOOLEAN SEMICOLON'''
    
    if len(p) == 6:  # TYPE ID = VALUE SEMICOLON
        print(f"Parsed variable declaration: {p[1]} {p[2]} = {p[4]}")
    else:  # TYPE ID SEMICOLON
        print(f"Parsed variable declaration: {p[1]} {p[2]}")

# Error rule for syntax errors
def p_error(p):
    if p is None:
        print("Syntax error at EOF")
    else:
        print(f"Syntax error at '{p.value}' (Line {p.lineno})")

# Build the parser
parser = yacc.yacc()

# ============= MAIN LOOP ====================
while True:
    try:
        s = input('Enter JavaScript variable declaration: ')
    except EOFError:
        break
    if not s: continue
    print(f"Input: '{s}'")
    lexer.input(s)  # Feed input to lexer
    for token in lexer:
        print(f"Token: {token.type}, Value: {token.value}")
    parser.parse(s)  # Parse the input
