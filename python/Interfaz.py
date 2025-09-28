import FuncionDensidad as fd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import re
import Graficacion
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import seaborn as sns



config_dist = {
    "Binomial": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 2, "bind_to": 1},
            {"text": "Número de ensayos:", "entry_idx": 1, "bind_to": 0},
            {"text": "Probabilidad (θ):", "entry_idx": 0, "bind_to": None},
        ]
    },
    "Binomial Puntual": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 0},
            {"text": "Probabilidad (θ):", "entry_idx": 0, "bind_to": None},
        ]
    },
    "Exponencial": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 6},
            {"text": "Lambda (λ):", "entry_idx": 6, "bind_to": None},
        ]
    },
    "Normal": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 4},
            {"text": "Media (μ):", "entry_idx": 4, "bind_to": 3},
            {"text": "Varianza (σ²):", "entry_idx": 3, "bind_to": None},
        ]
    },
    "Gibbs": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 5},
            {"text": "Función f(x,y):", "entry_idx": 5, "bind_to": 3},
            {"text": "(X0,Y0):", "entry_idx": 3, "bind_to": 4},
            {"text": "intervalos en x:", "entry_idx": 4, "bind_to": 6},
            {"text": "intervalos en y:", "entry_idx": 6, "bind_to": None}
        ]
    },
    "Normal Bivariada": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 3},
            {"text": "Media X, Y (μx, μy):", "entry_idx": 3, "bind_to": 4},
            {"text": "Desviación X, Y (σx, σy):", "entry_idx": 4, "bind_to": 6},
            {"text": "Covarianza (σxy):", "entry_idx": 6, "bind_to": None},
        ]
    },
    "Triangulo con Gibbs": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 3},
            {"text": "Punto inicial X, Y :", "entry_idx": 3, "bind_to": None},
        ]
    },
    "Lineal Bivariada": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 3},
            {"text": "Punto inicial X, Y :", "entry_idx": 3, "bind_to": None},
        ]
    },
    "Multinomial": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 2},
            {"text": "Número de ensayos:", "entry_idx": 2, "bind_to": 0},
            {"text": "Probabilidades (θ1, θ2...):", "entry_idx": 0, "bind_to": None},
        ]
    },
}

