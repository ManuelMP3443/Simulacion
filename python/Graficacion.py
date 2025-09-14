from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np

class Graficar:

    def __init__(self, fig, canvas):
         self.fig = fig
         self.canvas = canvas

    def histograma(self, dist, datos):
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        if dist == "Binomial":
            ax.set_ylim(0, max(datos.values()) * 1.1)  # 10% extra arriba
            ax.set_xlim(min(datos.keys())-0.5, max(datos.keys())+0.5)
            
        elif dist == "Binomial Puntual":
            cantidad_muestras = sum(datos.values())
            ax.set_ylim(0, (cantidad_muestras* (1.2)) + 0.5) 
            ax.set_xlim(min(datos.keys())-0.5, max(datos.keys())+0.5)

        # otros casos ...
        ax.bar(datos.keys(), datos.values(),color=['#F26B38', '#2E86AB', '#3CAEA3']*10)
        ax.set_title(f"Distribución: {dist}", fontsize=14, fontweight='bold')

        ax.set_title(f"Histograma {dist}")
        self.canvas.draw()

    def exponencial(self, dist, datos):
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        lista_datos_filtrada = [x for x in datos if x > 0]
        ax.hist(lista_datos_filtrada, bins=50, color='#F26B38', edgecolor='black', rwidth=0.8)

        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")

        # Títulos
        ax.set_title(f"Histograma {dist}", fontsize=14, fontweight='bold')
        self.canvas.draw()

    def normal(self, dist,  datos):
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        datos_para_hist = []
        for valor, freq in datos.items():
            datos_para_hist.extend([valor]*freq)


        ax.hist(datos_para_hist, bins=50, color='#F26B38', edgecolor='black', rwidth=0.8)
        ax.set_ylim(0, max(np.histogram(datos_para_hist, bins=50)[0]) * 1.3)




        # Ajustar etiquetas y título
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Histograma {dist}", fontsize=14, fontweight='bold')


        self.canvas.draw()



    
    def graficar_multinomial(self, datos, n_lanzamientos, index_prob):
        self.fig.clf()  # Limpiar la figura existente

        # Subplot principal
        ax_main = self.fig.add_subplot(111)
        ax_main.hist(datos[:, index_prob], bins=n_lanzamientos, color='#556270' , rwidth = 0.8,alpha=0.7, label=f"x{index_prob}")
        ax_main.set_title(f"Distribución x{index_prob}")
        ax_main.set_xlabel("Valores")
        ax_main.set_ylabel("Frecuencia")
        ax_main.legend()

        self.canvas.draw()

    def gibbs_bivariante_3D(self, x, y, bins=50):
       """
       x, y: arrays con las muestras del método de Gibbs
       bins: cantidad de intervalos en cada eje
       """
       self.fig.clf()  # Limpiar figura
       ax = self.fig.add_subplot(111, projection='3d')
       # Creamos el histograma 2D normalizado para densidad
       H, xedges, yedges = np.histogram2d(x, y, bins=bins, density=True)
       # Creamos la malla de coordenadas
       X, Y = np.meshgrid(xedges[:-1], yedges[:-1])
       Z = H.T  # transponemos para que coincida con X,Y
       # Graficamos la superficie
       ax.plot_surface(X, Y, Z, cmap='viridis')
       # Etiquetas
       ax.set_xlabel("X")
       ax.set_ylabel("Y")
       ax.set_zlabel("Densidad")
       ax.set_title("Muestreo Gibbs - Normal Bivariante")
       self.canvas.draw()    

    def gibbs_bivariante_2D(self, x, y, bins=50):
        """
        Grafica histograma 2D (heatmap) de muestras de Gibbs
        """
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        # Histograma 2D
        h = ax.hist2d(x, y, bins=bins, cmap='viridis', density=True)

        # Colorbar para indicar densidad
        self.fig.colorbar(h[3], ax=ax)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Histograma 2D - Muestreo Gibbs")

        self.canvas.draw()






    



