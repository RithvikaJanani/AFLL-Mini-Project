import ply.lex as lex
import ply.yacc as yacc

# ============= LEXER ====================

# List of token names
tokens = [
    'VAR', 'LET', 'CONST',  # JavaScript variable types
    'ID', 'ASSIGN', 'NUMBER', 'STRING', 'SEMICOLON',
    'LBRACE', 'RBRACE',  # Braces for objects
    'COLON', 'COMMA'     # Colon for key-value pairs and comma for elements
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
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'
t_COMMA = r','

# Regular expression for identifiers (variable names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Token for number literals
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Token for string literals (single or double quotes)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'.*?\''
    t.value = t.value[1:-1]  # Remove the quotes around the string
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

# Parsing rules for JavaScript object declarations
def p_var_declaration(p):
    '''var_declaration : VAR ID ASSIGN object SEMICOLON
                       | LET ID ASSIGN object SEMICOLON
                       | CONST ID ASSIGN object SEMICOLON'''
    
    print(f"Parsed object declaration: {p[1]} {p[2]} = {p[4]}")

def p_object(p):
    '''object : LBRACE object_properties RBRACE
              | LBRACE RBRACE'''
    
    if len(p) == 4:  # Format: { properties }
        p[0] = p[2]
    else:  # Empty object: {}
        p[0] = {}

def p_object_properties(p):
    '''object_properties : object_properties COMMA property
                         | property'''
    
    if len(p) == 4:  # Multiple properties in object
        p[0] = p[1]  # Keep existing properties
        p[0][p[3][0]] = p[3][1]  # Add new property (key-value)
    else:  # Single property in object
        p[0] = {p[1][0]: p[1][1]}  # Create new mapping

def p_property(p):
    '''property : ID COLON value'''
    p[0] = (p[1], p[3])  # Tuple of (key, value)

def p_value(p):
    '''value : NUMBER
             | STRING'''
    p[0] = p[1]

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
        s = input('Enter JavaScript object declaration: ')
    except EOFError:
        break
    if not s: continue
    print(f"Input: '{s}'")
    lexer.input(s)  # Feed input to lexer
    for token in lexer:
        print(f"Token: {token.type}, Value: {token.value}")
    parser.parse(s)  # Parse the input
