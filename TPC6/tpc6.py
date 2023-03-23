import ply.lex as lex
import sys


tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'TYPE',
   'VAR',
   'FUNCTION',
   'FUNCTIONNAME'
   'PROGRAM',
   'PROGRAMNAME',
   'ATRIB',
   'LCHAV',
   'RCHAV',
   'LRET',
   'RRET',
   'PONTVIRG',
   'VIRG',
   'MAIOR',
   'MENOR',
   'FOR',
   'WHILE',
   'IF',
   'DOISP',
   'IN',
   'COMMENT',
   'COMMENTB'
)

# Regular expression rules for simple tokens
t_PLUS      = r'\+'
t_MINUS     = r'\-'
t_TIMES     = r'\*'
t_DIVIDE    = r'\/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_ATRIB     = r'\='
t_LCHAV     = r'\{'
t_RCHAV     = r'\}'
t_LRET      = r'\['
t_RRET      = r'\]'
t_PONTVIRG  = r'\;'
t_VIRG      = r'\,'
t_MAIOR     = r'\>'
t_MENOR     = r'\<'
t_DOISP     = r'\.\.'
t_VAR       = r'[a-z_]\w*'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_TYPE(t):
    r'(int|float|double|long|short|void|char|string|bool)'
    return t

def t_PROGRAMNAME(t):
    r'(?<=program\s)\w+(?=\{)'
    return t

def t_FUNCTIONNAME(t):
    r'(?<=function\s)*\w+(?=\()'
    return t

def t_PROGRAM(t):
    r'program'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_FOR(t):
    r'for'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_IF(t):
    r'if'
    return t

def t_IN(t):
    r'in'
    return t

def t_COMMENT(t):
    r'\/\/.*'
    #return t
    pass

def t_COMMENTB(t):
    r'\/\*\s*(.|\n)*\*\/'
    #return t
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# Build the lexer
lexer = lex.lex()

for data in sys.stdin:
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)