info_dist = {
    "Binomial": "Simula el número de éxitos en una secuencia de n ensayos de Bernoulli.\n\n"
                  "Fórmula de la función de masa de probabilidad (PMF):\n"
                  "             ( n ) \n"
                  "P(X=k) = ( k ) ⋅ θᵏ ⋅ (1 - θ)ⁿ⁻ᵏ\n\n"
                  "Parámetros:\n"
                  "- Theta (θ): La probabilidad de éxito en cada ensayo (0 < θ < 1).\n"
                  "- Número de ensayos (n).\n"
                  "- Cantidad de muestras: El número de veces que se repite la simulación.",
    
    "Binomial Puntual": "Genera una secuencia de éxitos o fracasos. También se conoce como la distribución de Bernoulli.\n\n"
                      "Fórmula de la función de masa de probabilidad (PMF):\n"
                      "P(X=k) = θᵏ ⋅ (1 - θ)¹⁻ᵏ\n\n"
                      "Parámetros:\n"
                      "- Theta (θ): La probabilidad de éxito (0 < θ < 1).\n"
                      "- Cantidad de muestras: El número de resultados a generar.",
    
    "Exponencial": "Describe la probabilidad de que un evento ocurra en un tiempo continuo entre dos puntos.\n\n"
                  "Fórmula de la función de densidad de probabilidad (PDF):\n"
                  "f(x; λ) = λ ⋅ e^(-λx)\n\n"
                  "Parámetros:\n"
                  "- Lambda (λ): La tasa de ocurrencia de los eventos (λ > 0).\n"
                  "- Cantidad de muestras: El número de tiempos entre eventos a simular.",
    
    "Normal": "Una de las distribuciones más importantes en estadística, con forma de campana.\n\n"
              "Fórmula de la función de densidad de probabilidad (PDF):\n"
              "             1      \n"
              "f(x) = ------ ⋅ exp( -(x-μ)² / (2 ⋅ σ²) )\n"
              "           σ√2π\n\n"
              "Parámetros:\n"
              "- Media (μ): El centro de la campana.\n"
              "- Varianza (σ²): La dispersión de los datos (σ² > 0).\n"
              "- Cantidad de muestras: El tamaño de la muestra a generar.",
    
    "Gibbs": "El método de Gibbs es un algoritmo de muestreo para aproximar distribuciones conjuntas. "
              "Se basa en muestrear secuencialmente de las distribuciones condicionales de cada variable dado el resto:\n"
              "  X | Y ~ P(X | Y=y)\n"
              "  Y | X ~ P(Y | X=x)\n\n"
              "Parámetros:\n"
              "- Función f(x,y): La expresión de la densidad conjunta.\n"
              "- Punto inicial (x₀, y₀): Valores iniciales para las variables.\n"
              "- Intervalos [a, b]: Rango de valores para cada variable (si aplica).\n"
              "- Cantidad de muestras: Número de puntos a generar mediante Gibbs.",
    
    "Normal Bivariada": "Describe la distribución conjunta de dos variables aleatorias normales.\n\n"
                      "Fórmula de la función de densidad de probabilidad (PDF):\n"
                      "                        1        \n"
                      "f(x,y) = ----------------- ⋅ exp( -1/2 ⋅ Q(x,y) )\n"
                      "          2⋅π⋅σₓ⋅σᵧ√1-ρ²\n\n"
                      "donde:\n\n"
                      "              1    \n"
                      "Q(x,y) = ----- ⋅ [ ( (x-μₓ)/σₓ )² - 2⋅ρ⋅(x-μₓ)/σₓ ⋅ (y-μᵧ)/σᵧ + ( (y-μᵧ)/σᵧ )² ]\n"
                      "             1-ρ²\n\n"
                      "Parámetros:\n"
                      "- Media X, Y (μₓ, μᵧ): El centro de la 'campana' 3D.\n"
                      "- Desviación X, Y (σₓ, σᵧ): La dispersión en cada eje.\n"
                      "- Covarianza (σₓᵧ): La relación entre las variables, que determina la inclinación de la campana.\n"
                      "- Cantidad de muestras: Número de puntos a generar.",
    
    "Triangulo con Gibbs": "Distribución bivariada triangular usando muestreo de Gibbs.\n\n"
                          "f(x,y) = 2 para x+y <= 1, x >= 0, y >= 0\n\n"
                          "Parámetros:\n"
                          "- Punto inicial (x₀, y₀): El primer valor de x e y.\n"
                          "- Cantidad de muestras: Número de puntos a generar mediante Gibbs.",
    
    "Lineal Bivariada": "Distribución bivariada lineal (por ejemplo, f(x,y) = (2x + 3y + 2)/28) en un dominio rectangular.\n\n"
                      "Parámetros:\n"
                      "- Punto inicial (x₀, y₀): El primer valor de x e y.\n"
                      "- Cantidad de muestras: Número de puntos a generar mediante muestreo condicional.",
    
    "Multinomial": "Generalización de la distribución binomial para más de dos resultados posibles.\n\n"
                  "Fórmula de la función de masa de probabilidad (PMF):\n"
                  "                   n!      \n"
                  "P(x) = --------------- ⋅ θ₁ⁿ¹ ⋅ ... ⋅ θₖⁿᵏ\n"
                  "             n₁! ⋅ ... ⋅ nₖ!    \n\n"
                  "Parámetros:\n"
                  "- Probabilidades (θ₁, θ₂, ...): Las probabilidades de cada uno de los k resultados, que deben sumar 1.\n"
                  "- Número de ensayos: El número total de resultados en cada intento.\n"
                  "- Cantidad de muestras: El número de intentos a simular."
}


