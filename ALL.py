import ply.lex as lex
import ply.yacc as yacc

# --- Lexer (token definitions) ---

# Reserved words (keywords)
reserved = {
    'var': 'VAR',
    'let': 'LET',
    'const': 'CONST',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
}

# Token list
tokens = [
    'ID', 'NUMBER', 'STRING', 'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA', 'COLON', 'SEMICOLON', 'COMPARISON',
] + list(reserved.values())

# Regular expression rules for tokens
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'

# Match keywords
def t_VAR(t):
    r'var'
    return t

def t_LET(t):
    r'let'
    return t

def t_CONST(t):
    r'const'
    return t

def t_WHILE(t):
    r'while'
    return t

# Identifiers (variable names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for keywords
    return t

# Numbers (integers and floating-point)
def t_NUMBER(t):
    r'\d+\.\d*|\d+(\.\d*)?'  # Updated regex to handle decimal numbers
    t.value = float(t.value)  # Convert number to float
    return t

# Strings
def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    return t

# Comparison operators
def t_COMPARISON(t):
    r'==|!=|<=|>=|<|>'
    return t

# Skip whitespace
t_ignore = ' \t'

# Newline handling
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# --- Parser (grammar rules) ---

# Grammar rules

# Assignment statement
def p_statement_var(t):
    'statement : VAR ID ASSIGN expr SEMICOLON'
    print(f'Var declaration with assignment: {t[2]} = {t[4]}')

def p_statement_var_decl(t):
    'statement : VAR ID SEMICOLON'
    print(f'Var declaration without assignment: {t[2]}')

def p_statement_let(t):
    'statement : LET ID ASSIGN expr SEMICOLON'
    print(f'Let declaration: {t[2]} = {t[4]}')

def p_statement_const(t):
    'statement : CONST ID ASSIGN expr SEMICOLON'
    print(f'Const declaration: {t[2]} = {t[4]}')

def p_statement_assign(t):
    'statement : ID ASSIGN expr SEMICOLON'
    print(f'{t[1]} = {t[3]}')

def p_statement_expr(t):
    'statement : expr SEMICOLON'
    print(f'Expression: {t[1]}')

# Expression parsing (binary operations, values, and arrays)
def p_expr_binop(t):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr COMPARISON expr'''
    t[0] = f"({t[1]} {t[2]} {t[3]})"

def p_expr_number(t):
    'expr : NUMBER'
    t[0] = t[1]

def p_expr_string(t):
    'expr : STRING'
    t[0] = t[1]

def p_expr_id(t):
    'expr : ID'
    t[0] = t[1]

def p_expr_parens(t):
    'expr : LPAREN expr RPAREN'
    t[0] = t[2]

# Array literal (corrected expression rule)
def p_expr_array(t):
    'expr : LBRACKET elements RBRACKET'
    t[0] = f"[{t[2]}]"

# Elements inside an array (comma-separated list of expressions)
def p_elements_single(t):
    'elements : expr'
    t[0] = f"{t[1]}"

def p_elements_multiple(t):
    'elements : expr COMMA elements'
    t[0] = f"{t[1]}, {t[3]}"

# Object literal (for handling objects inside arrays)
def p_expr_object(t):
    'expr : LBRACE object_members RBRACE'
    t[0] = f"{{{t[2]}}}"

# Object members inside an object
def p_object_members(t):
    'object_members : ID COLON expr'
    t[0] = f"{t[1]}: {t[3]}"

def p_object_members_multiple(t):
    'object_members : ID COLON expr COMMA object_members'
    t[0] = f"{t[1]}: {t[3]}, {t[5]}"

# WHILE loop parsing (updated to handle body statements correctly)
def p_statement_while(t):
    'statement : WHILE LPAREN expr RPAREN LBRACE statements RBRACE'
    print(f"While loop: while ({t[3]}) {{ {t[6]} }}")

# Handle multiple statements inside braces
def p_statements_single(t):
    'statements : statement'
    t[0] = t[1]

def p_statements_multiple(t):
    'statements : statement statements'
    t[0] = f"{t[1]}; {t[2]}"

# Handle empty block (empty statement list)
def p_statements_empty(t):
    'statements : '
    t[0] = ''

# Error rule for syntax errors
def p_error(t):
    if t:
        print(f"Syntax error at '{t.value}'")
    else:
        print("Syntax error at EOF")

# --- Main ---

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Read input and process it
def parse_js_code(code):
    lexer.input(code)
    for token in lexer:
        print(f'Token: {token.type}, Value: {token.value}')
    
    print("Parsing code...")
    parser.parse(code)

# Input loop
while True:
    try:
        code = input("Enter JavaScript code: ")
        if code.lower() == "exit":
            break
        parse_js_code(code)
    except EOFError:
        break
