# Andres Marcelo Garza Cantu A00814236
# Ruben Alejandro Hernandez Gonzalez A01175209
# COMPILADORES 2017
# COMPILADOR DE INPUT GRAFICO
from tablas import *
import sys

#tokens relacionados con el programa
tokens = [
    'SEMICOLON', 'PUNTO', 'COMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 
    'CORCHETE_IZQ', 'CORCHETE_DER', 'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO', 'OPERADOR_AND_OR', 'EXP_OPERADOR', 
    'TERM_OPERADOR', 'IDENTIFICADOR', 'CONST_NUMERO_ENT', 'CONST_NUMERO_REAL', 'CONST_CARACTERES', 'CONST_BOOLEANO',    
]
# Palabras Reservadas del compilador
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

# Tokens Utilizados
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
t_OPERADOR_COMPARATIVO = r'[>]|[<]|[~]'
t_OPERADOR_AND_OR = r'&&|\|\|'
t_EXP_OPERADOR = r'\+|\-'
t_TERM_OPERADOR = r'\*|\/'
t_ignore = ' \t\n\r'

# VARIABLES DE COMPILACION
#TABLAS DE SIMBOLOS
tablaGlobal = TablaSimbolos()
tablaSimbolosActual = tablaGlobal
tablaConstantes = TablaConstantes()
tablaTemporales = TablaTemporales()
stackOperador = []  # se usa para guardar los operadores del momento
stackOperando = []  # se usa para guardar las ,variables, constantes, temporales;
stackSaltos = [] # stack saltos para guardar los saltos de GOTOF
temporales = [] #tabla de valores temporales. 
stackCambio = [] #contiene los casos de caso(ultimo indice a modificar). 
##variables para funciones
listaParametros = [] #lista de parametros para procedimientos. 
listaprocedimientos = Procedimientos()
stackParam = [] #parametro que guardara en una pila , la LISTA de parametros
procedureName = []#registrar el nombre de la funcion temporalmente.
nuevaFuncion = "" #nombredel procedimeinto para ajustar.
inicioCuad = 0
temporales.append(None)
indicetemporales = 0 #indice de las variables temporales.
checkSemantica = claseCuboSemantico()
cuadruplo = Cuadruplos()

#FIN DE VARIABELS DE COMPILACION

#VARIABLES DE MEMORIA
memoriaGlobal = MemoriaReal()
memoriaConstante =  MemoriaReal(20000)
monolito = Monolito()

# Tipo numerico que acepta numeros reales 
def t_CONST_NUMERO_REAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

#tipo numerico que solo acepta numeros enteros
def t_CONST_NUMERO_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t

#Los identificadores deben necesariamente iniciar en minuscula.
def t_IDENTIFICADOR(t):
    r'[a-z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

#keyword falso o verdadero son los unicos variables aceptados para constantes booleanas
def t_CONST_BOOLEANO(t):
    r'[KEYWORD_VERDADERO | KEYWORD_FALSO]'
    return t

#string de caracteres iniciados con " y termina con "
t_CONST_CARACTERES = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!\ ]*\"'

#funcion para imprimir errores lexicos
def t_error(t):
    print("Caracter  Ilegal>>> '%s'  <<<<" % t.value[0])
    t.lexer.skip(1)

def insertaConstante(iden,tipo):
    global tablaConstantes,memoriaConstante
    constante = iden
    existe = tablaConstantes.buscar(constante)
    if (existe is None):

        tablaConstantes.insertar(constante,tipo)
    else:
        print ("previamente insertada")

def getMemId(tipo):
    global memoriaGlobal
    memID = 0
    if (tipo == "real"):
        memID = memoriaGlobal.insertaReales()
    elif (tipo == "booleano"):
        memID = memoriaGlobal.insertaBooleano()
    elif (tipo == "caracter"):
        memID = memoriaGlobal.insertaCaracteres()
    elif (tipo == "entero"):
        memID = memoriaGlobal.insertaEntero()
    return memID

