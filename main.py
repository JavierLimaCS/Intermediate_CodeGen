import re
import Temporales
tokens = (
    'MAS',
    'MINUS',
    'POR',
    'DIV',
    'PAR1',
    'PAR2',
    'NUMBER',
    'ID'
)

t_ignore = ' \t'

t_MAS = r'\+'
t_MINUS = r'-'
t_POR = r'\*'
t_DIV = r'/'
t_PAR1 = r'\('
t_PAR2 = r'\)'


def t_NUMBER(t):
    r'[0-9]+'
    t.value = str(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z]+'
    t.value = str(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


import ply.lex as lex

lexer = lex.lex(reflags=re.IGNORECASE)
lexer.lineno = 1
lexer.input("")

precedence = (
    ( 'left', 'MAS', 'MINUS' ),
    ( 'left', 'POR', 'DIV' ),
    ( 'nonassoc', 'UMINUS' )
)


def p_s(p):
    's  : e'
    p[0] = p[1]


def p_e1(p):
    'e   : e MAS t'
    tmp = Temporales.nuevo_temporal()
    code3D = '%s = ' % tmp
    code3D += p[1] + ' + ' + p[3]
    print(code3D)
    p[0] = tmp



def p_e2(p):
    'e   : e MINUS t'
    tmp = Temporales.nuevo_temporal()
    code3D = '%s = ' % tmp
    code3D += p[1] + ' - ' + p[3]
    print(code3D)
    p[0] = tmp


def p_e3(p):
    'e   :  t'
    p[0] = p[1]


def p_expr2uminus(p):
    'f   : MINUS e %prec UMINUS'
    p[0] = - p[2]


def p_t1(p):
    '''t     : t POR f'''
    tmp = Temporales.nuevo_temporal()
    code3D = '%s = ' % tmp
    code3D += p[1] + ' * ' + p[3]
    print(code3D)
    p[0] = tmp


def p_t2(p):
    '''t     : t DIV f'''
    tmp = Temporales.nuevo_temporal()
    code3D = '%s = ' % tmp
    code3D += p[1] + ' / ' + p[3]
    print(code3D)
    p[0] = tmp


def p_t3(p):
    '''t     : f'''
    p[0] = p[1]


def p_expr2NUM(p):
    'f : NUMBER'
    p[0] = p[1]


def p_expr2ID(p):
    'f : ID'
    p[0] = p[1]


def p_parens(p):
    'f : PAR1 e PAR2'
    p[0] = p[2]


def p_error(p):
    print("Error en la sintaxis!")


import ply.yacc as yacc


def ejecutarParse():
    global code3D
    code3D = '\n'
    global tmp
    tmp = ''
    parser = yacc.yacc()
    res = parser.parse("((7 + 9)/(((3 + 1) * (6 + 7) + 8) * 7) / 9) + 100") # aqui se escribe la cadena

ejecutarParse()