# -------- Funciones de validación --------
def cerrar():
    root.quit()
    root.destroy()

def validar_entradaf(valor):
    dist = distribucion.get()
    if dist in ["Multinomial"]:
        return True
    if valor == "":
        return True
    try:
        numero = float(valor)
        return 0 <= numero <= 1
    except ValueError:
        return False

def validar_entradaif(valor):
    dist = distribucion.get()
    if dist in ["Normal Bivariada", "Gibbs", "Triangulo con Gibbs", "Lineal Bivariada"]:
        return True
    if valor == "" or valor == "-":
        return True
    try:
        float(valor)
        return True
    except ValueError:
        return False
  

def validar_entradai(valor):
    if valor == "":
        return True
    try:
        # Comprueba que el valor sea un entero Y que no sea negativo
        return int(valor) >= 0
    except ValueError:
        return False

def validar_funcion(valor):
    return bool(re.match(r'^[0-9a-zA-Z+\-*/^()., ]*$', valor))

def pasar_siguiente(event, siguiente_entry):
    siguiente_entry.focus_set()

# -------- Inicialización de ventana --------
root = tb.Window(themename="superhero")
root.title("Simulación de Distribuciones")

ancho= root.winfo_screenwidth()
alto = root.winfo_screenheight()

root.attributes('-fullscreen', True)

vcmdf = (root.register(validar_entradaf), '%P')
vcmdi = (root.register(validar_entradai), '%P')
vcmdif = (root.register(validar_entradaif), '%P')
vcmdfx = (root.register(validar_funcion), '%P')

# -------- Panel izquierdo --------
panel_izq = tb.Frame(root, width=250, padding=15) # <--- REMOVER BOOTSTYLE
panel_izq.pack(side=LEFT, fill=Y, padx=5, pady=5)

frame_central = tb.Frame(root)
frame_central.pack(fill=BOTH, expand=True)

# Frame de gráfica (mitad superior)
frame_grafica = tb.Frame(frame_central)
frame_grafica.pack(side=TOP, fill=BOTH, expand=False, padx=5, pady=5)
frame_grafica.pack_propagate(False)

# Frame de tabla (mitad inferior)
frame_tabla = tb.Frame(frame_central, padding=5)
frame_tabla.pack(side=BOTTOM, fill=BOTH, expand=False, padx=5, pady=5)
frame_tabla.pack_propagate(False)

frame_grafica.config(height=(alto/2)+alto*0.1)
frame_tabla.config(height=(alto/2)-alto*0.15)

tb.Label(panel_izq, text="Selección", font=("Helvetica", 16, "bold"), bootstyle="secondary",foreground="white").pack(fill=X, pady=(0,15)) # <--- CAMBIO DE FUENTE Y ESTILO

# Contenedor para la combobox y el botón de info
frame_selector = tb.Frame(panel_izq)
frame_selector.pack(fill=X, pady=(0,5))
distribucion = tb.Combobox(frame_selector, values=list(config_dist.keys()), bootstyle="secondary") # <--- CAMBIO DE ESTILO
distribucion.pack(side=LEFT, fill=X, expand=True)
distribucion.current(0)


# Botón de información
def mostrar_info():
    dist = distribucion.get()
    info = info_dist.get(dist, "Información no disponible.")

    ventana_info = tb.Toplevel(root)
    ventana_info.title(f"Información: {dist}")

    ancho = int(root.winfo_screenwidth() * 0.4)
    alto = int(root.winfo_screenheight() * 0.4)
    ventana_info.geometry(f"{ancho}x{alto}")
    ventana_info.resizable(True, True)

    # Frame principal
    frame = tb.Frame(ventana_info, padding=10)
    frame.pack(fill=BOTH, expand=True)

    # Canvas + scrollbar para texto largo
    canvas = tk.Canvas(frame, borderwidth=0, highlightthickness=0)
    scroll_y = tb.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    text_frame = tb.Frame(canvas)

    text_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=text_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scroll_y.pack(side=RIGHT, fill=Y)

    # Etiqueta de info con wrap
    tb.Label(text_frame, text=info, wraplength=ancho-50, justify=LEFT).pack(pady=10)


