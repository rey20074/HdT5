# Universidad del Valle de Guatemala
# José Rodrigo Barrera Carnet: 20807 y Mariano Reyes Carnet: 20074
# Realizado a partir de ejemplos en clase
 
# Importamos que necesitaremos para el programa
import simpy
import random
 

def proceso(env, tiempro, NombreEtapa, RAM, Cantidad_Ram, Numero_de_Instru, velocidad):
 
    # Variables que sirven para calcular y guardar la cantidad de tiempo que llevo cada proceso
    global tiempo_tot
    global tiempo
 
    #-------------------------------------- NEW --------------------------------------
    # El proceso llega al sistema operativo en donde dicho proceso debe esperar que se le asigne memoria RAM
    yield env.timeout(tiempro)
    print('%s. Solicita %d de RAM (New)' % ( NombreEtapa, Cantidad_Ram))
    # Se guarda el tiempo en el que llego el proceso
    tiempo_de_llegada = env.now
    
    #-------------------------------------- READY ------------------------------------
    # Con esto se solicita la RAM que se quiere utilizar 
    yield RAM.get(Cantidad_Ram)
    print('%s. Solicitud aceptada por %d de RAM (Admited)' % ( NombreEtapa, Cantidad_Ram))
 
    # Con esta variable almacenaremos el numero de instrucciones que se hayan finalizado
    Instruccion_Final = 0
    
    while Instruccion_Final < Numero_de_Instru:
        # Conexion con el resocurce CPU
        with cpu.request() as req:
            yield req
            # Instruccion a realizarse
            if (Numero_de_Instru - Instruccion_Final) >= velocidad:
                efec = velocidad
            else:
                efec = (Numero_de_Instru - Instruccion_Final)
 
            print('%s. CPU ejecutara %d instrucciones. (Ready)' % (NombreEtapa, efec))
            # Tiempo de instrucciones que se van a ejecutar
            yield env.timeout(efec/velocidad)   
 
            # Numero total de intrucciones terminadas
            Instruccion_Final += efec
            print('%s. CPU (%d/%d) completado. (Running)' % ( NombreEtapa, Instruccion_Final, Numero_de_Instru))
 
        # Si la decision es 1 wait, si es 2 procedemos a ready
        desicion = random.randint(1,2)
 
        if desicion == 1 and Instruccion_Final < Numero_de_Instru:
            #---------------------------------- WAITING -------------------------------
            with wait.request() as req2:
                yield req2
                yield env.timeout(1)                
                print('%s. Realizadas operaciones de entrada/salida. (Waiting)' % ( NombreEtapa))
    
 
    #------------------------------------ TERMINATED ----------------------------------
    # Cantidad de RAM que se retorna al sistema operativo 
    yield RAM.put(Cantidad_Ram)
    print('%s. Retorna %d de RAM. (Terminated)' % (NombreEtapa, Cantidad_Ram))
    # Total de tiempo que llevo a todo el proceso ejecutarse
    tiempo_tot += (env.now - tiempo_de_llegada)
    # Guardamos ese tiempo en un Array
    tiempo.append(env.now - tiempo_de_llegada) 
 
 
#-----------------------------------DEFINICION DE VARIABLES---------------------------------

velocidad = 6.0        # Velocidad que poseera el Procesador
Memoria_RAM = 100      # Cantidad de Memoria RAM que solicite el usuario
Numero_Pro = 200       # Numero de procesos a Realizar
tiempo_tot = 0.0       # Variable para el tiempo total que tardará un proceso
tiempo=[]              # Array de los tiempos en los que se ejecutaron
 
 
#------------------------------------SIMULACION---------------------------------

env = simpy.Environment()
# Cola de tipo Resource para el CPU 
cpu = simpy.Resource (env, capacity=1)
# Cola de tipo Container para la RAM
RAM = simpy.Container(env, init = Memoria_RAM, capacity = Memoria_RAM)
# Cola de tipo Resource Wait para operaciones I/O
wait = simpy.Resource (env, capacity=2) 
 
# Semilla del random
n_intervalo = 10 # Numero de intervalos
random.seed(5555)


# Creacion de los procesos a utilizar
for i in range(Numero_Pro):
    tiempro = random.expovariate(1.0 / n_intervalo)
    #Se encarga de generar un numero de instrucciones aleatorio
    Numero_de_Instru = random.randint(1,10)
    #Se encarga de generar una cantidad de memoria RAM aleatoria
    Cantidad_Ram = random.randint(1,10) 
    env.process(proceso(env, tiempro, 'Proceso %d' % i, RAM, Cantidad_Ram, Numero_de_Instru, velocidad))
 
# Se corre la simulacion
env.run()

print
# Se calcula el tiempo promedio total obtenido de los procesos
prom = (tiempo_tot/Numero_Pro)
# Imprime el resultado del promedio total obtenido de todos los procesos realizados
print ("El tiempo promedio de los procesos realizados es: ",prom," segundos")
 

print()
# Se calcula la desviación estandar de los tiempos 
suma = 0
for i in tiempo:
    suma += (i - prom)**2
 
desviacion = (suma/(Numero_Pro-1))**0.5
# Imprime el resultado obtenido de la desviacion estandar entre los tiempos
print ("La desviacion estandar obtenida de los tiempos es: ",desviacion," segundos")