def setTemporal(tipoNum):
    global memoriaGlobal,monolito,tablaTemporales,indicetemporales
    result = 't' + str(indicetemporales)
    indicetemporales = indicetemporales + 1
    memID = 0
    tipo = ""
    if(tipoNum == 0):
        memID = memoriaGlobal.insertaBooleano()
        tipo = "booleano"
    elif(tipoNum == 1):
        memID = memoriaGlobal.insertaEntero()
        tipo = "entero"
    elif (tipoNum == 2):
        memID = memoriaGlobal.insertaReales()
        tipo = "real"
    elif (tipoNum == 3):
        memID = memoriaGlobal.insertaCaracteres()
        tipo = "caracter"
    paraTabla = {'memID' : memID,'tipo':tipo}
    tablaTemporales.insertar(result,tipo)
    valor = setValor(tipo)
    monolito.insertaActual(memID,valor)
    return memID






def setValor(tipo):
    if (tipo == "real"):
        return 0.0
    elif (tipo == "booleano"):
        return "falso"
    elif (tipo == "caracter"):
        return "n/a"
    elif (tipo == "entero"):
        return 0

def makeParam(paramID, stackActual):
    global listaprocedimientos,cuadruplo
    print ("paramID: ", paramID)
    print("stackActual: ",stackActual)
    lista = listaprocedimientos.buscar(paramID)
    print("lista",lista)
    if (lista is None):
        print ("error en la funcion")
        raise SystemExit
    else:
        longitudTotal = len(lista)
        longitudActual = len(stackActual)
        if(longitudTotal == 0):
            paramActual = -1
        else:
            print("longitudActual",longitudActual)
            print("longitudTotal", longitudTotal)
            paramActual = longitudTotal - longitudActual 
            print("paramActual", paramActual)
        return paramActual




import ply.lex as lex

lexer = lex.lex()

#funcion para simular los vacios.
def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Error de sintaxis en '%s'" % t.value)

#diagrama de sintaxis Inicial del pograma , Funcion principal 
def p_Programa(t):
    '''
      Programa : ProgramaInicio ProgramaA FuncionPrincipal
    '''
    global tablaGlobal, tablaSimbolosActual, tablaConstantes,cuadruplo,listaprocedimientos
    cuadruplo.normalCuad('FIN',None,None,None)
    tablaSimbolosActual.imprimir()
    tablaConstantes.imprimir()
    cuadruplo.imprimir()
    listaprocedimientos.imprimir()

