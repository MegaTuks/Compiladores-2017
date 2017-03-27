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
      return len(self.cuadruplos) - 1
      print("ver como codigicar saltos")

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
        indice = 0
        for cuad in self.cuadruplos:
            print('indice:', indice, 'operador: ', cuad[0], 'operando1: ', cuad[1], 'operando2: ', cuad[2], 'destino:',
                  cuad[3])
            indice = indice + 1