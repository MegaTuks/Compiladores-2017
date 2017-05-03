# cubo semantico es un diccionario de matrices que tiene de Id los tipos de operador que puede haber
# Ejemplo de como son cada una
# bool=0,int=1,float =2 ,string = 3,error = 4
# +, [
# bool [bool,int,float,string],
# int [bool,int,float,string],
# real [bool, int ,float,string],
# caracter [bool, int ,float,string],
# ]

class claseCuboSemantico:
    def __init__(self):
        self.DataTypes = ['bool', 'int', 'real', 'caracter', 'error']
        self.Cubo = {'+': [[0, 4, 4, 4, 4], [4, 1, 2, 4, 4], [4, 2, 2, 4, 4], [4, 4, 4, 3, 4]],
                     '-': [[0, 4, 4, 4, 4], [4, 1, 2, 4, 4], [4, 2, 2, 4, 4], [4, 4, 4, 4, 4]],
                     '/': [[0, 4, 4, 4, 4], [4, 2, 2, 4, 4], [4, 2, 2, 4, 4], [4, 4, 4, 4, 4]],
                     '*': [[0, 4, 4, 4, 4], [4, 1, 2, 4, 4], [4, 2, 2, 4, 4], [4, 4, 4, 4, 4]],
                     '=': [[0, 4, 4, 4, 4], [4, 1, 4, 4, 4], [4, 4, 2, 4, 4], [4, 4, 4, 3, 4]],
                     '>': [[4, 4, 4, 4, 4], [4, 0, 0, 4, 4], [4, 0, 0, 4, 4], [4, 4, 4, 4, 4]],
                     '<': [[4, 4, 4, 4, 4], [4, 0, 0, 4, 4], [4, 0, 0, 4, 4], [4, 4, 4, 4, 4]],
                     '&&': [[0, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4]],
                     '||': [[0, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4]],
                     'entrada': [[0, 4, 4, 4, 4], [4, 1, 4, 4, 4], [4, 4, 2, 4, 4], [4, 4, 4, 3, 4]],
                     '~': [[0, 4, 4, 4, 4], [4, 0, 4, 4, 4], [4, 4, 0, 4, 4], [4, 4, 4, 0, 4]],
                     }
    def VerSemantica(self, operando1):
      aux = int(operando1 / 10000)
      VerdaderoValor1 = operando1 - aux * 10000
      IndexOP1 = 4
      print("VerdaderoValor1: ", VerdaderoValor1)
      if(VerdaderoValor1 >= 2501 and VerdaderoValor1 <= 5000):
          print("entero1")
          IndexOP1 = 1
      if(IndexOP1 == 4):
          print("Variables dimensionadas necesitan valores enteros para indexar!")
          raise SystemExit
      return IndexOP1


    def SemanticaRet(self, operando1):
        aux = int(operando1 / 10000)
        VerdaderoValor1 = operando1 - aux * 10000
        IndexOP1 = 4
        if(VerdaderoValor1 >= 0 and VerdaderoValor1 <= 2500):
            IndexOP1 = 0
        elif(VerdaderoValor1 >= 2501 and VerdaderoValor1 <= 5000):
            IndexOP1 = 1
        elif(VerdaderoValor1 >= 5001 and VerdaderoValor1 <= 7500):
            IndexOP1 = 2
        elif(VerdaderoValor1 >= 7501 and VerdaderoValor1 <= 10000): 
            IndexOP1 = 3 

        if IndexOP1 == 4:
            print ("Valor de retorno erroneo")
            SystemExit
        return IndexOP1 


    def Semantica(self, operador, operando1, operando2):
        aux = int(operando1 / 10000)
        aux2 = int(operando2 / 10000)
        VerdaderoValor1 = operando1 - aux * 10000
        VerdaderoValor2 = operando2 - aux2 * 10000
        IndexOP1 = 4
        IndexOP2 = 4
        if(VerdaderoValor1 >= 0 and VerdaderoValor1 <= 2500):
            IndexOP1 = 0
        elif(VerdaderoValor1 >= 2501 and VerdaderoValor1 <= 5000):
            print("entero1")
            IndexOP1 = 1
        elif(VerdaderoValor1 >= 5001 and VerdaderoValor1 <= 7500):
            IndexOP1 = 2
        elif(VerdaderoValor1 >= 7501 and VerdaderoValor1 <= 10000): 
            IndexOP1 = 3  
        if(VerdaderoValor2 >= 0 and VerdaderoValor2 <= 2500):  
            IndexOP2 = 0
        elif(VerdaderoValor2 >= 2501 and VerdaderoValor2 <= 5000):
            print("entero2")
            IndexOP2 = 1
        elif(VerdaderoValor2 >= 5001 and VerdaderoValor2 <= 7500):
            IndexOP2 = 2
        elif(VerdaderoValor2 >= 7501 and VerdaderoValor2 <= 10000): 
            IndexOP2 = 3
        # try:
        # 	IndexOP1 = self.DataTypes.index(operando1)
        # 	IndexOP2 = self.DataTypes.index(operando2)

        # except ValueError:
        # 	IndexOP1 = 4
        # 	IndexOP2 = 4


        if IndexOP1 < 5 and IndexOP2 < 5:
            print("sem: ",operador, "IndexOP1: ",IndexOP1, "IndexOP2: ",IndexOP2)
            sem = self.Cubo[operador][IndexOP1][IndexOP2]
            if sem == 4:
                if(IndexOP1 == 0):
                  tipoA = "booleano"
                elif(IndexOP1 == 1):
                  tipoA = "entero"
                elif(IndexOP1 == 2):
                  tipoA = "real"
                elif(IndexOP1 == 3):
                  tipoA = "caracter"

                if(IndexOP2 == 0):
                  tipoB = "booleano"
                elif(IndexOP2 == 1):
                  tipoB = "entero"
                elif(IndexOP2 == 2):
                  tipoB = "real"
                elif(IndexOP2 == 3):
                  tipoB = "caracter"
                print("ERROR TIPOS DE DATOS", tipoA, " y ", tipoB, "NO son compatibles con el operador" ,operador)


                raise SystemExit
                return 4
            else:
                print("sem: ", sem)
                return sem

        else:
            print("\nERROR. Tipos de datos:", operando1, ",", operando2, "y/o operador:", operador, "desconocidos.")
            return None

