import sys
import re
import ply.lex as lex

def printSaldo(saldo):
    euro = int(saldo // 1)
    centimo = str(saldo % 1)
    centimo = centimo[2:4]

    return str(euro) + 'e' + centimo + 'c'


tokens = (
   'LEVANTAR',
   'POUSAR',
   'MOEDA',
   'NUMERO',
   'ABORTAR'
)


states = (
    ('on' , 'exclusive'),
    ('off', 'exclusive')
)


def t_off_LEVANTAR(t):
    r'LEVANTAR'
    lexer.begin('on')
    print('maq: Introduza moedas.')
    return t


def t_on_LEVANTAR(t):
    r'LEVANTAR'
    pass


def t_off_POUSAR(t):
    r'POUSAR'
    pass


def t_on_POUSAR(t):
    r'POUSAR'
    troco = lexer.saldo
    t.saldo = 0
    print('troco=' + printSaldo(troco) +'; Volte sempre!')
    return t


def t_off_MOEDA(t):
    r'MOEDAS'
    pass


def t_on_MOEDA(t):
    r'MOEDA (\s?\d+[c|e],?)+.'
    moedas = t.value.split('A ')[1]
    moedas = re.split(r'[,.] ?', moedas)
    for moeda in moedas[:-1]:
        valor = int(moeda[:-1])
        tipo = moeda[-1]
        if tipo == 'c' and valor not in [1,2,5,10,20,50]:
            print(str(valor) + tipo +' - moeda inválida;', end=' ')
            continue
        elif tipo == 'e' and valor not in [1,2]:
            print(str(valor) + tipo + ' - moeda inválida;', end=' ')
            continue
        else:
            if tipo == 'c':
                lexer.saldo += valor/100
            else:
                lexer.saldo += valor
    print("saldo = " + printSaldo(lexer.saldo))
    return t



def t_off_NUMERO(t):
    r'T\s*=\s*([\d{9}|00\d{9}]{9,11})'
    pass


def t_on_NUMERO(t):
    r'T\s*=\s*([\d{9}|00\d{9}]{9,11})'
    numero = t.value
    numero = re.search(r'\d+', numero).group(0)
    print(numero)

    if (re.match(r'(601|641)\d+', numero)):
        print('Esse número não é permitido neste telefone. Queira discar novo número!')

    elif (re.match(r'00\d+', numero)):
        if lexer.saldo >= 1.5:
            lexer.saldo -= 1.5
        else:
            print('Saldo insufuciente para realizar esta chamada')
    
    elif (re.match(r'2\d+', numero)):
        if lexer.saldo >= 0.25:
            lexer.saldo -= 0.25
        else:
            print('Saldo insufuciente para realizar esta chamada')

    elif (re.match(r'800\d+', numero)):
            pass
    
    elif (re.match(r'808\d+', numero)):
        if lexer.saldo >= 0.10:
            lexer.saldo -= 0.10
        else:
            print('Saldo insufuciente para realizar esta chamada')

    else:
        if lexer.saldo >= 0.5:
            lexer.saldo -= 0.5
        else:
            print('Saldo insufuciente para realizar esta chamada')

    print('saldo = ' + printSaldo(lexer.saldo))

    return t


def t_off_ABORTAR(t):
    r'ABORTAR'
    pass


def t_on_ABORTAR(t):
    r'ABORTAR'
    lexer.begin('off')
    print('troco=' + printSaldo(lexer.saldo))
    return t



def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ANY_ignore  = ' \t'


def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
lexer.saldo = 0
lexer.begin('off')

file = open('maquina')

for data in file:
    lexer.input(data)
    for tok in lexer:
        print(tok)