# Andres Marcelo Garza Cantu A00814236
# Ruben Alejandro Hernandez Gonzalez A01175209

# List of token names.   This is always required
tokens = [
    'SEMICOLON', 'PUNTO', 'COMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 
    'CORCHETE_IZQ', 'CORCHETE_DER', 'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO', 'OPERADOR_AND_OR', 'EXP_OPERADOR', 
    'TERM_OPERADOR', 'IDENTIFICADOR', 'CONST_NUMERO_ENT', 'CONST_NUMERO_REAL', 'CONST_CARACTERES', 'CONST_BOOLEANO', 
    'KEYWORD_CAMBIO', 'KEYWORD_CASO', 'KEYWORD_ROMPE', 'KEYWORD_BASE'
]

reserved = {
    'entero': 'KEYWORD_TYPE_ENTERO',
    'real': 'KEYWORD_TYPE_REAL',
    'booleano': 'KEYWORD_TYPE_BOOLEANO',
    'si': 'KEYWORD_SI',
    'sino': 'KEYWORD_SINO',
    'mientras': 'KEYWORD_MIENTRAS',
    'caso':'KEYWORD_CASO',
    'escenario':'KEYWORD_ESCENARIO',
    'principal': 'KEYWORD_PRINCIPAL',
    'caracter': 'KEYWORD_TYPE_CARACTERES',
    'entrada': 'KEYWORD_ENTRADA',
    'salida': 'KEYWORD_SALIDA',
    'funcion': 'KEYWORD_FUNCION',
    'nulo': 'KEYWORD_NULO',
    'retorno': 'KEYWORD_RETORNO',
    'verdadero': 'KEYWORD_VERDADERO',
    'falso': 'KEYWORD_FALSO',
    'cambio': 'KEYWORD_CAMBIO',
    'caso': 'KEYWORD_CASO',
    'rompe': 'KEYWORD_ROMPE',
    'base': 'KEYWORD_BASE'
}
tokens += reserved.values()
# Tokens
# Tokens
t_SEMICOLON = r'\;'
t_PUNTO = r'[\.]'
t_COMA = r'[\,]'
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
    FuncionB : COMA FuncionA
    | empty
    '''

def p_Bloque(t):
    '''
    Bloque : BRACKET_IZQ BloqueA BRACKET_DER
    '''

def p_BloqueA(t):
    '''
    BloqueA : Declaracion BloqueA
    | Asignacion BloqueA
    | LlamadaId BloqueA
    | Ciclo BloqueA
    | Condicion BloqueA
    | Entrada BloqueA
    | Salida BloqueA
    | Cambio BloqueA
    | KEYWORD_RETORNO ValorSalida
    | empty
    '''

def p_Declaracion(t):
    '''
    Declaracion : Tipo IDENTIFICADOR DeclaracionA SEMICOLON
    '''

def p_DeclaracionA(t):
    '''
    DeclaracionA : CORCHETE_IZQ CONST_NUMERO_ENT CORCHETE_DER DeclaracionB
    | empty
    '''
def p_DeclaracionB(t):
    '''
    DeclaracionB : CORCHETE_IZQ CONST_NUMERO_ENT CORCHETE_DER
    | empty
    '''

def p_Asignacion(t):
    '''
    Asignacion : IDENTIFICADOR AsignacionA OPERADOR_IGUAL Expresion SEMICOLON
    '''

def p_AsignacionA(t):
    '''
    AsignacionA : CORCHETE_IZQ Expresion CORCHETE_DER AsignacionB
    | empty
    '''

def p_AsignacionB(t):
    '''
    AsignacionB : CORCHETE_IZQ Expresion CORCHETE_DER
    | empty
    '''

def p_LlamadaFuncion(t):
    '''
    LlamadaFuncion : IDENTIFICADOR PARENTESIS_IZQ LlamadaFuncionA PARENTESIS_DER
    '''

def p_LlamadaFuncionA(t):
    '''
    LlamadaFuncionA : Expresion LlamadaFuncionB
    | empty
    '''

def p_LlamadaFuncionB(t):
    '''
    LlamadaFuncionB : COMA LlamadaFuncionA
    | empty
    '''

def p_Ciclo(t):
    '''
    Ciclo : KEYWORD_MIENTRAS PARENTESIS_IZQ Expresion PARENTESIS_DER Bloque
    '''

def p_LlamadaId(t):
	'''
	LlamadaId : LlamadaFuncion
	| Terminal
	'''

def p_Terminal(t):
	'''
	Terminal : IDENTIFICADOR TerminalA
	'''

def p_TerminalA(t):
	'''
	TerminalA : CORCHETE_IZQ Expresion CORCHETE_DER TerminalB
	| empty
	'''
def p_TerminalB(t):
	'''
	TerminalB : CORCHETE_IZQ Expresion CORCHETE_DER TerminalB
	| empty
	'''
def p_Tipo(t):
	'''
	Tipo : KEYWORD_TYPE_BOOLEANO
	| KEYWORD_TYPE_ENTERO
	| KEYWORD_TYPE_REAL
	| KEYWORD_TYPE_CARACTERES
	'''

def p_Condicion(t):
    '''
    Condicion : KEYWORD_SI PARENTESIS_IZQ Expresion PARENTESIS_DER CondicionA
    '''

def p_CondicionA(t):
    '''
    CondicionA : Bloque
    | KEYWORD_SINO Bloque
    '''

def p_Entrada(t):
    '''
    Entrada : KEYWORD_ENTRADA IDENTIFICADOR SEMICOLON
    '''

def p_EntradaA(t):
    '''
    EntradaA : CORCHETE_IZQ Expresion CORCHETE_DER EntradaB
    | empty
    '''

def p_EntradaB(t):
    '''
    EntradaB : CORCHETE_IZQ Expresion CORCHETE_DER
    | empty
    '''

def p_Salida(t):
    '''
    Salida : KEYWORD_SALIDA Expresion SEMICOLON
    '''

def p_Cambio(t):
    '''
    Cambio : KEYWORD_CAMBIO PARENTESIS_IZQ Expresion PARENTESIS_DER BRACKET_IZQ CambioA
    '''

def p_CambioA(t):
    '''
    CambioA : KEYWORD_CASO ValorSalida COLON Bloque KEYWORD_ROMPE SEMICOLON CambioA
    | empty
    '''

def p_CambioB(t):
    '''
    CambioB : KEYWORD_BASE COLON Bloque BRACKET_DER
    '''

def p_ValorSalida(t):
    '''
    ValorSalida : CONST_NUMERO_ENT
    | CONST_NUMERO_REAL
    | CONST_CARACTERES
    | CONST_BOOLEANO
    | KEYWORD_NULO
    | LlamadaId
    '''


#cuadro principal de expresion
def p_Expresion(t):
    '''
      Expresion : Expresion ExpresionA
      | Expres
    '''

#Llama auxiliar y la siguiente parte de la expresion
def p_ExpressionA(t):
    '''
    ExpresionA : ExpresionAux Expres
    '''

#recibe los operadores And y Or
def p_ExpresionAux(t):
    '''
    ExpresionAux : OPERADOR_AND_OR
    '''

#siguiente parte de expresion, corre otras jerarquias de expresion
def p_Expres(t):
    '''
    Expres : Expres ExpresA
    | Exp
    '''

#llama la auxiliar de expresion y un nivel mas abajo de expresion
def p_ExpresA(t):
    '''
    ExpresA : ExpresAux Exp
    '''

#carga los operadores comparativos
def p_ExpresAux(t):
    '''
    ExpresAux : OPERADOR_COMPARATIVO
    '''


#carga siguientes niveles de expresion
def p_Exp(t):
    '''
    Exp : Exp ExpA
    | Termino
    '''
#carga el siguiente nivel de expresion
def p_ExpA(t):
    '''
    ExpA : ExpAux Termino
    '''

#carga los operadores de suma y resta
def p_ExpAux(t):
    '''
    ExpAux : EXP_OPERADOR
    '''

#carga la siguientes partes de expresion
def p_Termino(t):
    '''
    Termino : Termino TerminoA
    | Factor
    '''
#siguiente nivel de expresion compara
# el * e / y general el cuadruplo correcto
def p_TerminoA(t):
    '''
    TerminoA : TerminoAux Factor
    '''
 
#inserta los terminos * y / en el stack de operadores
def p_TerminoAux(t):
    '''
    TerminoAux : TERM_OPERADOR
    '''

#Factor es el valor "atmopico de una operacion, el caul es el resultaod de algo entre parentesis"
# o de los elementos atomicos
def p_Factor(t):
    '''
      Factor : ValorSalida
      | PARENTESIS_IZQ Expresion PARENTESIS_DER
    '''
    ## parentesis para fondos falsos. 






import ply.yacc as yacc

parser = yacc.yacc(start='Programa')

fileload = input('Nombre del archivo de entrada: ')

with open(fileload) as fileval:
  result = parser.parse(fileval.read())
  lexer.input(fileval.read())

print(result)