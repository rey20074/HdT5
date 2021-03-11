import simpy
import random

def proceso(proceso,env,timeprocess,CPU,RAM,cap,redIns,instruc):
    
    global Ttotal
    global Promedio
    
    #se regresa la capacidad de la memoria
    yield RAM.get(cap)

    while instruc > 0:
        with CPU.request() as req:
            yield req
            yield env.timeout(1)
            instruc = instruc- redIns

            aleatorio = random.randint(1,2)

            if(aleatorio == 1):
                print('El proceso %s fue enviado a la cola %s segundos. Se están ocupando %s unidades de memoria. El tiempo actual es de: %s segundos\n' % (proceso, timeprocess, cap,env.now))
                yield env.timeout(timeprocess)

            else:
                print('El proceso %s está enviando a procesar %s instrucciones mas. Se están ocupando %s unidades de memoria. El tiempo actual es de: %s segundos\n' % (proceso, redIns, cap, env.now))
    print('El proceso %s ha finalizado con exito luego de haber empezado los procesos hace: %s segundos \n' % (proceso, env.now))
    RAM.put(cap)
    Ttotal = env.now
    Promedio=timeprocess
# ----------------------

env = simpy.Environment() #ambiente de simulación
CPU = simpy.Resource(env,capacity = 1) # Fijar el procesador
random.seed(10) # fijar el inicio de random

RAM = simpy.Container(env, init=100, capacity=100) #fijar la RAM

Ttotal = 0

for i in range(20):
    env.process(proceso(i+1,env,random.randint(1,10),CPU,RAM,random.randint(20,40),3,3))

env.run(until=200)  #correr la simulación hasta el tiempo = 50

print("El tiempo total de los procesos fue de %s"%Ttotal)
