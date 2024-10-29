import ply.lex as lex
import ply.yacc as yacc

# ============= LEXER ====================

# List of token names
tokens = [
    'WHILE', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'ID', 'COMPARISON', 'NUMBER', 'SEMICOLON', 'ASSIGN',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'
]

# Token definitions
def t_WHILE(t):
    r'while'
    return t

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_PLUS = r'\+'  # Define the PLUS token
t_MINUS = r'-'   # Define the MINUS token
t_MULTIPLY = r'\*'  # Define the MULTIPLY token
t_DIVIDE = r'/'  # Define the DIVIDE token

# Regular expression for identifiers (variable names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Token for comparison operators
def t_COMPARISON(t):
    r'==|!=|<=|>=|<|>'
    return t

# Token for number literals
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
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

# Parsing rules for while loop
def p_while_loop(p):
    '''while_loop : WHILE LPAREN comparison RPAREN LBRACE statements RBRACE'''
    print(f"Parsed while loop: while ({p[3]}) {{ {p[6]} }}")

def p_comparison(p):
    '''comparison : ID COMPARISON NUMBER
                  | ID COMPARISON ID'''
    p[0] = f"{p[1]} {p[2]} {p[3]}"

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:  # More than one statement
        p[0] = p[1] + ' ' + p[2]
    else:  # Single statement
        p[0] = p[1]

def p_statement(p):
    '''statement : ID ASSIGN expression SEMICOLON
                 | ID SEMICOLON'''
    if len(p) == 5:  # ID = expression;
        p[0] = f"{p[1]} = {p[3]}"
    else:  # ID;
        p[0] = f"{p[1]}"

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''
    if len(p) == 4:  # expression operator term
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    else:  # Just a term
        p[0] = p[1]

def p_term(p):
    '''term : term MULTIPLY factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 4:  # term operator factor
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    else:  # Just a factor
        p[0] = p[1]

def p_factor(p):
    '''factor : ID
              | NUMBER'''
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
        s = input('Enter JavaScript while loop: ')
    except EOFError:
        break
    if not s: continue
    print(f"Input: '{s}'")
    lexer.input(s)  # Feed input to lexer
    for token in lexer:
        print(f"Token: {token.type}, Value: {token.value}")
    parser.parse(s)  # Parse the input