class Cuadruplos:
    def __init__(self):
        self.cuadruplos = list()

    def normalCuad(self, operador=None, operando1=None, operando2=None, destino=None):
        self.cuadruplos.append((operador, operando1, operando2, destino))
        print("operador:" ,operador , " op1:",operando1, " op2:", operando2 , " destino:",destino)

    def updateCuad(self, index, operador=None, operando1=None, operando2=None, destino=None):
        self.cuadruplos[index] = (operador, operando1, operando2, destino)

    def AssignCuad(self,operador, operando1, destino):
        self.cuadruplos.append((operador, operando1, None, destino))

    def SaltaCuad(self, Goto, destino=None):
      self.cuadruplos.append((Goto, None, "1", destino))
      print("ver como codigicar saltos")

    def CuadIndex(self):
      return len(self.cuadruplos) - 1

    def InsertarSalto(self,indice,salto):
      jump = (self.cuadruplos[indice][0], self.cuadruplos[indice][1], self.cuadruplos[indice][2], salto)
      self.cuadruplos[indice] = jump


    def AgregarSalto(self, indice, expr, destino=None):
      if destino is None:
        destino = len(self.cuadruplos)
      salto = (self.cuadruplos[indice][0], expr, "2", destino)
      self.cuadruplos[indice] = salto
      print("darle update al cuadruplo")

    def EspecialCuad(self, operador, operando1, operando2, destino):
        print("cuadruplo a usar en funciones especiales")

    def CuadSize(self):
        return len(self.cuadruplos)

    def Ultimo(self):
        return self.cuadruplos[-1]

    def imprimir(self):
        print("|---------------------------------------------------------------------------------------------------|")
        print("|-----------------------------------------CUADRUPLOS------------------------------------------------|")
        indice = 0
        for cuad in self.cuadruplos:
            cuadrin='| indice:'+ str(indice).rjust(3,' ') + ' | operador: '+ str(cuad[0]).rjust(5,' ') + ' | operando1: ' + str(cuad[1]).rjust(10,' ') + ' | operando2: '+ str(cuad[2]).rjust(10,' ') + ' | destino:'+ str(cuad[3]).rjust(10,' ')+ ' |'
            print (cuadrin)
            indice = indice + 1
        print("-----------------------------------------------------------------------------------------------------")

