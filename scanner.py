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
    raise SystemExit
    t.lexer.skip(1)

def insertaConstante(iden,tipo):
    global tablaConstantes,memoriaConstante
    constante = iden
    existe = tablaConstantes.buscar(constante)
    if (existe is None):

        tablaConstantes.insertar(constante,tipo)
    else:
        x = "la magia de disney"

#recibe un string de caracteres, del cual determina su tipo de variable
#genera una direccion de memoria y la devuelve al que haya llamadao la funcion
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

#calcularMatriz id recibe de parametros las casillas de entrada de la izquierda de la derecha
# y genera un diccionario que recibe {'inicio':primeracasilla, 'fin':ultimacasilla}
def calcularMatrizId(tipo,izquierda, derecha):
    global memoriaGlobal
    total = izquierda * derecha
    if (tipo == "real"):
        memID = memoriaGlobal.insertaDimReales(total)
    elif (tipo == "booleano"):
        memID = memoriaGlobal.insertaDimBooleano(total)
    elif (tipo == "caracter"):
        memID = memoriaGlobal.insertaDimCaracteres(total)
    elif (tipo == "entero"):
        memID = memoriaGlobal.insertaDimEntero(total)
    return memID

#Genera los cuadruplos para verificar que las expresiones del arreglo o matriz no se excedan
# si el dicionario tiene 5 elementos es arreglo
# de tener 6 es matriz
# el .5 se usa para definir una variable que almacena una direccion de memoria
#cuadruplo interpreta la funcion
def VerificadorCuad(diccionario, opExpresionArr,opExpArr2 = None):
    global checkSemantica,monolito,cuadruplo, stackOperando,tablaConstantes
    val = checkSemantica.VerSemantica(opExpresionArr)
    if(len(diccionario) == 5):
        tope = diccionario['casillas'] - 1
        dirBase = diccionario['memID']
        cuadruplo.normalCuad('ver', opExpresionArr, 0, tope)
        temp = setTemporal(val)
        cuadruplo.normalCuad('+v', dirBase, opExpresionArr, temp)
        temp = temp + 0.5
        stackOperando.append(temp)
    elif(len(diccionario) == 6):
        topeIzquierdo = diccionario['izquierda'] - 1
        topeDerecho = diccionario['derecha'] - 1
        dirBase = diccionario['memID']
        cuadruplo.normalCuad('ver',opExpresionArr, 0, topeIzquierdo)
        cuadruplo.normalCuad('ver',opExpArr2,0,topeDerecho)
        #constante
        constanteDimension = tablaConstantes.buscar(diccionario['derecha'])
        tempo1 = setTemporal(1)
        cuadruplo.normalCuad('*',opExpresionArr,constanteDimension['memID'],tempo1)
        tempo2 = setTemporal(1)
        cuadruplo.normalCuad('+',tempo1,opExpArr2,tempo2)
        temp = setTemporal(val)
        cuadruplo.normalCuad('+v',dirBase,tempo2,temp)
        temp = temp + 0.5
        stackOperando.append(temp)

#genera una variable temporal
#dependiendo de tipo num es el tipo de temporal que genera
#la almacena en una tabla ademas de insertarla en el monolito
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
    tablaTemporales.insertar(result,paraTabla)
    valor = setValor(tipo)
    monolito.insertaActual(memID,valor)
    return memID

#Genera un valor default para un arreglo o matriz de direcciones
#tipo es el tipo, inicio la direccion de inicio y fin la direccion final.
def setValorDim(tipo,inicio,fin):
    global monolito
    if (tipo == "real"):
        valor = 0.0
    elif (tipo == "booleano"):
        valor ="falso"
    elif (tipo == "caracter"):
        valor = "n/a"
    elif (tipo == "entero"):
        valor = 0
    while (inicio <= fin):
        monolito.insertaActual(inicio,valor)
        inicio = inicio + 1

#genera un valor default para una variable , temporal o constante.
def setValor(tipo):
    if (tipo == "real"):
        return 0.0
    elif (tipo == "booleano"):
        return "falso"
    elif (tipo == "caracter"):
        return "n/a"
    elif (tipo == "entero"):
        return 0
#al definir funciones make param inserta sus parametros en la lista de procedimientos.
def makeParam(paramID, stackActual):
    global listaprocedimientos,cuadruplo
    lista = listaprocedimientos.buscar(paramID)
    if (lista is None):
        print ("error en la funcion")
        raise SystemExit
    else:
        longitudTotal = len(lista)
        longitudActual = len(stackActual)
        if(longitudTotal == 0):
            paramActual = -1
        else:
            paramActual = longitudTotal - longitudActual 
        return paramActual

