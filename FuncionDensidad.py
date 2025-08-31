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
    
    def multinomial_exponencial(self,probabilidades, numero_muestras):

        categorias = [f"x{i}" for i in range(len(probabilidades))]
        trayectoria = []

        for _ in range(numero_muestras):
            tiempos = []
            for p in probabilidades:
                
                u = random.random()
                t = -math.log(1 - u) / p
                tiempos.append(t)
            
            indice = tiempos.index(min(tiempos))
            trayectoria.append(categorias[indice])

        return trayectoria
    
    def multinomial(self, probabilidades,numero_muestras):
        categorias = [f"x{i}" for i in range(len(probabilidades))]
        trayectoria = []

        total = sum(probabilidades)
        probabilidades = [p/total for p in probabilidades]

        for _ in range(numero_muestras):
            r= random.random()
            acum =0.0 
            for i, p in enumerate(probabilidades):
                acum += p
                if r < acum or i == len(probabilidades)-1:
                    trayectoria.append(categorias[i])
                    break

        return trayectoria        