# Tabla de simbolos
class TablaSimbolos:
    def __init__(self):
        self.simbolos = dict()
        self.hijos = list()
        self.padre = None
        # agregar atributo name?
    #Funcion para insertar variable a la tabla
    #@id es el identificador de la variable, tipo es un string que denota el tipo de variable que se almacena
    def insertar(self, id, tipo):
        self.simbolos[id] = tipo
    
    #funcion de busqueda, devuelve el tipo, de no existir devuelve none
    def buscar(self, id):
        return self.simbolos.get(id)

     #funcion que anexa una tablasimbolos con otra
     #@hijo es la tabla de simbolos que se le anexara como hijo a esta tabla
    def agregarHijo(self, hijo):
        self.hijos.append(hijo)

    #funcion para indicar cual es la tabla padre de la variable.
    #@pad es la tabla de simbolos padre    
    def agregarPadre(self, pad):
        self.padre = pad
    # funcion para devolver el padre
    # de no existir imprime no existe padre
    #de lo contrario devuelve la tabla simbolos padre    
    def devolverPadre(self):
        if (self.padre is None):
            print("no hay padre al cual ir");
        else:
            return self.padre
    # funcion para devolver el hijo
    # @name es el nombre de la tabla hijo a buscar
    #devuelve hijo si encuentra uno.
    def buscarHijos(self, name):
        for hijo in self.hijos:
            existe = hijo.buscar(name)
            if (existe is not None):
                return hijo

                # def __str__(self):
    #funcion que imprime los valores dentro de la tablaSimbolos
    def imprimir(self):
        i = 0
        for hijo in self.hijos:
            print("Hijo:",hijo.simbolos)
        print ("tablaGlobal",self.simbolos)



#Tabla que maneja las constantes
#almacena la constante y su tipo.
class TablaConstantes:
    def __init__(self):
        self.simbolos = dict()

    def insertar(self, id, tipo):
        self.simbolos[id] = tipo

    def buscar(self, id):
        return self.simbolos.get(id)

    def imprimir(self):
        print("Constantes:",self.simbolos)

class TablaTemporales:
    def __init__(self):
        self.simbolos = dict()

    def insertar(self, id, tipo):
        self.simbolos[id] = tipo

    def buscar(self, id):
        return self.simbolos.get(id)

    def imprimir(self):
        print("Constantes:",self.simbolos)

#clase de procedimeintos en esta manejamos lo relacionado a funciones.
class Procedimientos:
    def __init__(self):
        self.procedimientos = list()
        self.listParam = dict()

    def normalLista(self, id, cuadinicio,cuadruplofin):
        self.procedimientos.append((id, self.listParam[id], cuadinicio,cuadruplofin))
        print("ID Procedimiento:" , id, " # Param:", self.listParam[id] , "inicio:",cuadinicio ,"Final:", cuadruplofin)

    def updateLista(self, index, id, parametros, variables, destino):
        self.procedimientos[index] = (id, parametros, variables, destino)

    def meteParametros(self, id, lista = []):
        self.listParam[id] = lista

    def buscar(self, id):
        return self.listParam.get(id)

    def buscarParam(self, id, param):
        return self.listParam.get(id)[param]['memID']

    def buscarInicio(self, id):
        for proc in self.procedimientos:
            if proc[0] == id:
                return proc[2]
        print ("Se llamo una funcion no existente.")
        raise SystemExit
                

    def buscarFinal(self, id):
        for proc in self.procedimientos:
            if proc[0] == id:
                return proc[3]
        print ("Se llamo una funcion no existente.")
        raise SystemExit
                

    def ListaSize(self):
        return len(self.procedimientos)

    def Ultimo(self):
        return self.procedimientos[-1]

    def imprimir(self):
        indice = 0
        for proc in self.procedimientos:
            print('indice:', indice, 'ID Procedimiento: ', proc[0], '#Param: ', proc[1], 'INICIO: ', proc[2], 'FIN:',
                  proc[3])
            indice = indice + 1


