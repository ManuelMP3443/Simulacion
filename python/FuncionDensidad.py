import numpy as np
import ctypes
import os


class FuncionDensidad: 

    def __init__(self):
        self.lib = ctypes.CDLL(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build", "FuncionDensidad.dll"))) 
        
        self.lib.binomial.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.c_int]
        self.lib.binomial.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

        self.lib.binomial_puntual.argtypes = [ctypes.c_double, ctypes.c_int]
        self.lib.binomial_puntual.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

        self.lib.exponencial.argtypes = [ctypes.c_int, ctypes.c_double ]
        self.lib.exponencial.restype = ctypes.POINTER(ctypes.c_double)

        self.lib.normal.argtypes = [ ctypes.c_int, ctypes.c_double, ctypes.c_double]
        self.lib.normal.restype = ctypes.POINTER(ctypes.c_double)

        self.lib.multinomial.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
        self.lib.multinomial.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

        self.lib.free_vector_int.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.lib.free_vector_int.restype = None
        
        self.lib.free_vector_double.argtypes = [ctypes.POINTER(ctypes.c_double)]
        self.lib.free_vector_double.restype = None

        self.lib.free_matriz_int.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_int]
        self.lib.free_matriz_int.restype = None


    def binomial(self, theta, num_ensayos, cantidad_muestras):
        resultado_ptr = self.lib.binomial(theta, num_ensayos, cantidad_muestras)
    
        # Convertir punteros C a listas de Python
        valores_ptr = resultado_ptr[0]
        frecuencia_ptr = resultado_ptr[1]
    
        resultado_lista = [valores_ptr[i] for i in range(cantidad_muestras)]
        resultado_dic = {i: frecuencia_ptr[i] for i in range(num_ensayos + 1) if frecuencia_ptr[i] > 0}
    
        # Liberar memoria
        self.lib.free_matriz_int(resultado_ptr, 2)
    
        return resultado_dic, resultado_lista

    
    def binomial_puntual(self,theta, cantidad_muestras):
        dic,lista = self.binomial(theta, 1,cantidad_muestras)

        dic.setdefault(1, 0) 
        dic.setdefault(0, 0)

        return dic, lista
    
    def exponencial(self, numero_muestras, lmbda):
        resultado_ptr = self.lib.exponencial(numero_muestras, lmbda)
        resultado_lista = [resultado_ptr[i] for i in range(numero_muestras) if np.isfinite(resultado_ptr[i])]
        resultado_dic = {}

        for x in resultado_lista:
            resultado_dic[x] = resultado_dic.get(x, 0) +1
       
        self.lib.free_vector_double(resultado_ptr)
        return resultado_dic, resultado_lista
    
    def normal(self, numero_muestras, sigma, mu):
        resultado_ptr = self.lib.normal(numero_muestras, sigma, mu)

        resultado_lista = [resultado_ptr[i] for i in range(numero_muestras) if np.isfinite(resultado_ptr[i])]
        resultado_dic = {}

        for x in resultado_lista:
            resultado_dic[x] = resultado_dic.get(x, 0) +1
       
        self.lib.free_vector_double(resultado_ptr)

        return resultado_dic, resultado_lista

    def multinomial(self, probabilidades, numero_muestras, n_lanzamientos):

        n = len(probabilidades)
        arr = (ctypes.c_double *(n+1))(*probabilidades, -1.0)

        resultado_ptr = self.lib.multinomial(arr, numero_muestras, n_lanzamientos)
        resultados = []

        for i in range(numero_muestras):
            vector = [resultado_ptr[i][j] for j in range(n)]
            resultados.append(vector)

        self.lib.free_matriz_int(resultado_ptr, numero_muestras)

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

