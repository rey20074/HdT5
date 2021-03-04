import simpy
import random

def proceso(proceso,env,timeprocess,CPU,RAM)

    #cola memoria,cola para cpu

    # Simular que esta realizando un proceso
    yield env.timeout(timeprocess)

# ----------------------

env = simpy.Environment() #ambiente de simulación
CPU = simpy.Resource(env,capacity = 1) # Fijar el procesador
random.seed(10) # fijar el inicio de random

RAM = simpy.Container(env, init=100, capacity=100) #fijar la RAM



totalDia = 0
for i in range(25):
    env.process(proceso('proceso %d'%i,env,random.expovariate(1.0/10),CPU))

env.run(until=50)  #correr la simulación hasta el tiempo = 50

print ("Tiempo promedio en el proceso es: ", totalDia/25.0)