import ply.lex as lex

lexer = lex.lex()

#funcion para simular los vacios.
def p_empty(p):
    'empty :'
    pass
#funcion que maneja errores de tener errores lo marca y deja de correr.
def p_error(t):
    print("Error de sintaxis en '%s'" % t.value)

#diagrama de sintaxis Inicial del pograma , Funcion principal Se declaran PRIMERO las variables globales, luego lsa funciones
def p_Programa(t):
    '''
      Programa : Globales ProgramaInicio ProgramaA FuncionPrincipal
    '''
    global tablaGlobal, tablaSimbolosActual, tablaConstantes,cuadruplo,listaprocedimientos
    cuadruplo.normalCuad('FIN',None,None,None)
    tablaSimbolosActual.imprimir()
    tablaConstantes.imprimir()
    cuadruplo.imprimir()
    listaprocedimientos.imprimir()
    monolito.imprimir()
    maquina = MaquinaVirtual()
    maquina.Ejecutar(cuadruplo,monolito, listaprocedimientos, tablaGlobal)


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
      ProgramaA : Funcion ProgramaA
      | empty
    '''
#diagrama de sintaxis para la definicion de variables globales
def p_Globales(t):
    '''
      Globales : Declaracion Globales
      | Asignacion Globales
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

#auxiliar de principal par aal momento de encontrar la keyword principal generar los saltos de cuadruplo y 
#acciones de resolucion de memoria necesarios.
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

#diagrama de sintaxis de funcion , codigo se ejecuta en sus auxiliares
def p_Funcion(t):
    '''
    Funcion : FuncionAux PARENTESIS_IZQ FuncionA PARENTESIS_DER Bloque FinFuncion
    '''

#auxiliar qeu denomina el final de una funcion, inserta el cuadruplo de RETU
#ademas de liberar la memoria necesaria de liberar.
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

#almacena los valores necesarios en tablasimbolos actual, tabla global , almacena el nombre
# e inserta la direccion de memoria en el monolito.
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


#funcion para meter los valores de los parametros dentro de funcion y a lista parametros que maneja los parametros necesarios.
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
            tipoPar = {'tipo':tipo, 'memID':memID}
            listaParametros.append(parametro)
            tablaSimbolosActual.insertar(identificador, tipoPar)
            monolito.insertaActual(memID,valorDefault)
        else:
            print("parametro declarado previamente, o variable global comparte su nombre")
            raise SystemExit

#recursisvidad en caso de tener mas de 1 parametro.
def p_FuncionB(t):
    '''
    FuncionB : COMA FuncionA
    | empty
    '''
#diagrama principal donde declara las posible sacciones de un bloque
def p_Bloque(t):
    '''
    Bloque : BRACKET_IZQ BloqueA BRACKET_DER
    '''
#diagrama de las acciones de bloque es recursiva
#para que el bloque no tenga un tamano finito.
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
#genera cuadruplos de re y las operaciones necesarias apra correr en cuadruplo.
def p_RetornoAux(t):
    '''
    RetornoAux : KEYWORD_RETORNO Expresion SEMICOLON
    '''
    global cuadruplo, stackOperando, nuevaFuncion, checkSemantica
    op = stackOperando.pop()
    retorno =  t[1]
    existe = tablaGlobal.buscar(nuevaFuncion)
    tipoRet = existe['tipo']
    sem = checkSemantica.SemanticaRet(op)
    if tipoRet == "entero" and sem == 1:
        var1 = 0
    elif tipoRet == "booleano" and sem == 0:
        var1 = 0
    elif tipoRet == "real" and sem == 2:
        var1 = 0
    elif tipoRet == "caracter" and sem == 3:
        var1 = 0
    else:
        print ("Tipo de retorno incopatible")
        raise SystemExit
    cuadruplo.normalCuad('ret', None, None, op)