btn_info = tb.Button(frame_selector, text="ℹ️", bootstyle="secondary-outline", command=mostrar_info, width=3) # <--- CAMBIO DE ESTILO
btn_info.pack(side=RIGHT, padx=(5,0))


frame_parametros = tb.Frame(panel_izq)
frame_parametros.pack(fill=X, pady=(10,5))

# -------- Variables y widgets --------
param_vars = [tk.StringVar() for _ in range(8)]
labels = [tb.Label(frame_parametros, text=f"Parámetro {i+1}:", font=("Helvetica",12), anchor="w") for i in range(8)] # <--- CAMBIO DE FUENTE
entries = [tb.Entry(frame_parametros, textvariable=param_vars[i], bootstyle="secondary") for i in range(8)] # <--- CAMBIO DE ESTILO

# Asignar validación una sola vez, de acuerdo a la lógica del proyecto
entries[0].configure(validate="key", validatecommand=vcmdf)
entries[1].configure(validate="key", validatecommand=vcmdi)
entries[2].configure(validate="key", validatecommand=vcmdi)
entries[3].configure(validate="key", validatecommand=vcmdif)
entries[4].configure(validate="key", validatecommand=vcmdif)
entries[5].configure(validate="key", validatecommand=vcmdfx)
entries[6].configure(validate="key", validatecommand=vcmdif)
entries[7].configure(validate="key", validatecommand=vcmdif)

# Ajuste de ancho uniforme y centrado
for lbl, ent in zip(labels, entries):
    lbl.pack(fill=X, pady=(2,0))
    ent.pack(fill=X, pady=(0,5))
    ent.config(justify="center")

# -------- Gráfica -------
sns.set_theme()  # inicializa Seaborn sin cambiar tu estilo
plt.style.use("dark_background")  # fondo oscuro con grilla suave

# Opcional: ajustar un poco los colores si quieres más contraste
plt.rcParams["axes.facecolor"] = "#2C3E50"  # fondo del gráfico
plt.rcParams["figure.facecolor"] = "#2C3E50"  # fondo de la figura
plt.rcParams["grid.color"] = "#566573"  # color de la grilla
fig, ax = plt.subplots(figsize=(6,4.5))
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().pack(fill=BOTH, expand=False)
graficador = Graficacion.Graficar(fig, canvas)

