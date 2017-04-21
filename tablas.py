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
        self.Cubo = {'+': [[0, 1, 2, 4, 4], [1, 1, 2, 4, 4], [2, 2, 2, 4, 4], [4, 4, 4, 3, 4]],
                     '-': [[0, 1, 2, 4, 4], [1, 1, 2, 4, 4], [2, 2, 2, 4, 4], [4, 4, 4, 4, 4]],
                     '/': [[0, 1, 2, 4, 4], [1, 1, 2, 4, 4], [2, 2, 2, 4, 4], [4, 4, 4, 3, 4]],
                     '*': [[0, 1, 2, 4, 4], [1, 1, 2, 4, 4], [2, 2, 2, 4, 4], [4, 4, 4, 3, 4]],
                     '=': [[0, 4, 4, 4, 4], [4, 1, 4, 4, 4], [4, 4, 2, 4, 4], [4, 4, 4, 4, 4]],
                     '>': [[4, 4, 4, 4, 4], [4, 0, 0, 4, 4], [4, 0, 0, 4, 4], [4, 4, 4, 4, 4]],
                     '<': [[4, 4, 4, 4, 4], [4, 0, 0, 4, 4], [4, 0, 0, 4, 4], [4, 4, 4, 4, 4]],
                     '&&': [[0, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4]],
                     '||': [[0, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4]],
                     'entrada': [[0, 4, 4, 4, 4], [4, 1, 4, 4, 4], [4, 4, 2, 4, 4], [4, 4, 4, 3, 4]]
                     }

    def Semantica(self, operador, operando1, operando2):
        #aux = int(operando1/10000)
        #aux2 = int(operando2/10000)
        #VerdaderoValor1 = operando1 - aux*10000
        #VerdaderoValor2 = operando2 - aux2*10000
        #IndexOP1 = 4
        #IndexOP2 = 4
        #if(VerdaderoValor1 >= 0 and VerdaderoValor1 <= 2500):
        #    IndexOP1 = 0
        #elif(VerdaderoValor1 >= 2501 and VerdaderoValor1 <= 5000):
        #    IndexOP1 = 1
        #elif(VerdaderoValor1 >= 5001 and VerdaderoValor1 <= 7500):
        #    IndexOP1 = 2
        #elif(VerdaderoValor1 >= 7501 and VerdaderoValor1 <= 10000): 
        #    IndexOP1 = 3  
        #if(VerdaderoValor2 >= 0 and VerdaderoValor2 <= 2500):
        #    IndexOP2 = 0
        #elif(VerdaderoValor2 >= 2501 and VerdaderoValor2 <= 5000):
        #    IndexOP2 = 1
        #elif(VerdaderoValor2 >= 5001 and VerdaderoValor2 <= 7500):
        #    IndexOP2 = 2
        #elif(VerdaderoValor2 >= 7501 and VerdaderoValor2 <= 10000): 
        #    IndexOP2 = 3
        try:
        	IndexOP1 = self.DataTypes.index(operando1)
        	IndexOP2 = self.DataTypes.index(operando2)

        except ValueError:
        	IndexOP1 = 4
        	IndexOP2 = 4


        if IndexOP1 < 5 and IndexOP2 < 5:
            sem = self.Cubo[operador][IndexOP1][IndexOP2]
            if sem == 4:
                print("\nERROR TYPE MISMATCH. Los operandos:", operando1, "y", operando2,
                      "no son compatibles con el operador:", operador)
                return 4

            else:
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

#clase de procedimeintos en esta manejamos lo relacionado a funciones.
class Procedimientos:
    def __init__(self):
        self.procedimientos = list()
        self.listParam = dict()

    def normalLista(self, id, cuadruplo):
        self.procedimientos.append((id, self.listParam[id], cuadruplo))
        print("ID Procedimiento:" , id, " # Param:", self.listParam[id] , "Destino:", cuadruplo)

    def updateLista(self, index, id, parametros, variables, destino):
        self.procedimientos[index] = (id, parametros, variables, destino)

    def meteParametros(self, id, lista = []):
        self.listParam[id] = lista

    def buscar(self, id):
        return self.listParam.get(id)

    def ListaSize(self):
        return len(self.procedimientos)

    def Ultimo(self):
        return self.procedimientos[-1]

    def imprimir(self):
        indice = 0
        for proc in self.procedimientos:
            print('indice:', indice, 'ID Procedimiento: ', proc[0], '#Param: ', proc[1], '#Variables: ', proc[2], 'Destino:',
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

    def insertaBooleano(self,valor):
        if(self.cont_bool < self.enteros):
            self.cont_bool = self.cont_bool + 1
            return self.cont_bool
        else:
            print("memoria fuera de limites")

    def insertaEntero(self,valor):
        if(self.cont_ent < self.reales):
            self.cont_ent = self.cont_ent + 1
            return self.cont_ent
        else:
            print("memoria fuera de limites")
    
    def insertaReales(self,valor):
        if(self.cont_real < self.caracteres):
            self.cont_real = self.cont_real + 1
            return self.cont_real
        else:
            print("memoria fuera de limites")

    def insertaCaracteres(self,memID,valor):
        if(self.cont_car < caracteres + 2500):
            self.cont_car = self.cont_car + 1
            return self.cont_car
        else:
            print("memoria fuera de limites")

    def eliminaTemporales(self,topeBool, topeInt,topeReal, topeCar):
        print("funcion de borrado")