#salto inicial del programa. 
def p_ProgramaInicio(t):
    '''
    ProgramaInicio : 
    '''
    global cuadruplo,stackSaltos
    cuadruplo.normalCuad('GOTO',None,None,None)
    salto = cuadruplo.CuadIndex()
    stackSaltos.append(salto)

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
    FuncionPrincipal : PrincipalAux PARENTESIS_IZQ PARENTESIS_DER Bloque FinPrincipal
    '''
def p_FinPrincipal(t):
    '''
    FinPrincipal : 
    '''
    global tablaSimbolosActual, tablaGlobal
    tablaSimbolosActual =  tablaGlobal

def p_PrincipalAux(t):
    '''
    PrincipalAux : KEYWORD_PRINCIPAL
    '''
    global tablaSimbolosActual,cuadruplo,stackSaltos,listaprocedimientos
    identificador = t[1]
    tablaF = TablaSimbolos()
    tablaSimbolosActual.insertar(identificador,"funcionPrincipal")
    tablaF.insertar(identificador,"principal")
    tablaSimbolosActual.agregarHijo(tablaF)
    tablaF.agregarPadre(tablaSimbolosActual)
    tablaSimbolosActual = tablaF
    indice = stackSaltos.pop()
    salto =  cuadruplo.CuadIndex() + 1
    cuadruplo.InsertarSalto(indice, salto)


def p_Funcion(t):
    '''
    Funcion : FuncionAux PARENTESIS_IZQ FuncionA PARENTESIS_DER Bloque FinFuncion
    '''


def p_FinFuncion(t):
    '''
    FinFuncion : 
    '''
    global tablaGlobal, tablaSimbolosActual,nuevaFuncion,listaprocedimientos,listaParametros,cuadruplo,inicioCuad
    cuadruplo.normalCuad('RETU',None,None,None)
    destino = cuadruplo.CuadIndex()
    tablaSimbolosActual = tablaGlobal
    listaprocedimientos.meteParametros(nuevaFuncion, listaParametros)
    listaprocedimientos.normalLista(nuevaFuncion,inicioCuad,destino)
    nuevaFuncion = ""
    inicioCuad = 0
    listaParametros = []

def p_FuncionAux(t):
    '''
    FuncionAux : KEYWORD_FUNCION Tipo IDENTIFICADOR
    '''
    global tablaSimbolosActual, tablaGlobal, nuevaFuncion,cuadruplo,inicioCuad,memoriaGlobal, monolito
    funcion  = t[1]
    tipo =  t[2]
    identificador =  t[3]
    tablaF = TablaSimbolos()
    existe = tablaGlobal.buscar(t[3])
    if(existe is None):
        nuevaFuncion = identificador
        inicioCuad =  cuadruplo.CuadIndex() + 1
        memID = getMemId(tipo)
        valor = {'funcion':'funcion','tipo': tipo,'inicio':inicioCuad, 'memID': memID }
        valorDefault = setValor(tipo)
        monolito.insertaActual(memID,valorDefault)
        tablaSimbolosActual.insertar(identificador, valor)
        tablaF.insertar(identificador,tipo)
        tablaSimbolosActual.agregarHijo(tablaF)
        tablaF.agregarPadre(tablaSimbolosActual)
        tablaSimbolosActual = tablaF
    else:
        print("funcion declarada previamente, o variable global comparte su nombre")
        raise SystemExit



def p_FuncionA(t):
    '''
    FuncionA : Tipo IDENTIFICADOR FuncionB
    | empty
    '''
    global tablaSimbolosActual, tablaGlobal,listaParametros,monolito
    if(len(t) == 4):
        tipo = t[1]
        identificador = t[2]
        existe = tablaSimbolosActual.buscar(identificador)
        if(existe is None):
            memID = getMemId(tipo)
            valorDefault = setValor(tipo)
            parametro = {'id':identificador,'tipo':tipo , 'memID':memID}
            listaParametros.append(parametro)
            tablaSimbolosActual.insertar(identificador, tipo)
            monolito.insertaActual(memID,valorDefault)
        else:
            print("parametro declarado previamente, o variable global comparte su nombre")
            raise SystemExit


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
    | LlamadaFuncion SEMICOLON BloqueA
    | Ciclo BloqueA
    | Condicion BloqueA
    | Entrada BloqueA
    | Salida BloqueA
    | Cambio BloqueA
    | RetornoAux
    | empty
    '''

def p_RetornoAux(t):
    '''
    RetornoAux : KEYWORD_RETORNO Expresion SEMICOLON
    '''
    global cuadruplo, stackOperando
    op = stackOperando.pop()
    retorno =  t[1]
    cuadruplo.normalCuad('ret', None, None, op)

def p_Declaracion(t):
    '''
    Declaracion : Tipo IDENTIFICADOR DeclaracionA SEMICOLON
    '''
    global tablaSimbolosActual, tablaGlobal,monolito
    tipo = t[1]
    identificador = t[2]
    existe = tablaSimbolosActual.buscar(identificador)
    existeArreglos = t[3]
    if(existe is None):
        if (t[3] is  None):
            memID = getMemId(tipo)
            valorDefault = setValor(tipo)
            monolito.insertaActual(memID,valorDefault)
            insert = {'tipo':tipo,'memID':memID}
            tablaSimbolosActual.insertar(identificador, insert)
        else:
            print("existeArreglo: ",existeArreglos)
            #si es matriz AQUI se corren funciones de matriz
            tablaSimbolosActual.insertar(identificador, tipo)
    else:
        print("Variable declarada previamente, o variable global comparte su nombre")
        raise SystemExit
    

def p_DeclaracionA(t):
    '''
    DeclaracionA : ArregloAux DeclaracionB
    | empty
    '''
    if(len(t) == 2):
        print("tiene dimension")
        #t[0] = {'arreglo':t[1],'matriz':t[2] }

def p_ArregloAux(t):
    '''
    ArregloAux : CORCHETE_IZQ CONST_NUMERO_ENT CORCHETE_DER
    '''
    t[0] = {'casillas': t[2]}
    
def p_DeclaracionB(t):
    '''
    DeclaracionB : ArregloAux
    | empty
    '''
    t[0] = t[1]


