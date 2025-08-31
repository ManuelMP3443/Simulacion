import FuncionDensidad as fd
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import re
import Graficacion
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Función de cierre seguro
def cerrar():
    root.quit()
    root.destroy()

def validar_entradaf(valor):
    dist = distribucion.get()

    if dist == "Multinomial" or dist == "Multinomial-exponencial":
        return True
    else: 
        if valor == "":
            return True
        
        try:
            numero = float(valor)
            if 0 <= numero <= 1:
                return True
            else: 
                return False
        except ValueError:
            return False    

def validar_entradai(valor):
    if valor == "":  
        return True
    try:
        int(valor)
        return True
    except ValueError:
        return False
    
def pasar_siguiente(event, siguiente_entry):
    siguiente_entry.focus_set()    


root = tb.Window(themename="cosmo")
root.title("Simulación de Distribuciones")
root.geometry("1000x600")

vcmdf = (root.register(validar_entradaf), '%P') 
vcmdi = (root.register(validar_entradai), '%P') 
 
# Panel izquierdo
panel_izq = tb.Frame(root, bootstyle=LIGHT, width=250, padding=15)
panel_izq.pack(side=LEFT, fill=Y, padx=5, pady=5)

tb.Label(panel_izq, text="Selección", font=("Arial", 16, "bold"), bootstyle=INFO).pack(fill=X, pady=(0,15))

# ComboBox distribución
tb.Label(panel_izq, text="Distribución:", font=("Arial", 12)).pack(pady=(5,2))
distribucion = tb.Combobox(panel_izq, values=["Binomial", "Binomial Puntual", "Multinomial", "Multinomial-exponencial"], bootstyle="info")
distribucion.pack(fill=X, pady=(0,5))
distribucion.current(0)

# Panel de parámetros dinámicos
frame_parametros = tb.Frame(panel_izq, bootstyle=LIGHT)
frame_parametros.pack(fill=X, pady=(10,5))

# Variables de entradas
param1_var = tk.StringVar()
param2_var = tk.StringVar()
param3_var = tk.StringVar()

# Widgets de parámetros
label1 = tb.Label(frame_parametros, text="Parámetro 1:", font=("Arial",12))
entry1 = tb.Entry(frame_parametros, textvariable=param1_var, bootstyle="info")
entry1.configure(validate="key", validatecommand=vcmdf)

label2 = tb.Label(frame_parametros, text="Parámetro 2:", font=("Arial",12))
entry2 = tb.Entry(frame_parametros, textvariable=param2_var, bootstyle="info")
entry2.configure(validate="key", validatecommand=vcmdi)

label3 = tb.Label(frame_parametros, text="Parámetro 3:", font=("Arial",12))
entry3 = tb.Entry(frame_parametros, textvariable=param3_var, bootstyle="info")
entry3.configure(validate="key", validatecommand=vcmdi)

entry1.bind("<Return>", lambda e: pasar_siguiente(e, entry2))
entry2.bind("<Return>", lambda e: graficar())
entry3.bind("<Return>", lambda e: graficar())

# Inicializar la grafica
fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill="both", expand=True) 

# Crear instancia de Graficar
graficador = Graficacion.Graficar(fig, canvas)

# Función para actualizar parámetros visibles según distribución
def actualizar_parametros(event=None):
    for widget in frame_parametros.winfo_children():
        widget.pack_forget()

    dist = distribucion.get()
    # Reconfigurar bindings de entry2 según distribución
    entry2.unbind("<Return>")
    if dist == "Binomial":
        entry2.bind("<Return>", lambda e: pasar_siguiente(e, entry3))    
    else:
        entry2.bind("<Return>", lambda e: graficar())
        
    if dist == "Binomial":
        label1.config(text="Theta (prob. éxito):")
        label2.config(text="Número de ensayos:")
        label3.config(text="Cantidad de muestras:")
        label1.pack(pady=(5,2)); entry1.pack(fill=X,pady=(0,5))
        label2.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))
        label3.pack(pady=(5,2)); entry3.pack(fill=X,pady=(0,5))
    elif dist == "Binomial Puntual":
        label1.config(text="Theta (prob. éxito):")
        label2.config(text="Cantidad de muestras:")
        label1.pack(pady=(5,2)); entry1.pack(fill=X,pady=(0,5))
        label2.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))
    elif dist == "Multinomial":
        label1.config(text="Probabilidades (separadas por ,):")
        label2.config(text="Cantidad de muestras:")
        label1.pack(pady=(5,2)); entry1.pack(fill=X,pady=(0,5))
        label2.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))
    elif dist == "Multinomial-exponencial":
        label1.config(text="Probabilidades (separadas por ,):")
        label2.config(text="Cantidad de muestras:")
        label1.pack(pady=(5,2)); entry1.pack(fill=X,pady=(0,5))
        label2.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))     

distribucion.bind("<<ComboboxSelected>>", actualizar_parametros)
actualizar_parametros()

# Panel derecho para gráfica
frame_grafica = tb.Frame(root, bootstyle=LIGHT)
frame_grafica.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

# Función de graficado
def graficar():
    fund = fd.FuncionDensidad()
    dist = distribucion.get()

    # Limpiar frame_grafica de widgets antiguos
    for w in frame_grafica.winfo_children():
        if isinstance(w, tk.Scale):
            w.destroy()

    # Leer parámetros
    p1 = param1_var.get()
    p2 = param2_var.get()
    p3 = param3_var.get()

    if dist == "Binomial":
        theta = float(p1)
        num_ensayos = int(p2)
        cantidad_muestras = int(p3)
        datos = fund.binomial(theta, num_ensayos, cantidad_muestras)
        graficador.histograma(dist, datos)

    elif dist == "Binomial Puntual":
        theta = float(p1)
        cantidad_muestras = int(p2)
        datos = fund.binomial_puntual(theta, cantidad_muestras)
        graficador.histograma(dist, datos)

    elif dist in ["Multinomial", "Multinomial-exponencial"]:
        
       

        tokens = re.split(r"[ ,]+", p1.strip())
        probabilidades = [float(t) for t in tokens if t]
        cantidad_muestras = int(p2) if p2 else 1000

        if dist == "Multinomial":
            trayectoria = fund.multinomial(probabilidades, cantidad_muestras)
        else:
            trayectoria = fund.multinomial_exponencial(probabilidades, cantidad_muestras)

        graficador.graficar3d(dist, trayectoria)

        # Crear slider después del canvas
        muestra_slider = tk.Scale(frame_grafica,
                                  from_=1,
                                  to=len(trayectoria),
                                  orient='horizontal',
                                  label="Muestra",
                                  command=lambda v: graficador.graficar_muestra(trayectoria, int(v)-1))
        muestra_slider.pack(fill=X, pady=10)
            
# Botón Graficar
boton = tb.Button(panel_izq, text="Graficar", bootstyle=(PRIMARY, OUTLINE), command=graficar)
boton.pack(pady=20, fill=X)

# Cierre seguro
root.protocol("WM_DELETE_WINDOW", cerrar)
root.mainloop()
