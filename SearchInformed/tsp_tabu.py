# TSP con búsqueda tabú
import math
import random

def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# calcula la distancia cubierta por una ruta
def evalua_ruta(ruta):
    total = 0
    for i in range(0, len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i+1]
        total = total + distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[i+1]
    ciudad2 = ruta[0]
    total = total + distancia(coord[ciudad1], coord[ciudad2])
    return total

def busqueda_tabu(ruta):
    mejor_ruta = ruta
    memoria_tabu = {}
    persistencia = 5
    mejora = False
    iteraciones = 100

    while iteraciones > 0:
        iteraciones = iteraciones - 1
        dist_actual = evalua_ruta(ruta)
        # evaluar vecinos
        mejora = False
        for i in range(0, len(ruta)):
            if mejora:
                break
            for j in range(0, len(ruta)):
                if i != j:
                    ruta_tmp = ruta[:]
                    ciudad_tmp = ruta_tmp[i]
                    ruta_tmp[i] = ruta_tmp[j]
                    ruta_tmp[j] = ciudad_tmp
                    dist = evalua_ruta(ruta_tmp)

                    # comprobar si el movimiento es taboo
                    tabu = False
                    if ruta_tmp[i] + "_" + ruta_tmp[j] in memoria_tabu:
                        if memoria_tabu[ruta_tmp[i] + "_" + ruta_tmp[j]] > 0:
                            tabu = True
                    
                    if dist < dist_actual and not tabu:
                        # encontrado vecino que mejora el resultado
                        ruta = ruta_tmp[:]
                        if evalua_ruta(ruta) < evalua_ruta(mejor_ruta):
                            mejor_ruta = ruta[:]
                        # almacenamos en memoria tabú
                        memoria_tabu[ruta_tmp[i] + "_" + ruta_tmp[j]] = persistencia
                        mejora = True
                        break
                    elif dist < dist_actual and tabu:
                        # comprobamos criterio de aspiracion 
                        # aunque sea movimiento tabú
                        if evalua_ruta(ruta_tmp) < evalua_ruta(mejor_ruta):
                            mejor_ruta = ruta_tmp[:]
                            ruta = ruta_tmp[:]
                            #almacenamos en memoria tabú
                            memoria_tabu[ruta_tmp[i] + "_" + ruta_tmp[j]] = persistencia
                            mejora = True
                            break
        # rebajar persistencia de los movimientos tabú
        if len(memoria_tabu) > 0:
            for k in memoria_tabu:
                memoria_tabu[k] = memoria_tabu[k]-1
    return mejor_ruta

if __name__ == "__main__":
    coord = {
        'Malaga': (36.43, -4.24),
        'Sevilla': (37.23, -5.59),
        'Granada': (37.11, -3.35),
        'Valencia': (39.28, -0.22),
        'Madrid': (40.24, -3.41),
        'Salamanca': (40.57, -5.40),
        'Santiago': (42.52, -8.33),
        'Santander': (43.28, -3.48),
        'Zaragoza': (41.39, -0.52),
        'Barcelona': (41.23, 2.11)
    }

    #crear ruta inicial aleatoria
    ruta = []
    for ciudad in coord:
        ruta.append(ciudad)
    random.shuffle(ruta)

    ruta = busqueda_tabu(ruta)
    print(ruta)
    print("Distancia total: " + str(evalua_ruta(ruta)))