def p_Asignacion(t):
    '''
    Asignacion : IDENTIFICADOR AsignacionA OPERADOR_IGUAL Expresion SEMICOLON
    '''
    global tablaSimbolosActual,tablaGlobal,cuadruplo,stackOperando
    identificador = t[1]
    existe = tablaSimbolosActual.buscar(identificador)
    existeGlobal = tablaGlobal.buscar(identificador)
    if(existe is  None):
        if(existeGlobal is  None):
            print("VARIABLE no declarada previamente") 
            raise SystemExit
    else:
        op1 = stackOperando.pop()
        cuadruplo.normalCuad('=',op1,None,identificador)

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
    LlamadaFuncion : LlamadaAux PARENTESIS_IZQ LlamadaFuncionA PARENTESIS_DER finLlamada
    '''

def p_LlamadaAux(t):
    '''
    LlamadaAux : IDENTIFICADOR
    '''
    global tablaGlobal, cuadruplo, stackParam, listaprocedimientos, procedureName
    identificador = t[1]
    existe = tablaGlobal.buscar(t[1])
    if(existe is None):
        print("Funcion no declarada")
        raise SystemExit
    else:

        iden = list(listaprocedimientos.buscar(identificador))
        print("iden",iden)
        stackParam.append(iden)
        procedureName.append(identificador)
        print("stack de parametros: ",stackParam)
        cuadruplo.normalCuad('ERA', identificador, None, None)



def p_LlamadaFuncionA(t):
    '''
    LlamadaFuncionA :  ParamAux  LlamadaFuncionB
    | empty
    '''   

def p_ParamAux(t):
    '''
    ParamAux : Expresion
    '''
    global cuadruplo,stackParam,procedureName,stackOperando
    listaPar = stackParam.pop()
    iden = procedureName.pop()
    param = makeParam(iden, listaPar)
    procedureName.append(iden)
    if (param == -1):
        print("Funcion Sin parametros")
    else:

        expresion = stackOperando.pop()
        paramNo = 'param#' + str(param)
        cuadruplo.normalCuad('param', expresion, None, paramNo)
        listaPar.pop()
        print("listaPar", listaPar)
        stackParam.append(listaPar)

def p_LlamadaFuncionB(t):
    '''
    LlamadaFuncionB : COMA LlamadaFuncionA
    | empty
    '''

def p_finLlamada(t):
    '''
    finLlamada : 
    '''
    global cuadruplo, stackOperando,procedureName
    iden =  procedureName.pop()
    cuadruplo.normalCuad('gosub', iden, None, None)


def p_Ciclo(t):
    '''
    Ciclo : KEYWORD_MIENTRAS PARENTESIS_IZQ Expresion PARENTESIS_DER CicloAux Bloque FinCiclo
    '''

def p_CicloAux(t):
    '''
    CicloAux : 
    '''
    global tablaSimbolosActual,tablaGlobal,stackOperando,cuadruplo,stackSaltos
    #print("Cuadruplo Indice: ",cuadruplo.CuadIndex())
    op = stackOperando.pop()
    cuadruplo.normalCuad("GOTOF",op,None,None)
    salto = cuadruplo.CuadIndex()
    stackSaltos.append(salto)
    print("Ciclo")

def p_FinCiclo(t):
    '''
    FinCiclo : 
    '''
    global tablaSimbolosActual,tablaGlobal,stackOperando,cuadruplo,stackSaltos
    #print("Cuadruplo Indice: ",cuadruplo.CuadIndex())
    indice = stackSaltos.pop()
    cuadruplo.normalCuad('GOTO',None,None,indice)
    salto = cuadruplo.CuadIndex() + 1
    cuadruplo.InsertarSalto(indice,salto)



def p_LlamadaId(t):
    '''
    LlamadaId : LlamadaFuncion
    | Terminal
    '''
    #funcion a checar

def p_Terminal(t):
    '''
    Terminal : IDENTIFICADOR TerminalA
    '''
    identificador = t[1]
    global tablaSimbolosActual,tablaGlobal,stackOperando
    existe = tablaSimbolosActual.buscar(identificador)
    existeGlobal = tablaGlobal.buscar(identificador)
    if (existe is None):
        if(existeGlobal is None):
            print("variable no declarada")
            raise SystemExit
        else:
            stackOperando.append(existeGlobal['memID'])
    else:
        stackOperando.append(existe['memID'])

    #funcion a checar

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
    t[0] = t[1]


def p_Condicion(t):
    '''
    Condicion : CondicionSi CondicionA
    '''
    print('entre a condicion')

def p_CondicionSi(t):
    '''
    CondicionSi : KEYWORD_SI PARENTESIS_IZQ Expresion PARENTESIS_DER
    '''
    global cuadruplo, stackOperando,stackSaltos
    #print("Cuadruplo Indice: ",cuadruplo.CuadIndex())
    op = stackOperando.pop()
    cuadruplo.normalCuad("GOTOF",op,None,None)
    salto = cuadruplo.CuadIndex()
    stackSaltos.append(salto)
    print("CondicionSi")

def p_CondicionA(t):
    '''
    CondicionA : Bloque CondicionSino
    |  Bloque
    '''
    print('entraste CondicionA?')
    global cuadruplo,stackOperando,stackSaltos
    indice = stackSaltos.pop()
    salto = cuadruplo.CuadIndex()
    cuadruplo.InsertarSalto(indice,salto)


def p_CondicionSino(t):
    '''
    CondicionSino : SinoAux Bloque FinSino
    '''
    
def p_SinoAux(t):
    '''
    SinoAux : KEYWORD_SINO
    '''
    global cuadruplo, stackOperando,stackSaltos
    #print("Cuadruplo Indice: ",cuadruplo.CuadIndex())
    cuadruplo.normalCuad("GOTO",None,None,None)
    salto = cuadruplo.CuadIndex()
    stackSaltos.append(salto)


def p_FinSino(t):
    '''
    FinSino :
    '''
    global cuadruplo,stackOperando,stackSaltos
    indice = stackSaltos.pop()
    salto = cuadruplo.CuadIndex() + 1
    cuadruplo.InsertarSalto(indice,salto)


def p_Entrada(t):
    '''
    Entrada : KEYWORD_ENTRADA IDENTIFICADOR EntradaA SEMICOLON
    '''
    global cuadruplo,stackOperando
    identificador = t[2]
    cuadruplo.normalCuad("input",identificador,None,None)


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
    global cuadruplo,stackOperando
    identificador = stackOperando.pop()
    cuadruplo.normalCuad("output",identificador,None,None)

def p_Cambio(t):
    '''
    Cambio : KEYWORD_CAMBIO PARENTESIS_IZQ Expresion PARENTESIS_DER BRACKET_IZQ CambioA BRACKET_DER
    '''

def p_CambioA(t):
    '''
    CambioA : CambioCasoAux Bloque FinCambioCaso CambioA
    | empty
    '''

    
def p_CambioCasoAux(t):
    '''
    CambioCasoAux : KEYWORD_CASO ValorSalida COLON
    '''
    global cuadruplo, stackOperando,stackSaltos,temporales,indicetemporales,stackCambio
    op = stackOperando.pop()
    comparador = t[2]
    temporales[indicetemporales] = "temporalCambio"
    result = 't' + str(indicetemporales)
    temporales.append(result)
    indicetemporales = indicetemporales + 1
    cuadruplo.normalCuad('==', op, comparador, result)
    cuadruplo.normalCuad('GOTOF',result,None,None)
    asaltar = cuadruplo.CuadIndex()
    stackOperando.append(op)
    stackSaltos.append(asaltar)
    stackCambio.append(asaltar)

def p_FinCambioCaso(t):
    '''
    FinCambioCaso : 
    '''
    global cuadruplo, stackOperando, stackSaltos, stackCambio
    indice = stackSaltos.pop()
    salto = cuadruplo.CuadIndex() + 1
    cuadruplo.InsertarSalto(indice,salto)


def p_ValorSalida(t):
    '''
    ValorSalida : ValorEnt
    | ValorReal
    | ValorCar
    | ValorBool
    | KEYWORD_NULO
    | LlamadaId
    '''
    #funcion a checar
def p_ValorEnt(t):
    '''
    ValorEnt : CONST_NUMERO_ENT
    '''
    global tablaConstantes,stackOperando,monolito
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = getMemId("entero")
        val =  {"memID":memID, 'tipo':"entero"}
        insertaConstante(t[1],val)
        monolito.insertaConstante(memID,t[1])
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memID'])
        

def p_ValorReal(t):
    '''
    ValorReal : CONST_NUMERO_REAL
    '''
    global tablaConstantes,stackOperando,monolito
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = getMemId("real")
        val =  {"memID":memID, 'tipo':"real"}
        insertaConstante(t[1],val)
        stackOperando.append(memID)
        monolito.insertaConstante(memID,t[1])
    else:
        stackOperando.append(existe['memID'])

def p_ValorCar(t):
    '''
    ValorCar : CONST_CARACTERES
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = getMemId("caracter")
        val =  {"memID":memID, 'tipo':"caracter"}
        insertaConstante(t[1],val)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memID'])

