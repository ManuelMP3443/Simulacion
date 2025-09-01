import random
import math

class FuncionDensidad: 

    def binomial(self,theta, num_ensayos, cantidad_muestras):
        resultado = {}

        for _ in range(cantidad_muestras):
            exitos = 0
            for _ in range(num_ensayos):
                if random.random() < theta:
                    exitos += 1
            # Solo incrementar la clave si existe, o crearla si no
            if exitos in resultado:
                resultado[exitos] += 1
            else:
                resultado[exitos] = 1
        return resultado
    
    def binomial_puntual(self,theta, cantidad_muestras):
        resultado = self.binomial(theta, 1,cantidad_muestras)

        resultado.setdefault(1, 0) 
        resultado.setdefault(0, 0)

        return {1: resultado[1], 0:  resultado[0]}
    
    def multinomial_exponencial(self, probabilidades, numero_muestras, n_lanzamientos):
        """
        Devuelve una lista de vectores de conteos para cada muestra
        usando el método de tiempos exponenciales.
        """
        k = len(probabilidades)
        categorias = [f"x{i}" for i in range(k)]
        resultados = []

        for _ in range(numero_muestras):
            vector = [0]*k
            for _ in range(n_lanzamientos):
                tiempos = []
                for p in probabilidades:
                    u = random.random()
                    t = -math.log(1 - u) / p
                    tiempos.append(t)
                indice = tiempos.index(min(tiempos))
                vector[indice] += 1
            resultados.append(vector)

        return resultados

    def multinomial(self, probabilidades, numero_muestras, n_lanzamientos):
        """
        Devuelve una lista de vectores de conteos para cada muestra
        usando el método clásico de muestreo acumulativo.
        """
        total = sum(probabilidades)
        probabilidades = [p/total for p in probabilidades]
        k = len(probabilidades)
        categorias = [f"x{i}" for i in range(k)]
        resultados = []

        for _ in range(numero_muestras):
            vector = [0]*k
            for _ in range(n_lanzamientos):
                r = random.random()
                acum = 0.0
                for i, p in enumerate(probabilidades):
                    acum += p
                    if r < acum or i == k-1:
                        vector[i] += 1
                        break
            resultados.append(vector)

        return resultados

        return trayectoria        