class MemoriaReal:
    def __init__(self, rango = 0): 
        self.booleanos = rango
        self.enteros = rango + 2500
        self.reales = rango + 5000
        self.caracteres =  rango + 7500

        self.cont_bool = self.booleanos
        self.cont_ent = self.enteros
        self.cont_real = self.reales
        self.cont_car = self.caracteres

    def insertaBooleano(self):
        if(self.cont_bool < self.enteros):
            self.cont_bool = self.cont_bool + 1
            return self.cont_bool
        else:
            print("memoria fuera de limites")

    def insertaEntero(self):
        if(self.cont_ent < self.reales):
            self.cont_ent = self.cont_ent + 1
            return self.cont_ent
        else:
            print("memoria fuera de limites")
    
    def insertaReales(self):
        if(self.cont_real < self.caracteres):
            self.cont_real = self.cont_real + 1
            return self.cont_real
        else:
            print("memoria fuera de limites")

    def insertaCaracteres(self):
        if(self.cont_car < self.caracteres + 2500):
            self.cont_car = self.cont_car + 1
            return self.cont_car
        else:
            print("memoria fuera de limites")

    def insertaDimBooleano(self,total):
        if(self.cont_bool + total < self.enteros):
            inicio = self.cont_bool + 1
            self.cont_bool = self.cont_bool + total
            fin = self.cont_bool
            retorno = {'inicio': inicio, 'fin':fin}
            return retorno
        else:
            print("memoria fuera de limites")

    def insertaDimEntero(self,total):
        if(self.cont_ent + total < self.reales):
            inicio = self.cont_ent + 1
            self.cont_ent = self.cont_ent + total
            fin = self.cont_ent
            retorno = {'inicio': inicio, 'fin':fin}
            return retorno
        else:
            print("memoria fuera de limites")

    def insertaDimReales(self,total):
        if(self.cont_real + total < self.caracteres):
            inicio = self.cont_real + 1
            self.cont_real = self.cont_real + total
            fin = self.cont_real
            retorno = {'inicio': inicio, 'fin':fin}
            return retorno
        else:
            print("memoria fuera de limites")

    def insertaDimCaracteres(self,total):
        if(self.cont_car + total < self.caracteres + 2500):
            inicio = self.cont_car + 1
            self.cont_car = self.cont_car + total
            fin = self.cont_car
            retorno = {'inicio': inicio, 'fin':fin}
            return retorno
        else:
            print("memoria fuera de limites")


    def eliminaTemporales(self,topeBool, topeInt,topeReal, topeCar):
        print("funcion de borrado")

class Monolito:      
    def __init__(self):
        self.Monolito = dict()
        self.Constantes = dict()
        self.stack = list()

    def insertaActual(self, memID, value):
        self.Monolito[memID] = value

    def insertaConstante(self,memID,value):
        self.Constantes[memID] = value

    def buscar(self, id):
        if(self.Monolito.get(id) is None):
          return self.Constantes.get(id)
        else:
          return self.Monolito.get(id)

    def insertaStack(self):
        toStack = dict(self.Monolito)
        self.stack.append(toStack)

    def popStack(self):
      return self.stack.pop()

    def imprimir(self):
      print("Monolito: ",self.Monolito)
      print("Constantes: ",self.Constantes)

