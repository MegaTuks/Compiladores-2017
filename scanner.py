# Andres Marcelo Garza Cantu A00814236
# Ruben Alejandro Hernandez Gonzalez A01175209

# List of token names.   This is always required
tokens = [
    'SEMICOLON', 'PUNTO',
    'COMMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO', 'OPERADOR_AND_OR', 'EXP_OPERADOR', 'TERM_OPERADOR', 'IDENTIFICADOR',
    'CONST_NUMERO_ENT',
    'CONST_NUMERO_REAL', 'IDENTIFICADOR_CLASE', 'CONST_CARACTERES', 'CONST_BOOLEANO', 'INTER_IZQ', 'INTER_DER',
]

reserved = {
    'entero': 'KEYWORD_TYPE_ENTERO',
    'real': 'KEYWORD_TYPE_REAL',
    'booleano': 'KEYWORD_TYPE_BOOLEANO',
    'si': 'KEYWORD_SI',
    'sino': 'KEYWORD_SINO',
    'mientras': 'KEYWORD_MIENTRAS',
    'caso':'KEYWORD_CASO',
    'escenario':'KEYWORD_ESCENARIO'
    'principal': 'KEYWORD_PRINCIPAL',
    'caracter': 'KEYWORD_TYPE_CARACTERES',
    'entrada': 'KEYWORD_ENTRADA',
    'salida': 'KEYWORD_SALIDA',
    'funcion': 'KEYWORD_FUNCION',
    'nulo': 'KEYWORD_NULO',
    'retorno': 'KEYWORD_RETORNO',
    'verdadero': 'KEYWORD_VERDADERO',
    'falso': 'KEYWORD_FALSO'
}
tokens += reserved.values()
# Tokens
# Tokens
t_SEMICOLON = r'\;'
t_PUNTO = r'[\.]'
t_COMMA = r'[\,]'
t_COLON = r'\:'
t_BRACKET_IZQ = r'\{'
t_BRACKET_DER = r'\}'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_OPERADOR_IGUAL = r'\='
t_OPERADOR_COMPARATIVO = r'[>]|[<]'
t_OPERADOR_AND_OR = r'&&|\|\|'
t_EXP_OPERADOR = r'\+|\-'
t_TERM_OPERADOR = r'\*|\/'
t_ignore = '\t\n\r'

def t_CONST_NUMERO_REAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_CONST_NUMERO_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFICADOR(t):
    r'[a-z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_IDENTIFICADOR_CLASE(t):
    r'[A-Z][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_CONST_BOOLEANO(t):
    r'[KEYWORD_VERDADERO|KEYWORD_FALSO]'
    return t


t_CONST_CARACTERES = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!\ ]*\"'

def t_error(t):
    print("Caracter  Ilegal>>> '%s'  <<<<" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex

lexer = lex.lex()

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Error de sintaxis en '%s'" % t.value)

#diagrama de sintaxis Inicial del pograma , Funcion principal 
def p_Programa(t):
    '''
      Programa : ProgramaA FuncionPrincipal
    '''


#diagrama de sintaxis de como funciona el programa , puedes ahcer declaraciones, Funciones o clases antes de entrar al main
def p_ProgramaA(t):
    '''
      ProgramaA : Declaracion ProgramaA
      | Funcion ProgramaA
      | empty
    '''

#funcion que corre el programa principal , necesaria para correr nuestro lenguaje
def p_FuncionPrincipal(t):
    '''
    FuncionPrincipal : KEYWORD_PRINCIPAL PARENTESIS_IZQ PARENTESIS_DER Bloque
    '''

def p_Funcion(t):
    '''
    Funcion : KEYWORD_FUNCION Tipo IDENTIFICADOR PARENTESIS_IZQ FuncionA PARENTESIS_DER Bloque
    '''

def p_FuncionA(t):
    '''
    FuncionA : Tipo IDENTIFICADOR FuncionB
    | empty
    '''

def p_FuncionB(t):
    '''
    FuncionB : COMMA FuncionA
    | empty
    '''

import ply.yacc as yacc

#parser = yacc.yacc(start='Programa')

#fileload = input('Nombre del archivo de entrada: ')

#with open(fileload) as fileval:
#  result = parser.parse(fileval.read())
#  lexer.input(fileval.read())

#print(result)