from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde


# Paleta de colores uniforme
PALETA = {
    "binomial": ["#1f77b4", "#ff7f0e"],   # Azul y naranja
    "normal": "#2ca02c",                   # Verde
    "exponencial": "#d62728",              # Rojo
    "multinomial": "#9467bd",              # Morado
    "gibbs_2d": "#17becf",                 # Cyan
    "normal_2d": "#bcbd22"                 # Amarillo-verde
}

class Graficar:
    def __init__(self, fig, canvas):
        self.fig = fig
        self.canvas = canvas
        self._callback_ids = {}
       

    def histograma(self, dist, datos):
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        if dist == "Binomial Puntual":
            x_vals = [0, 1]
            y_vals = [datos.get(0, 0), datos.get(1, 0)]
            ax.set_xlim(-0.5, 1.5)
            ax.set_ylim(0, max(y_vals) * 1.3)
            colores = PALETA["binomial"]
            ax.bar(x_vals, y_vals, color=colores, edgecolor='gray', alpha=0.8)
            ax.set_xticks(x_vals)
            ax.set_xticklabels(["Fracaso", "Éxito"], fontsize=12)
        else:
            ax.set_ylim(0, max(datos.values()) * 1.2)
            ax.set_xlim(min(datos.keys()) - 0.5, max(datos.keys()) + 0.5)
            colores = sns.color_palette("Set2", n_colors=len(datos))
            ax.bar(datos.keys(), datos.values(), color=colores, edgecolor='gray', alpha=0.8)

        ax.set_xlabel("Valores")
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Histograma {dist}", fontsize=14, fontweight='bold')
        ax.grid(True, linestyle='--', color='gray', alpha=0.3)
        self.canvas.draw()

    def exponencial(self, dist, datos):
        self.fig.clf()
        ax = self.fig.add_subplot(111)
        lista_datos = [x for x in datos if x > 0]
        ax.hist(lista_datos, bins=40, color=PALETA["exponencial"], edgecolor='black', alpha=0.8)
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Histograma {dist}", fontsize=14, fontweight='bold')
        self.canvas.draw()

    def normal(self, dist, datos):
        self.fig.clf()
        ax = self.fig.add_subplot(111)
        
        # "datos" ahora es tu arreglo NumPy directo, ya no es un diccionario.
        ax.hist(datos, bins=40, color=PALETA["normal"], edgecolor='black', alpha=0.8)
        
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Histograma {dist}", fontsize=14, fontweight='bold')
        self.canvas.draw()

    def graficar_multinomial(self, datos, n_lanzamientos, index_prob):
        self.fig.clf()
        ax = self.fig.add_subplot(111)
        ax.hist(datos[:, index_prob], bins=n_lanzamientos, color=PALETA["multinomial"], alpha=0.7, edgecolor='gray')
        ax.set_xlabel("Valores")
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Distribución x{index_prob}", fontsize=14, fontweight='bold')
        self.canvas.draw()

    def gibbs_bivariante_2D(self, x, y):
        
        
        LIMITE_PUNTOS = 50000 
        if len(x) > LIMITE_PUNTOS:
            x = x[-LIMITE_PUNTOS:]
            y = y[-LIMITE_PUNTOS:]
        

        self.fig.clf() # Limpia la figura anterior

        # --- Scatter 2D ---
        ax2d = self.fig.add_subplot(121)
        ax2d.scatter(x, y, s=15, color=sns.color_palette("Set2")[0], alpha=0.7)
        ax2d.set_xlabel("X")
        ax2d.set_ylabel("Y")
        ax2d.set_title("Muestras 2D")
        ax2d.grid(True, linestyle='--', alpha=0.5)

        # --- Superficie 3D (Histograma) ---
        ax3d = self.fig.add_subplot(122, projection='3d')

        try:
            # (El cálculo del histograma ahora usa los datos limitados)
            bins_x = int(np.max(x) - np.min(x)) + 1 if len(np.unique(x)) > 1 else 1
            bins_y = int(np.max(y) - np.min(y)) + 1 if len(np.unique(y)) > 1 else 1
            bins_x = min(bins_x, 50)
            bins_y = min(bins_y, 50)

            hist, xedges, yedges = np.histogram2d(x, y, bins=(bins_x, bins_y))

            X, Y = np.meshgrid(xedges[:-1] + (xedges[1]-xedges[0])/2,
                               yedges[:-1] + (yedges[1]-yedges[0])/2)

            ax3d.plot_surface(X, Y, hist.T, cmap='coolwarm', edgecolor='none', rstride=1, cstride=1)
            
            ax3d.set_xlabel("X")
            ax3d.set_ylabel("Y")
            ax3d.set_zlabel("Frecuencia")
            ax3d.set_title("Histograma 3D")

        except Exception as e:
            print(f"Error al generar histograma 3D: {e}")
            ax3d.set_title("Error en Histograma 3D")
            ax3d.set_xlabel("X")
            ax3d.set_ylabel("Y")
            ax3d.set_zlabel("Error")

        # --- Manejo de Callback de Rotación (Sin cambios) ---
        callback_id = self._callback_ids.get(ax3d)
        if callback_id:
            self.canvas.mpl_disconnect(callback_id)

        elev_fija = 25
        ax3d.view_init(elev=elev_fija, azim=-60)

        def bloquear_elev(event):
            if event.inaxes == ax3d:
                ax3d.view_init(elev=elev_fija, azim=ax3d.azim)
                self.canvas.draw_idle()

        new_callback_id = self.canvas.mpl_connect('motion_notify_event', bloquear_elev)
        self._callback_ids[ax3d] = new_callback_id
        
        self.canvas.draw()


    def normal_bivariada(self, x, y, parametros="Normal Bivariada"):
        
        
        LIMITE_PUNTOS = 50000 
        if len(x) > LIMITE_PUNTOS:
            x = x[-LIMITE_PUNTOS:]
            y = y[-LIMITE_PUNTOS:]
       

        self.fig.clf()
        # Scatter 2D
        ax2d = self.fig.add_subplot(121)
        ax2d.scatter(x, y, s=15, color=sns.color_palette("Set2")[1], alpha=0.7)
        ax2d.set_xlabel("X")
        ax2d.set_ylabel("Y")
        ax2d.set_title("Normal Bivariada 2D")
        ax2d.grid(True, linestyle='--', alpha=0.5)
    
        # Superficie 3D
        ax3d = self.fig.add_subplot(122, projection='3d')
        # (El cálculo del histograma ahora usa los datos limitados)
        hist, xedges, yedges = np.histogram2d(x, y, bins=25) 
        X, Y = np.meshgrid(xedges[:-1] + (xedges[1]-xedges[0])/2,
                           yedges[:-1] + (yedges[1]-yedges[0])/2)
        ax3d.plot_surface(X, Y, hist.T, cmap='coolwarm', edgecolor='none', rstride=2, cstride=2)
        ax3d.set_xlabel("X")
        ax3d.set_ylabel("Y")
        ax3d.set_zlabel("Frecuencia")
        ax3d.set_title(parametros)
    
        # Fijar elevación
        elev_fija = 25
        ax3d.view_init(elev=elev_fija, azim=-60)
    
        # --- CÓDIGO DE CALLBACK CORREGIDO (para evitar fugas) ---
        # Desconectar el callback anterior si existía
        callback_id = self._callback_ids.get(ax3d)
        if callback_id:
            self.canvas.mpl_disconnect(callback_id)

        # Mantener elevación fija (solo horizontal)
        def bloquear_elev(event):
            if event.inaxes == ax3d: # Añadido check
                ax3d.view_init(elev=elev_fija, azim=ax3d.azim)
                self.canvas.draw_idle()
        
        # Conectar el nuevo callback y guardar su ID
        new_callback_id = self.canvas.mpl_connect('motion_notify_event', bloquear_elev)
        self._callback_ids[ax3d] = new_callback_id
        # --- FIN DE CORRECCIÓN ---
        
        self.canvas.draw()
    