# -------- Función tabla con scroll y centrado --------
def tabla(datos, k):
    for w in frame_tabla.winfo_children():
        w.destroy()

    frame_scroll = tb.Frame(frame_tabla)
    frame_scroll.pack(fill=BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_scroll, orient="vertical")
    scroll_x = ttk.Scrollbar(frame_scroll, orient="horizontal")
    tree = ttk.Treeview(frame_scroll, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    tree.pack(fill=BOTH, expand=True)

    tree["columns"] = [f"x{i}" for i in range(k)]
    tree["show"] = "headings"
    for i in range(k):
        tree.heading(f"x{i}", text=f"x{i}")
        tree.column(f"x{i}", width=80, anchor="center")

    for fila in datos[:min(20, len(datos))]:
    # Si no es iterable, lo dejamos tal cual
        if isinstance(fila, (list, tuple, np.ndarray)):
            fila_formateada = [
                f"{v:.6f}" if isinstance(v, (float, int, np.integer, np.floating)) else v
                for v in fila
            ]
        else:
            fila_formateada = fila
        tree.insert("", "end", values=fila_formateada)


# -------- Función abrir ventana secundaria --------
def abrir_ventana_muestras(datos, columnas, titulo):
    ventana = tk.Toplevel(root)
    ventana.title(f"Todas las muestras - {titulo}")
    ventana.geometry(f"{int(ancho*0.7)}x{int(alto*0.6)}")
    ventana.minsize(500, 400)

    frame_tabla_sec = tb.Frame(ventana)
    frame_tabla_sec.pack(fill=BOTH, expand=True, padx=5, pady=5)

    scroll_y = ttk.Scrollbar(frame_tabla_sec, orient="vertical")
    scroll_x = ttk.Scrollbar(frame_tabla_sec, orient="horizontal")
    tree = ttk.Treeview(frame_tabla_sec, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    tree.pack(fill=BOTH, expand=True)

    tree["columns"] = columnas
    tree["show"] = "headings"
    for c in columnas:
        tree.heading(c, text=c)
        tree.column(c, width=80, anchor="center")

    for fila in datos:
        if isinstance(fila, (list, tuple, np.ndarray)):
            fila_formateada = [
                f"{v:.6f}" if isinstance(v, (float, int, np.integer, np.floating)) else v
                for v in fila
            ]
        else:
            fila_formateada = fila
        tree.insert("", "end", values=fila_formateada)

    def exportar_excel():
        file_path = filedialog.asksaveasfilename( defaultextension=".xlsx", filetypes=[("Excel files","*.xlsx")] )
        if file_path:
            try:
                df = pd.DataFrame(np.array(datos), columns=columnas)
                df.to_excel(file_path, index=False, engine='openpyxl')
                messagebox.showinfo("Exportar", f"Archivo guardado en: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    btn_exportar = tb.Button(ventana, text="Exportar a Excel", bootstyle="success-outline", command=exportar_excel)
    btn_exportar.pack(pady=10, fill=X)


# -------- Función actualizar parámetros con Enter --------
def actualizar_parametros(event=None):
    for var in param_vars:
        var.set("")
    dist = distribucion.get()

    
    # Ocultar todos los widgets
    for lbl, ent in zip(labels, entries):
        lbl.pack_forget()
        ent.pack_forget()

    # Ocultar todos los bindings para evitar conflictos
    for ent in entries:
        ent.unbind("<Return>")

    # Configuración según el diccionario
    current_params = config_dist.get(dist, {"params": []})["params"]
    
    for param in current_params:
        entry_idx = param["entry_idx"]
        bind_to_idx = param["bind_to"]
        
        labels[entry_idx].config(text=param["text"])
        labels[entry_idx].pack(fill=X, pady=(2,0))
        entries[entry_idx].pack(fill=X, pady=(0,5))
        
        if bind_to_idx is not None:
            entries[entry_idx].bind("<Return>", lambda e, next_entry=entries[bind_to_idx]: pasar_siguiente(e, next_entry))
        else:
            entries[entry_idx].bind("<Return>", lambda e: graficar())

        

distribucion.bind("<<ComboboxSelected>>", actualizar_parametros)
actualizar_parametros()

# -------- Función graficar --------
def graficar():
    try:
        fund = fd.FuncionDensidad()
        dist = distribucion.get()

        # Limpiar sliders o tablas previas
        for w in frame_grafica.winfo_children():
            if isinstance(w, tk.Scale) or isinstance(w, ttk.Treeview) or isinstance(w, tb.Button):
                w.destroy()

        p = [var.get() for var in param_vars]

        datos_tabla = []
        k = 1

        if dist == "Binomial":
            theta = float(p[0])
            num_ensayos = int(p[1])
            cantidad_muestras = int(p[2])
            datos_grafica, datos_tabla = fund.binomial(theta, num_ensayos, cantidad_muestras)
            graficador.histograma(dist, datos_grafica)
            datos_tabla = np.array(datos_tabla)
            k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1

        elif dist == "Binomial Puntual":
            theta = float(p[0])
            cantidad_muestras = int(p[1])
            datos_grafica, datos_tabla = fund.binomial_puntual(theta, cantidad_muestras)
            graficador.histograma(dist, datos_grafica)
            datos_tabla = np.array(datos_tabla)
            k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1

        elif dist == "Exponencial":
            lmbda = float(p[6])
            cantidad_muestras = int(p[1])

            if lmbda < 0:
                messagebox.showerror("Error", "Lambda debe ser >=")
                return

            datos_grafica, datos_tabla = fund.exponencial(cantidad_muestras, lmbda)
            graficador.normal(dist, datos_grafica)
            datos_tabla = np.array(datos_tabla)
            k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1

        elif dist == "Normal":
            cantidad_muestras = int(p[1])
            sigma = float(p[3])
            mu = float(p[4])

            if sigma <= 0:
                messagebox.showerror("Error de Parámetro", "La varianza (σ²) debe ser un número positivo mayor que cero.", parent=root)
                return

            datos_grafica, datos_tabla = fund.normal(cantidad_muestras, sigma, mu)
            graficador.normal(dist, datos_grafica)
            datos_tabla = np.array(datos_tabla)
            k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1

        elif dist == "Gibbs":
            cantidad_muestras = int(p[1])
            fxy = p[5]
            xy_string = re.split(r"[ ,]+", p[3].strip())
            intervalos_x_s = re.split(r"[ ,]+", p[4].strip())
            intervalos_y_s = re.split(r"[ ,]+", p[6].strip())

            try:
                xy = [float(t) for t in xy_string if t]
                intervalos_x = [float(t) for t in intervalos_x_s if t]
                intervalos_y = [float(t) for t in intervalos_y_s if t]
            except ValueError:
                messagebox.showerror("Error", "Debe ser dos numero valido separado por comas")
                return

            if len(xy) != 2 or len(intervalos_x) != 2 or len(intervalos_y) != 2:
                messagebox.showerror("Error", "La funcion debe ser bivariada")
                return

            datos_grafica = fund.gibbs_sample(fxy, xy,cantidad_muestras, intervalos=[intervalos_x[0],intervalos_x[1], intervalos_y[0], intervalos_x[1]] )

            if datos_grafica == None:
                messagebox.showerror("Error", "La funcion no converge")
                return

            arr = np.array(datos_grafica)
            x = arr[:,0]; y = arr[:,1]
            graficador.gibbs_bivariante_2D(x, y)
            datos_tabla = np.column_stack((x,y))
            k = datos_tabla.shape[1]

        elif dist == "Normal Bivariada":
            cantidad_muestras = int(p[1])
            media_string = re.split(r"[ ,]+", p[3].strip())
            desviacion_string = re.split(r"[ ,]+", p[4].strip())
            covarianza = float(p[6])


            try:
                media = [float(t) for t in media_string if t]
                desviacion = [float(t) for t in desviacion_string if t]
            except ValueError:
                messagebox.showerror("Error", "Deben ser numeros validos separados por comas")     

            if len(media) != 2 or len(desviacion) != 2:
                messagebox.showerror("Error", "EL conjunto de la media y la desviacion debe ser de dos valores")
                return

            if desviacion[0] <= 0 or desviacion[1] <= 0:
                messagebox.showerror("Error", "La desviacion debe ser un valor real mayor a 0")
                return

            if abs(covarianza) >= desviacion[0] * desviacion[1]:
                messagebox.showerror("Error", "la covarianza debe ser menor a la multiplicacion de la desviacion")
                return

            if media[0] == 0 and media[1] == 0:
                media[0] = 1e-9
                media[1] = 1e-9

            datos_grafica, parametros = fund.normal_bivariada(cantidad_muestras, media, desviacion, covarianza)

            arr = np.array(datos_grafica)
            x = arr[:,0]; y = arr[:,1]

            graficador.normal_bivariada(x, y, parametros)
            datos_tabla = np.column_stack((x,y))
            k = datos_tabla.shape[1]

        elif dist == "Triangulo con Gibbs":
            cantidad_muestras = int(p[1])
            punto_string = re.split(r"[ ,]+", p[3].strip())
            try:
                punto_inicial = [float(t) for t in punto_string if t]
            except ValueError:
                messagebox.showerror("Error", "Punto inicial debe ser dos numeros separados por comas")
                return

            if punto_inicial[0] < 0 or punto_inicial[1] < 0:
                messagebox.showerror("Error", "el punto inicial debe estar en los reales positivos")
                return

            datos_grafica = fund.triangulo(cantidad_muestras, punto_inicial)

            arr = np.array(datos_grafica)
            x = arr[:,0]; y = arr[:,1]

            graficador.gibbs_bivariante_2D(x, y)
            datos_tabla = np.column_stack((x,y))
            k = datos_tabla.shape[1]

        elif dist == "Lineal Bivariada":
            cantidad_muestras = int(p[1])
            punto_string = re.split(r"[ ,]+", p[3].strip())
            try:
                punto_inicial = [float(t) for t in punto_string if t]
            except ValueError:
                messagebox.showerror("Error", "Punto inicial debe ser dos numeros separados por comas")
                return

            if punto_inicial[0] < 0 or punto_inicial[1] < 0:
                messagebox.showerror("Error", "el punto inicial debe estar en los reales positivos")
                return

            datos_grafica = fund.lineal(cantidad_muestras, punto_inicial)

            arr = np.array(datos_grafica)
            x = arr[:,0]; y = arr[:,1]

            graficador.gibbs_bivariante_2D(x, y)
            datos_tabla = np.column_stack((x,y))
            k = datos_tabla.shape[1]

        elif dist == "Multinomial":
            tokens = re.split(r"[ ,]+", p[0].strip())
            probabilidades = [float(t) for t in tokens if t]
            cantidad_muestras = int(p[1]) if p[1] else 1000
            n_lanzamientos = int(p[2])
            if not 0.95 <= sum(probabilidades) <= 1.05:
                messagebox.showerror("Error", "La suma de probabilidades debe ser 1")
                return
            datos_tabla = np.array(fund.multinomial(probabilidades, cantidad_muestras, n_lanzamientos))
            k = len(probabilidades)

            # Slider para Multinomial
            slider_var = tk.IntVar(value=0)
            def on_release(event):
                idx = int(round(float(slider.get())))
                graficador.graficar_multinomial(datos_tabla, n_lanzamientos, idx)

            slider = tb.Scale(frame_grafica, from_=0, to=k-1, bootstyle="info", orient="horizontal", length=250, variable=slider_var)
            slider.pack(fill=X, pady=5, padx=10)
            slider.bind("<ButtonRelease-1>", on_release)

        # -------- Tabla y botón abrir todas las muestras --------
        root.update_idletasks()
        tabla(datos_tabla, k)

        columnas = [f"x{i}" for i in range(k)]
        btn_abrir = tb.Button(frame_grafica, text="📑 Ver todas las muestras", bootstyle=(tb.INFO, "outline"), padding=5,
                                command=lambda: abrir_ventana_muestras(datos_tabla, columnas, dist))
        btn_abrir.pack(side=BOTTOM, pady=5, fill=X)
    except  Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error en la simulación:\n{e}", parent=root)
        return

# -------- Botón graficar principal --------
boton = tb.Button(panel_izq, text="📊 Graficar", bootstyle=(tb.SUCCESS, "outline-toolbutton"), padding=10, command=graficar)
boton.pack(pady=20, fill=X)

btn_salir = tb.Button(panel_izq, text="❌ Salir", bootstyle="danger", command=cerrar)
btn_salir.pack(side=BOTTOM, fill=X, pady=(5,0))

# -------- Cierre seguro --------
root.protocol("WM_DELETE_WINDOW", cerrar)
root.mainloop()