class MaquinaVirtual:
  def __init__(self):
        self.stack = list()
  
  def Ejecutar(self,cuadruplo,mon, proc, glob):
    indiceActual = 0
    stackIndices = []
    stackIndicesFinales = []
    stackERA = []
    stackParam = 0
    print(cuadruplo.cuadruplos[0][0])
    while(True):
      indiceTemporal = 0
      operador = cuadruplo.cuadruplos[indiceActual][0]
      cuad = cuadruplo.cuadruplos[indiceActual]
      if(operador == "+"):
        Suma(cuad,mon)
      elif(operador == "-"):
        Resta(cuad,mon)
      elif(operador == "*"):
        Multiplicacion(cuad,mon)
      elif(operador == "/"):
        Division(cuad,mon)
      elif(operador == "="):
        Asignar(cuad,mon)
      elif(operador == "output"):
        Salida(cuad,mon)
      elif(operador == "input"):
        Entrada(cuad,mon)
      elif(operador == "GOTOF"):
        indiceTemporal = GotoF(cuad,mon,indiceActual)
      elif(operador == "GOTOT"):
        indiceTemporal = GotoT(cuad,mon,indiceActual)
      elif(operador == "GOTO"):
        indiceTemporal = Goto(cuad,mon) 
      elif(operador == "gosub"):
        print("run Gosub")
        stackParam = 0
        stackIndices.append(indiceActual+1)
        print ("-----regreso a donde se cargo funcion----. ")
        print (stackIndices)
        indiceTemporal = Gosub(cuad,proc)

      elif(operador == "RETU"):
        print("run RETU")
        nuevoIndice = stackIndices.pop()
        indiceTemporal = nuevoIndice - 1

      elif(operador == "ERA"):
        print("run ERA")
        final = ERA(cuad,proc)
        print (final)
        stackIndicesFinales.append(final)
        print ("-----direcciones de retorno al terminar funcion----. ")
        print (stackIndicesFinales)
        stackERA.append(cuad[1])
        print (stackERA)

      elif(operador == "param"):
        stackParam = stackParam + 1
        nega = stackParam * -1
        func = stackERA[-1]
        print (nega)
        Param(cuad, mon, proc, func, nega)
        print (func)

      elif(operador == "ret"):
        print("run retorno")
        print (stackERA)
        idFun = stackERA.pop()
        Retorno(cuad, mon, proc, glob, idFun)
        indiceTemporal = stackIndicesFinales.pop() - 1
        
      elif(operador == "&&"):
        AndOp(cuad,mon)
      elif(operador == "||"):
        OrOp(cuad,mon)
      elif(operador == ">"):
        MayorQue(cuad,mon)
      elif(operador == "<"):
        MenorQue(cuad,mon)
      elif(operador == "?"):
        print("igual que")
        IgualQue(cuad,mon)
      ##Funciones de arreglos
      elif(operador == "ver"):
        Ver(cuad,mon)
      elif(operador == "+v"):
        DirArreglo(cuad,mon)
      ##FIN DE FUNCIONES DE ARREGLO
      elif(operador == "FIN"):
        break;
      if(indiceTemporal == 0):
        indiceActual =  indiceActual + 1 
      else:
        indiceActual =  indiceTemporal + 1