#maneja la funcionalidad de declaracion
#genera valores de monolito
#almacena la variable en la tabla de simbolos (previamente checa que no exista)
#ALmacena valores en el monolito.
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
            if(len(existeArreglos) == 2):
                # calcular casillas
                izquierda = existeArreglos['izquierda']
                derecha = existeArreglos['derecha']
                memID = calcularMatrizId(tipo, izquierda, derecha) 
                valorDefault = setValor(tipo)
                insert = {'tipo':tipo,'memID':memID['inicio'], 'inicio':memID['inicio'],'fin':memID['fin'],'izquierda':existeArreglos['izquierda'], 'derecha':existeArreglos['derecha'] }
                #guardar en tabla de simbolos
                tablaSimbolosActual.insertar(identificador, insert)
                #meter valores default encasillas
                setValorDim(tipo,memID['inicio'],memID['fin'])
            else:
                casillas = existeArreglos['casillas']
                memID = calcularMatrizId(tipo, casillas, 1) 
                valorDefault = setValor(tipo)
                insert = {'tipo':tipo,'memID':memID['inicio'], 'inicio':memID['inicio'],'fin':memID['fin'],'casillas':existeArreglos['casillas'] }
                #guardar en tabla de simbolos
                tablaSimbolosActual.insertar(identificador, insert)
                # calcular valores default en casillas
                setValorDim(tipo,memID['inicio'],memID['fin'])
                #guardar en tabla de simbolos
    else:
        print("Variable declarada previamente, o variable global comparte su nombre")
        raise SystemExit
    
#devuelve a declaracion diccionario si tiene casillas(osease si es matriz o arreglo)
def p_DeclaracionA(t):
    '''
    DeclaracionA : ArregloAux DeclaracionB
    | empty
    '''

    if(t[1] is  not None):
        if(t[2] is None):
            dimension = {'casillas': t[1]['casillas']}
            t[0] = dimension
        else:
            dimension = {'izquierda' : t[1]['casillas'], 'derecha':t[2]['casillas']}
            t[0] = dimension


        #t[0] = {'arreglo':t[1],'matriz':t[2] }
# dicionario recibido por declaracion a , interpretado para definir si es vector o arreglo.
def p_ArregloAux(t):
    '''
    ArregloAux : CORCHETE_IZQ CONST_NUMERO_ENT CORCHETE_DER
    '''
    global tablaConstantes,stackOperando,monolito
    existe = None
    existe = tablaConstantes.buscar(t[2])
    if (existe is None):
        memID = getMemId("entero")
        val =  {"memID":memID, 'tipo':"entero"}
        insertaConstante(t[2],val)
        monolito.insertaConstante(memID,t[2])

    t[0] = {'casillas': t[2]}
    
def p_DeclaracionB(t):
    '''
    DeclaracionB : ArregloAux
    | empty
    '''
    t[0] = t[1]

#genera cuadruplo de asignacion
#recibe exp
#maneja funcionalidad con Arreglos y MAtrices
def p_Asignacion(t):
    '''
    Asignacion : IDENTIFICADOR AsignacionA OPERADOR_IGUAL Expresion SEMICOLON
    '''
    global tablaSimbolosActual,tablaGlobal,cuadruplo,stackOperando,checkSemantica,monolito
    identificador = t[1]
    existe = tablaSimbolosActual.buscar(identificador)
    existeGlobal = tablaGlobal.buscar(identificador)
    if(existe is  None):
        if(existeGlobal is  None):
            print("VARIABLE no declarada previamente") 
            raise SystemExit
        else:
            if(len(existeGlobal) == 2):
                op1 = stackOperando.pop
                checkSemantica.Semantica('=',op1,existeGlobal['memID'])
                cuadruplo.normalCuad('=',op1,None,existeGlobal['memID'])
            elif(len(existeGlobal) == 5):
                opExpresion = stackOperando.pop()
                expresion =  monolito.buscar(opExpresion)
                opArreglo = stackOperando.pop()
                expresionArr =  monolito.buscar(opArreglo)
                VerificadorCuad(existeGlobal, opArreglo)
                casillaActual = stackOperando.pop()
                cuadruplo.normalCuad('=',opExpresion,None,casillaActual)
            elif(len(existeGlobal) == 6):
                opExpresion = stackOperando.pop()
                expRes =  monolito.buscar(opExpresion)
                opExpresionDer = stackOperando.pop()
                expDer =  monolito.buscar(opExpresionDer)
                opExpresionIzq = stackOperando.pop()
                expIzq = monolito.buscar(opExpresionIzq)
                VerificadorCuad(existeGlobal,opExpresionIzq, opExpresionDer)
                aAlmacenar = stackOperando.pop()
                cuadruplo.normalCuad('=',opExpresion,None,aAlmacenar)

    else:
        if(len(existe) == 2):
            op1 = stackOperando.pop()
            checkSemantica.Semantica('=',op1,existe['memID'])
            cuadruplo.normalCuad('=',op1,None,existe['memID'])
        elif(len(existe) == 5):
            opExpresion = stackOperando.pop()
            expresion =  monolito.buscar(opExpresion)
            opArreglo = stackOperando.pop()
            expresionArr =  monolito.buscar(opArreglo)
            VerificadorCuad(existe, opArreglo)
            casillaActual = stackOperando.pop()
            cuadruplo.normalCuad('=',opExpresion,None,casillaActual)
        elif(len(existe) == 6):
            opExpresion = stackOperando.pop()
            expRes =  monolito.buscar(opExpresion)
            opExpresionDer = stackOperando.pop()
            expDer =  monolito.buscar(opExpresionDer)
            opExpresionIzq = stackOperando.pop()
            expIzq = monolito.buscar(opExpresionIzq)
            VerificadorCuad(existe,opExpresionIzq,opExpresionDer)
            aAlmacenar = stackOperando.pop()
            cuadruplo.normalCuad('=',opExpresion,None,aAlmacenar)


