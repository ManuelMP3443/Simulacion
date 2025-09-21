from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from scipy.stats import gaussian_kde


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
   

    def gibbs_bivariante_2D(self, x, y):
        self.fig.clf()

        # --- Scatter 2D ---
        ax2d = self.fig.add_subplot(121)
        ax2d.scatter(x, y, s=10, c='black', alpha=0.6)
        ax2d.grid(True, linestyle='--', color='gray', alpha=0.5)
        ax2d.set_xticks(np.linspace(min(x), max(x), 10))
        ax2d.set_yticks(np.linspace(min(y), max(y), 10))
        ax2d.set_xlabel("X")
        ax2d.set_ylabel("Y")
        ax2d.set_title("Muestras Gibbs 2D")

        # --- Superficie 3D tipo ola ---
        ax3d = self.fig.add_subplot(122, projection='3d')

        # Crear malla más pequeña para velocidad
        X, Y = np.meshgrid(np.linspace(min(x), max(x), 30),
                           np.linspace(min(y), max(y), 30))

        # KDE 2D para densidad suave
        values = np.vstack([x, y])
        kernel = gaussian_kde(values)
        Z = kernel(np.vstack([X.ravel(), Y.ravel()]))
        Z = Z.reshape(X.shape)

        # Graficar superficie
        surf = ax3d.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none',
                                 rstride=2, cstride=2, alpha=0.8)

        # Bloquear elevación vertical
        elev_fijo = 15
        azim_inicial = -60
        ax3d.view_init(elev=elev_fijo, azim=azim_inicial)

        # Deshabilitar que se cambie elevación al actualizar
        def fix_elev(event):
            ax3d.view_init(elev=elev_fijo, azim=ax3d.azim)

        self.canvas.mpl_connect('motion_notify_event', fix_elev)

        # Ejes y títulos
        ax3d.set_xlabel("X")
        ax3d.set_ylabel("Y")
        ax3d.set_zlabel("Densidad")
        ax3d.set_title("Densidad Gibbs 3D")

        self.canvas.draw()
    # Asumiendo que esta es una clase que tiene self.fig y self.canvas
    # y que recibe x, y, y el diccionario de parametros
    def normal_bivariada(self, x, y, parametros):
        self.fig.clf()
    
        # --- Gráfico de Dispersión 2D ---
        # ... (tu código para el gráfico 2D va aquí, sin cambios) ...
        ax2d = self.fig.add_subplot(121)
        ax2d.scatter(x, y, s=10, c='black', alpha=0.6)
        # ... (otros parámetros del gráfico 2D) ...
    
        # --- Histograma 3D de Frecuencia ---
        ax3d = self.fig.add_subplot(122, projection='3d')
        elevacion_fija = 20 # Define la elevación que quieres mantener
    
        # Crear el histograma 2D
        max_range = max(abs(np.array([x, y]).flatten()))
        hist, xedges, yedges = np.histogram2d(x, y, bins=30, range=[[-max_range, max_range], [-max_range, max_range]])
        X, Y = np.meshgrid(xedges[:-1] + (xedges[1]-xedges[0])/2,
                           yedges[:-1] + (yedges[1]-yedges[0])/2)
    
        # Graficar la superficie
        surf = ax3d.plot_surface(X, Y, hist.T, cmap='viridis', edgecolor='none')
        
        # Ejes y títulos
        ax3d.set_xlabel("X")
        ax3d.set_ylabel("Y")
        ax3d.set_zlabel("Frecuencia")
        ax3d.set_title(parametros)
    
        # Función que se ejecutará con el evento del mouse
        def on_move(event):
            if event.inaxes == ax3d:
                # Mantener la elevación fija y actualizar solo el acimut
                ax3d.view_init(elev=elevacion_fija, azim=ax3d.azim)
                self.canvas.draw_idle()
    
        # Conectar el evento de movimiento del mouse a nuestra función
        self.fig.canvas.mpl_connect('motion_notify_event', on_move)
    
        self.canvas.draw()





    