def p_ValorBool(t):
    '''
    ValorBool : CONST_BOOLEANO
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = getMemId("real")
        val =  {"memID":memID, 'tipo':"real"}
        insertaConstante(t[1],val)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memID'])

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
    global checkSemantica, stackOperador, stackOperando,temporales,indicetemporales,cuadruplo
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO AND OR", stackOperador)
    if (top == '&&' or top == '||'):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        sem = checkSemantica.Semantica(op,oper1,oper2)
        memTemporal=setValor(sem)
        stackOperando.append(memTemporal)
        #sem = checkSemantica.Semantica(op,oper1, oper2)
        ##RECUERDA, REPARA LA SEMANTICA AL FINAAAAL , FINAAAL , FINAAAL
        #  def normalCuad(self, operador=None, operando1=None, operando2=None, destino=None):
        cuadruplo.normalCuad(op,oper1,oper2,memTemporal)



#recibe los operadores And y Or
def p_ExpresionAux(t):
    '''
    ExpresionAux : OPERADOR_AND_OR
    '''
    global stackOperador
    stackOperador.append(t[1])

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
    global checkSemantica, stackOperador, stackOperando, temporales,indicetemporales,cuadruplo
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO COMPARATIVO", stackOperador)
    if (top == '<' or top == '>' or top == '~'):
        memTemporal = -1
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        sem = checkSemantica.Semantica(op,oper1,oper2)
        memTemporal = setTemporal(sem)

        stackOperando.append(memTemporal)
   
        #sem = checkSemantica.Semantica(op,oper1, oper2)
        ##RECUERDA, REPARA LA SEMANTICA AL FINAAAAL , FINAAAL , FINAAAL
        cuadruplo.normalCuad(op,oper1,oper2,memTemporal)


#carga los operadores comparativos
def p_ExpresAux(t):
    '''
    ExpresAux : OPERADOR_COMPARATIVO
    '''
    global stackOperador
    stackOperador.append(t[1])


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
    global checkSemantica, stackOperador, stackOperando, indicetemporales,cuadruplo
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO + -", stackOperador)
    if (top == '+' or top == '-'):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        memTemporal = -1
        sem = checkSemantica.Semantica(op,oper1,oper2)
        memTemporal = setTemporal(sem)
        stackOperando.append(memTemporal)
        print("op: ", op,"oper1: ",oper1,"oper2: ",oper2)
       
        #sem = checkSemantica.Semantica(op,oper1, oper2)
        ##RECUERDA, REPARA LA SEMANTICA AL FINAAAAL , FINAAAL , FINAAAL
        cuadruplo.normalCuad(op,oper1,oper2,memTemporal)



#carga los operadores de suma y resta
def p_ExpAux(t):
    '''
    ExpAux : EXP_OPERADOR
    '''
    global stackOperador
    stackOperador.append(t[1])

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
    global checkSemantica, stackOperador, stackOperando,temporales,indicetemporales,cuadruplo
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO * /", stackOperador)
    if (top == '*' or top == '/'):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        sem = checkSemantica.Semantica(op,oper1,oper2)
        memTemporal = setTemporal(sem)
        stackOperando.append(memTemporal)
        #sem = checkSemantica.Semantica(op,oper1, oper2)
        ##RECUERDA, REPARA LA SEMANTICA AL FINAAAAL , FINAAAL , FINAAAL
        cuadruplo.normalCuad(op,oper1,oper2,memTemporal)

 
#inserta los terminos * y / en el stack de operadores
def p_TerminoAux(t):
    '''
    TerminoAux : TERM_OPERADOR
    '''
    global stackOperador
    stackOperador.append(t[1])

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