#asignacion de valores dimensionados
def p_AsignacionA(t):
    '''
    AsignacionA : CORCHETE_IZQ Expresion CORCHETE_DER AsignacionB
    | empty
    '''
#asignacion de valores bi dimensionados.
def p_AsignacionB(t):
    '''
    AsignacionB : CORCHETE_IZQ Expresion CORCHETE_DER
    | empty
    '''
#diagrama de llamada funcion
def p_LlamadaFuncion(t):
    '''
    LlamadaFuncion : LlamadaAux PARENTESIS_IZQ LlamadaFuncionA PARENTESIS_DER finLlamada
    '''
#auxiliar de llamada funcion quealmacena el nombre de la funcion y sus respectivos valores. 
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
        listaprocedimientos.imprimir()
        iden = list(listaprocedimientos.buscar(identificador))
        
        stackParam.append(iden)
        procedureName.append(identificador)
        cuadruplo.normalCuad('ERA', identificador, None, None)



def p_LlamadaFuncionA(t):
    '''
    LlamadaFuncionA :  ParamAux  LlamadaFuncionB
    | empty
    '''   
#maneja los parametros que se fueran a usar
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
        x=0
    else:

        expresion = stackOperando.pop()
        paramNo = 'param#' + str(param)
        cuadruplo.normalCuad('param', expresion, None, paramNo)
        listaPar.pop()
        stackParam.append(listaPar)

def p_LlamadaFuncionB(t):
    '''
    LlamadaFuncionB : COMA LlamadaFuncionA
    | empty
    '''
#funcion que finaliza el fin de la llamada
def p_finLlamada(t):
    '''
    finLlamada : 
    '''
    global cuadruplo, stackOperando,procedureName, tablaSimbolosActual, tablaGlobal
    iden =  procedureName.pop()
    cuadruplo.normalCuad('gosub', iden, None, None)
    existe = tablaGlobal.buscar(iden)
    stackOperando.append(existe['memID']) 


def p_Ciclo(t):
    '''
    Ciclo : KEYWORD_MIENTRAS PARENTESIS_IZQ CicloInicio Expresion PARENTESIS_DER CicloAux Bloque FinCiclo
    '''
def p_CicloInicio(t):
    '''
    CicloInicio : 
    '''
    global cuadruplo, stackSaltos
    salto =  cuadruplo.CuadIndex() + 1
    stackSaltos.append(salto)


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

def p_FinCiclo(t):
    '''
    FinCiclo : 
    '''
    global tablaSimbolosActual,tablaGlobal,stackOperando,cuadruplo,stackSaltos
    #print("Cuadruplo Indice: ",cuadruplo.CuadIndex())
    indice = stackSaltos.pop()
    regresoA = stackSaltos.pop()
    cuadruplo.normalCuad('GOTO',None,None,regresoA)
    salto = cuadruplo.CuadIndex() + 1
    cuadruplo.InsertarSalto(indice,salto)



def p_LlamadaId(t):
    '''
    LlamadaId : LlamadaFuncion
    | Terminal
    '''
    #funcion a checar
#funcion para manejar terminales y meterlos al stackde operandos
# sean variables, vectores o matrices.
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
            if(len(existeGlobal) == 2):
                stackOperando.append(existeGlobal['memID'])
            elif(len(existeGlobal) == 5):
                expArr =  stackOperando.pop()
                VerificadorCuad(existeGlobal, expArr)
            elif(len(existeGlobal) == 6):
                expArr =  stackOperando.pop()
                expArrDer = stackOperando.pop()
                VerificadorCuad(existeGlobal, expArr,expArrDer)
    else:
        if(len(existe) == 2):
            stackOperando.append(existe['memID'])
        elif(len(existe) == 5):
            expArr =  stackOperando.pop()
            VerificadorCuad(existe, expArr)
        elif(len(existe) == 6):
            expArr =  stackOperando.pop()
            expArrDer = stackOperando.pop()
            VerificadorCuad(existe, expArrDer,expArr)


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
#devuelve el keyword del tipo a los diagramas que utilicen Tipo
def p_Tipo(t):
    '''
    Tipo : KEYWORD_TYPE_BOOLEANO
    | KEYWORD_TYPE_ENTERO
    | KEYWORD_TYPE_REAL
    | KEYWORD_TYPE_CARACTERES
    '''
    t[0] = t[1]

