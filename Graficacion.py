from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Graficar:

    def __init__(self, fig, canvas):
         self.fig = fig
         self.canvas = canvas

    def histograma(self, dist, datos):
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        if dist == "Binomial":
            maxi = max(datos.values())    
            umbral = maxi *0.1
            datos_filtrados = {k: v for k, v in datos.items() if v >= umbral}  
            datos = dict(sorted(datos_filtrados.items()))

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

    def graficar3d(self, dist, trayectoria, modo="panoramica", filtro=None):
        categorias = sorted(set(trayectoria))
        cat_idx = {c: i for i, c in enumerate(categorias)}
    
        xs, ys, zs = [], [], []
        for i, cat in enumerate(trayectoria):
            xs.append(i)
            ys.append(cat_idx[cat])
            zs.append(1)
            self.fig.clf()

        ax3d = self.fig.add_subplot(111, projection="3d")
        ax3d.bar3d(xs, ys, [0]*len(xs), 1, 0.5, zs, shade=True)
    
        ax3d.set_xlabel("Ensayo")
        ax3d.set_ylabel("Categoría")
        ax3d.set_zlabel("Conteo")
        ax3d.set_yticks(list(cat_idx.values()))
        ax3d.set_yticklabels(categorias)
        ax3d.set_title(f"Distribución: {dist} (3D)", fontsize=14, fontweight='bold')
        self.canvas.draw()

    def multinomial(self,trayectoria, n_lanzamientos, dist, k):
        ax = self.fig.add_subplot(111)

        ax.clear()
        for i in range(k):
            ax.hist(trayectoria[:, i], bins=range(n_lanzamientos+2), alpha=0.5, label=f"x{i}")
        ax.set_xlabel("Conteo en la muestra")
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Distribución marginal {dist}")
        ax.legend()
        self.canvas.draw()

    



