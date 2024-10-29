import ply.lex as lex
import ply.yacc as yacc

# ============= LEXER ====================

# List of token names
tokens = [
    'VAR', 'LET', 'CONST',  # JavaScript variable types
    'ID', 'ASSIGN', 'NUMBER', 'STRING', 'SEMICOLON',
    'LBRACKET', 'RBRACKET',  # Brackets for arrays
    'COMMA',                 # Comma for array elements
    'TRUE', 'FALSE', 'NULL'  # Boolean and null values
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
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','

# Token for number literals
def t_NUMBER(t):
    r'\d+(\.\d+)?'  # Allow for integers and floating point numbers
    if '.' in t.value:
        t.value = float(t.value)  # Convert to float if it has a decimal
    else:
        t.value = int(t.value)  # Convert to int if it's an integer
    return t

# Token for string literals (single or double quotes)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'.*?\''
    t.value = t.value[1:-1]  # Remove the quotes around the string
    return t

# Tokens for boolean values and null
def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t

def t_NULL(t):
    r'null'
    t.value = None
    return t

# Regular expression for identifiers (variable names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
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

# Parsing rules for JavaScript array declarations
def p_var_declaration(p):
    '''var_declaration : VAR ID ASSIGN array SEMICOLON
                       | LET ID ASSIGN array SEMICOLON
                       | CONST ID ASSIGN array SEMICOLON'''
    
    print(f"Parsed array declaration: {p[1]} {p[2]} = {p[4]}")

def p_array(p):
    '''array : LBRACKET array_elements RBRACKET
             | LBRACKET RBRACKET'''
    
    if len(p) == 4:  # Format: [elements]
        p[0] = p[2]
    else:  # Empty array: []
        p[0] = []

def p_array_elements(p):
    '''array_elements : array_elements COMMA element
                      | element'''
    
    if len(p) == 4:  # Multiple elements in array
        p[0] = p[1] + [p[3]]
    else:  # Single element in array
        p[0] = [p[1]]

# Rule for an array element which can be a number, string, boolean, null, or another array
def p_element(p):
    '''element : NUMBER
               | STRING
               | TRUE
               | FALSE
               | NULL
               | array'''  # Allow nested arrays
    p[0] = p[1]  # Assign the parsed value to p[0]

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
        s = input('Enter JavaScript array declaration: ')
    except EOFError:
        break
    if not s: continue
    print(f"Input: '{s}'")
    lexer.input(s)  # Feed input to lexer
    for token in lexer:
        print(f"Token: {token.type}, Value: {token.value}")
    parser.parse(s)  # Parse the input