#diagrama de sintaxis de condicion
def p_Condicion(t):
    '''
    Condicion : CondicionSi CondicionA
    '''
#diagrama de sintaxis de condicionSi Genera cuadruplo goto
#almacena direccion del gotof
#la devuelve en sino o cuando se cierra
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

def p_CondicionA(t):
    '''
    CondicionA : Bloque CondicionSino
    |  Bloque
    '''
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

#ACTUALIZA SALTO de goto, diagrama auxiliar
def p_FinSino(t):
    '''
    FinSino :
    '''
    global cuadruplo,stackOperando,stackSaltos
    indice = stackSaltos.pop()
    salto = cuadruplo.CuadIndex() + 1
    cuadruplo.InsertarSalto(indice,salto)

#diagrama de sintaxis para entrada
def p_Entrada(t):
    '''
    Entrada : KEYWORD_ENTRADA IDENTIFICADOR EntradaA SEMICOLON
    '''
    global cuadruplo,stackOperando,tablaSimbolosActual,tablaGlobal
    identificador = t[2]
    existe = tablaSimbolosActual.buscar(identificador)
    if(len(existe) == 2):
        cuadruplo.normalCuad("input",existe['memID'],None,None)
    else:
        print("no se permite entrada con variables dimensionadas")
        raise SystemExit

#diagramaauxiliar para entrada de enteros.
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
#diagrama para valores de salida
def p_Salida(t):
    '''
    Salida : KEYWORD_SALIDA Expresion SEMICOLON
    '''
    global cuadruplo,stackOperando
    identificador = stackOperando.pop()
    cuadruplo.normalCuad("output",identificador,None,None)
#funcion de cambio para simular switch case
def p_Cambio(t):
    '''
    Cambio : KEYWORD_CAMBIO PARENTESIS_IZQ Expresion PARENTESIS_DER BRACKET_IZQ CambioA BRACKET_DER
    '''
#funcion auxiliar para switch case.
def p_CambioA(t):
    '''
    CambioA : CambioCasoAux Bloque FinCambioCaso CambioA
    | empty
    '''

#funcionalidad para caso cambio .    
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
#auxiliar para definri fin de caso de uso.
def p_FinCambioCaso(t):
    '''
    FinCambioCaso : 
    '''
    global cuadruplo, stackOperando, stackSaltos, stackCambio
    indice = stackSaltos.pop()
    salto = cuadruplo.CuadIndex() + 1
    cuadruplo.InsertarSalto(indice,salto)

#valor a devolver en Expresion su valor mas granular
# se maneja en auxiliares para identificar tu tipo y las funciones apropiadas.
def p_ValorSalida(t):
    '''
    ValorSalida : ValorEnt
    | ValorReal
    | ValorCar
    | ValorBool
    | KEYWORD_NULO
    | LlamadaId
    '''
    #funcion a checar enteros
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
        
#funcion a checar reales
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

#funcion a checar caracteres.
def p_ValorCar(t):
    '''
    ValorCar : CONST_CARACTERES
    '''
    global tablaConstantes,stackOperando,monolito
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = getMemId("caracter")
        val =  {"memID":memID, 'tipo':"caracter"}
        insertaConstante(t[1],val)
        stackOperando.append(memID)
        monolito.insertaConstante(memID,t[1])
    else:
        stackOperando.append(existe['memID'])

#almacena tipo booleano
def p_ValorBool(t):
    '''
    ValorBool : KEYWORD_FALSO
    | KEYWORD_VERDADERO
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = getMemId("booleano")
        val =  {"memID":memID, 'tipo':"booleano"}
        insertaConstante(t[1],val)
        stackOperando.append(memID)
        monolito.insertaConstante(memID,t[1])
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
    if (top == '&&' or top == '||'):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        sem = checkSemantica.Semantica(op,oper1,oper2)
        memTemporal = setTemporal(sem)
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
    if (top == '+' or top == '-'):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        memTemporal = -1
        sem = checkSemantica.Semantica(op,oper1,oper2)
        memTemporal = setTemporal(sem)
        stackOperando.append(memTemporal)
       
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