def Suma(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    operando2 =  cuadruplo[2]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    existe2 = monolito.buscar(operando2)
    existeres = monolito.buscar(resultado)
    almacenar = existe + existe2
    print("operando1: ", existe, " + ", existe2, " = ", almacenar)
    monolito.insertaActual(resultado,almacenar)


def Resta(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    operando2 =  cuadruplo[2]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    existe2 = monolito.buscar(operando2)
    existeres = monolito.buscar(resultado)
    almacenar = existe - existe2
    print("operando1: ", existe, " - ", existe2, " = ", almacenar)
    monolito.insertaActual(resultado,almacenar)

def Multiplicacion(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    operando2 =  cuadruplo[2]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    existe2 = monolito.buscar(operando2)
    existeres = monolito.buscar(resultado)
    almacenar = existe * existe2
    print("operando1: ", existe, " * ", existe2, " = ", almacenar)
    monolito.insertaActual(resultado,almacenar)

def Division(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    operando2 =  cuadruplo[2]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    existe2 = monolito.buscar(operando2)
    existeres = monolito.buscar(resultado)
    if(existe2 == 0):
      print("No se puede dividir entre 0")
      raise SystemExit
    else:
      almacenar = existe / existe2
      print("operando1: ", existe, "/ ", existe2, "=", almacenar)
    monolito.insertaActual(resultado,almacenar)

def MayorQue(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    operando2 =  cuadruplo[2]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    existe2 = monolito.buscar(operando2)
    existeres = monolito.buscar(resultado)
    if(existe > existe2):
      almacenar = "verdadero"
    else:
      almacenar = "falso"
    print(existe, " :MAYOR QUE: ", existe2)
    monolito.insertaActual(resultado,almacenar)

def MenorQue(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    operando2 =  cuadruplo[2]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    existe2 = monolito.buscar(operando2)
    existeres = monolito.buscar(resultado)
    if(existe < existe2):
      almacenar = "verdadero"
    else:
      almacenar = "falso"
    print(existe, " :MENOR QUE: ",existe2)
    monolito.insertaActual(resultado,almacenar)  

def IgualQue(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    print("operando1", operando1)
    operando2 =  cuadruplo[2]
    print("operando2", operando2)
    resultado =  cuadruplo[3]
    print("res", resultado)
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    print("operando1:" ,existe)
    existe2 = monolito.buscar(operando2)
    print("opearndo2:" ,existe2)
    existeres = monolito.buscar(resultado)
    print("resultado", existeres)
    if(existe == existe2):
      almacenar = "verdadero"
    else:
      almacenar = "falso"
    monolito.insertaActual(resultado,almacenar)  

def AndOp(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    operando2 =  cuadruplo[2]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    existe2 = monolito.buscar(operando2)
    existeres = monolito.buscar(resultado)
    if(existe == "verdadero"):
      existe = True
    else:
      existe = False
    if(existe2 == "verdadero"):
      existe2 = True
    else:
      existe2 = False
    if(existe and existe2):
      existeres =  "verdadero"
    else:
      existeres = "falso"
    print("cuadruplo AND : operador1: ", existe, "operando2", existe2, "resultado: ", existeres)
    monolito.insertaActual(resultado,existeres)

def OrOp(cuadruplo,monolito):
    operando1 = cuadruplo[1]
    operando2 =  cuadruplo[2]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaOperando2 = int(operando2)
    checaResultado = int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaOperando2 != operando2):
      operando2 =  monolito.buscar(checaOperando2)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    existe2 = monolito.buscar(operando2)
    existeres = monolito.buscar(resultado)
    if(existe == "verdadero"):
      existe = True
    else:
      existe = False
    if(existe2 == "verdadero"):
      existe2 = True
    else:
      existe2 = False
    if( existe or existe2):
      existeres =  "verdadero"
    else:
      existeres = "falso"
    print("cuadruplo OR : operador1: ", existe, "operando2", existe2,"resultado: ",existeres)
    monolito.insertaActual(resultado,existeres)

def Entrada(cuadruplo,monolito):
  ## ver como funciona luego
    operando1 = cuadruplo[1]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    #fin de la obtencion de direcciones 
    print("operando1", operando1)
    existe = monolito.buscar(operando1)
    print("operando1:" ,existe)
    monolito.insertaActual(operando1,existe)
    print("resultado = ", monolito.buscar(operando1))

def Salida(cuadruplo,monolito):
    ## ver como funciona luego
    operando1 = cuadruplo[1]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    print("Salida =  operando1:" ,existe)
    print(existe)

def Asignar( cuadruplo,monolito):
    operando1 = cuadruplo[1]
    resultado =  cuadruplo[3]
    #validar que sean direcciones de tener algun valor real saldran diferentes en la comparacion
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    checaResultado =  int(resultado)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    if(checaResultado != resultado):
      resultado = monolito.buscar(checaResultado)
    #fin de la obtencion de direcciones 
    existe = monolito.buscar(operando1)
    print("operando1:" ,existe)
    existeres = monolito.buscar(resultado)
    monolito.insertaActual(resultado,existe)
    print("Asignacion   Direccion: ",resultado, "valor: ",existe )

def GotoT(cuadruplo, monolito,indice):
    operando1 = cuadruplo[1]
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    resultado =  cuadruplo[3]
    print("res", resultado)
    existe = monolito.buscar(operando1)
    print("operando1:" ,existe)
    existeres = monolito.buscar(resultado)
    print("existeres",existeres)
    if(existe == "verdadero"):
      indice = resultado - 1
    else:
      indice = indice
    #monolito.insertaActual(resultado,existe)
    print("GotoF = operando1: ",existe," hacia a ", indice)
    return indice

def GotoF(cuadruplo, monolito,indice):
    operando1 = cuadruplo[1]
    print("operando1", operando1)
    #indicando que esa temporal almacena la direccion de memoria indicada
    checaOperando1 = int(operando1)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != operando1):
      operando1 = monolito.buscar(checaOperando1)
    resultado =  cuadruplo[3]
    existe = monolito.buscar(operando1)
    if(existe == "falso"):
      print("es falso, salto a :" ,resultado)
      indice = resultado - 1
    else:
      indice = indice
    #monolito.insertaActual(resultado,existe)
    print("GotoF = operando1: ",existe," hacia a", indice)
    return indice

def Goto(cuadruplo, monolito):
    resultado =  cuadruplo[3]
    print("GOTO", resultado)
    return resultado - 1
    #monolito.insertaActual(resultado,existe)

def Gosub(cuadruplo, proced):
    resultado =  proced.buscarInicio(cuadruplo[1])
    print ("GOSUB", resultado)
    return resultado - 1

def ERA(cuadruplo, proced):
    resultado =  proced.buscarFinal(cuadruplo[1])
    print ("ERA", resultado)
    return resultado

def Param(cuadruplo, monolito, proced, funci, negativo):
    param =  proced.buscarParam(funci, negativo)
    temp = cuadruplo[1]
    checaOperando1 = int(temp)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != temp):
      temp = monolito.buscar(checaOperando1)

    #fin de la obtencion de direcciones 
    existe = monolito.buscar(temp)
    print("operando1:" ,existe)
    existeres = monolito.buscar(param)
    monolito.insertaActual(param,existe)
    print("resultado = ", monolito.buscar(param))


    print ("param = ", param)

def Retorno(cuad, monolito, proc, glob, idFun):
    exists = glob.buscar(idFun)
    print ("HOLA DOROTI")
    resul = exists['memID']
    temp = cuad[3]
    print (temp)
    print (resul)
    checaOperando1 = int(temp)
    checaResultado =  int(resul)
    #validar si es direccion o llave y transformarlo en la llave que es
    if(checaOperando1 != temp):
      temp = monolito.buscar(checaOperando1)
    if(checaResultado != resul):
      resul = monolito.buscar(checaResultado)

    #fin de la obtencion de direcciones 
    existe = monolito.buscar(temp)
    print("operando1:" ,existe)
    existeres = monolito.buscar(resul)
    monolito.insertaActual(resul,existe)
    print("resultado = ", monolito.buscar(resul))

    print ("retorno = ", idFun, "resul ", resul)


def Ver(cuadruplo,monolito):
    valorVerificable =  cuadruplo[1]
    menor = cuadruplo[2]
    mayor = cuadruplo[3]
    checaValorVerificable =  int(valorVerificable)
    if(checaValorVerificable != valorVerificable):
        valorVerificable = monolito.buscar(checaValorVerificable)
    valor = monolito.buscar(valorVerificable)
    print("valorVer: ",valor,"menor: ",menor,"mayor: ",mayor)
    if(not ( (valor >= menor) and (valor <= mayor) ) ):
      print("valor fuera del rango de arreglo")
      raise SystemExit

def DirArreglo(cuadruplo,monolito):
    dirBase = cuadruplo[1]
    desplazamiento =  cuadruplo[2]
    print("desplazamiento: ",desplazamiento)
    almacenaDezplazamiento = cuadruplo[3]
    checaDesplazamiento = int(desplazamiento)
    if(checaDesplazamiento != desplazamiento):
        desplazamiento = monolito.buscar(checaDesplazamiento)
    suma = monolito.buscar(desplazamiento)
    resultado =  dirBase + suma
    print("suma: ",suma, " + DirBase: ",dirBase ," = ",resultado)
    monolito.insertaActual(almacenaDezplazamiento,resultado)

















 # def imprimir(self):
 #        print("|---------------------------------------------------------------------------------------------------|")
 #        print("|-----------------------------------------CUADRUPLOS------------------------------------------------|")
 #        indice = 0
 #        for cuad in self.cuadruplos:
 #            cuadrin='| indice:'+ str(indice).rjust(3,' ') + ' | operador: '+ str(cuad[0]).rjust(5,' ') + ' | operando1: ' + str(cuad[1]).rjust(10,' ') + ' | operando2: '+ str(cuad[2]).rjust(10,' ') + ' | destino:'+ str(cuad[3]).rjust(10,' ')+ ' |'
 #            print (cuadrin)
 #            indice = indice + 1
 #        print("-----------------------------------------------------------------------------------------------------")



