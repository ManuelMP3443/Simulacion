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

        self.lib.gibbs_sample.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
        self.lib.gibbs_sample.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

        self.lib.normal_bivariada.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
        self.lib.normal_bivariada.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

        self.lib.triangulo.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        self.lib.triangulo.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

        self.lib.lineal.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        self.lib.lineal.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

        self.lib.free_vector_int.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.lib.free_vector_int.restype = None
        
        self.lib.free_vector_double.argtypes = [ctypes.POINTER(ctypes.c_double)]
        self.lib.free_vector_double.restype = None

        self.lib.free_matriz_int.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_int]
        self.lib.free_matriz_int.restype = None

        self.lib.free_matriz_double.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
        self.lib.free_matriz_double.restype = None

        


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

    def gibbs_sample(self, fxy, punto_inicial, numero_muestras, intervalos, n_intentos=500, n_prelim=3000):
        # convertir la función a cadena C
        fxy_c = ctypes.c_char_p(fxy.encode("utf-8"))

        # preparar el punto inicial
        n1 = len(punto_inicial)
        arrpunto = (ctypes.c_double * n1)(*punto_inicial)

        # preparar los intervalos
        n2 = len(intervalos)
        arrintervalo = (ctypes.c_double * n2)(*intervalos)

        # llamada a la librería (OJO: orden correcto de los enteros)
        resultado_ptr = self.lib.gibbs_sample(
            fxy_c,
            arrpunto,
            numero_muestras,
            arrintervalo,
            n_intentos,
            n_prelim
        )

        resultados = []
        for i in range(numero_muestras):
            # asumiendo que hay 2 columnas (x,y)
            vector = [resultado_ptr[i][j] for j in range(2)]
            print(f"{vector}\n")
            resultados.append(vector)

        # liberar memoria
        self.lib.free_matriz_double(resultado_ptr, numero_muestras)

        return resultados
    
    def normal_bivariada(self, cantidad_muestras, media, desviacion, covarianza):
        mu_x, mu_y = media
        sigma_x, sigma_y = desviacion
        rho = covarianza / (sigma_x * sigma_y)

        # Preparar punto inicial como arreglo C
        punto_inicial = (ctypes.c_double * 2)(mu_x, mu_y)

        # Llamar a la función C
        resultado_ptr = self.lib.normal_bivariada(
            punto_inicial,
            cantidad_muestras,
            sigma_x,
            sigma_y,
            mu_x,
            mu_y,
            rho
        )

        # Convertir a numpy array
        arr = np.zeros((cantidad_muestras + 1, 2))
        for i in range(cantidad_muestras + 1):
            arr[i][0] = resultado_ptr[i][0]
            arr[i][1] = resultado_ptr[i][1]

        # Preparar cadena de parámetros para mostrar
        parametros = (
            f"\u03bc_x: {mu_x} \u03bc_y: {mu_y} "
            f"\u03c3_x: {sigma_x} \u03c3_y: {sigma_y} "
            f"\u03c3_xy: {covarianza} \u03c1: {rho}"
        )

        self.lib.free_matriz_double(resultado_ptr, cantidad_muestras)

        return arr, parametros
    
    def triangulo(self, cantidad_muestras,punto_inicial):

        punto_inicial_c = (ctypes.c_double * 2)(punto_inicial[0], punto_inicial[1])

        # Llamar a la función C
        resultado_ptr = self.lib.triangulo(
            punto_inicial_c,
            cantidad_muestras
        )

        arr = np.zeros((cantidad_muestras + 1, 2))
        for i in range(cantidad_muestras + 1):
            arr[i][0] = resultado_ptr[i][0]
            arr[i][1] = resultado_ptr[i][1]

        self.lib.free_matriz_double(resultado_ptr, cantidad_muestras)

        return arr
    
    def lineal(self, cantidad_muestras,punto_inicial):

        punto_inicial_c = (ctypes.c_double * 2)(punto_inicial[0], punto_inicial[1])

        # Llamar a la función C
        resultado_ptr = self.lib.lineal(
            punto_inicial_c,
            cantidad_muestras
        )

        arr = np.zeros((cantidad_muestras + 1, 2))
        for i in range(cantidad_muestras + 1):
            arr[i][0] = resultado_ptr[i][0]
            arr[i][1] = resultado_ptr[i][1]

        self.lib.free_matriz_double(resultado_ptr, cantidad_muestras)

        return arr



