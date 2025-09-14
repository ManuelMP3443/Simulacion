import random
import math
import numpy as np
class FuncionDensidad: 

    def binomial(self,theta, num_ensayos, cantidad_muestras):
        resultado_lista =[]
        resultado_dic = {}
        

        for _ in range(cantidad_muestras):
            exitos = 0
            for _ in range(num_ensayos):
                if random.random() < theta:
                    exitos += 1
                    
            resultado_lista.append(exitos)
            if exitos in resultado_dic:
                resultado_dic[exitos] += 1
            else:
                resultado_dic[exitos] = 1
        return resultado_dic, resultado_lista
    
    def binomial_puntual(self,theta, cantidad_muestras):
        dic,lista = self.binomial(theta, 1,cantidad_muestras)

        dic.setdefault(1, 0) 
        dic.setdefault(0, 0)

        return dic, lista
    
    def exponencial(self, numero_muestras, lmbda):
        resultado_lista = []
        resultado_dic = {}
        for _ in range(numero_muestras):
            u = random.random()
            x = -np.log(u)/lmbda
            resultado_lista.append(x)
            key = round(x, 6)
            resultado_dic[key] = resultado_dic.get(key, 0) + 1

        return resultado_dic, resultado_lista
    
    def normal(self, numero_muestras, sigma, mu):
        resultado_lista = []
        resultado_dic = {}
        for _ in range(numero_muestras):
            u1 = random.random()
            u2 = random.random()

            z = np.sqrt(-2 * np.log(u1)) * np.cos(2*np.pi*u2)
            x = mu + sigma * z

            resultado_lista.append(x)
            key = round(x, 6)
            resultado_dic[key] = resultado_dic.get(key, 0) + 1

        return resultado_dic, resultado_lista

    def multinomial(self, probabilidades, numero_muestras, n_lanzamientos):
        """
        Devuelve una lista de vectores de conteos para cada muestra
        usando el método clásico de muestreo acumulativo.
        """
        total = sum(probabilidades)
        probabilidades = [p/total for p in probabilidades]
        k = len(probabilidades)
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

    def gibbs_bivariante(self, rho, N, x0, y0):
        rng = np.random.default_rng(123)  
        x, y = np.zeros(N), np.zeros(N)   
        x[0], y[0] = x0, y0               
        sigma = np.sqrt(1 - rho**2)       

        # Bucle de Gibbs
        for t in range(1, N):
            
            x[t] = rng.normal(rho * y[t-1], sigma)
            
            y[t] = rng.normal(rho * x[t], sigma)

        return x, y

