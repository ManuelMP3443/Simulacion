import FuncionDensidad as fd
from Thread import TareaThread
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
    "Binomial Puntual": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 0},
            {"text": "Probabilidad de éxito (θ):", "entry_idx": 0, "bind_to": None},
        ]
    },

    "Binomial": {
        "params": [
            {"text": "Cantidad de muestras:", "entry_idx": 2, "bind_to": 1},
            {"text": "Número de ensayos:", "entry_idx": 1, "bind_to": 0},
            {"text": "Probabilidad de éxito (θ):", "entry_idx": 0, "bind_to": None},
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
    "Metropolis-Hasting Discreta": {
        "params": [
            
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 2}, 
            
            {"text": "BursTime:", "entry_idx": 2, "bind_to": 5},

            {"text": "Función f(k) o f(k,l):", "entry_idx": 5, "bind_to": 3}, 
           
            {"text": "Punto(s) inicial(es) (k0 ó k0,l0):", "entry_idx": 3, "bind_to": None},
            
        ]
    },
    "Metropolis-Hasting Continua": { # <-- Quité el espacio extra al final
        "params": [
        
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 2},

            {"text": "BursTime:", "entry_idx": 2, "bind_to": 5},
            
            {"text": "Función f(x) o f(x,y):", "entry_idx": 5, "bind_to": 3},
          
            {"text": "Punto(s) inicial(es) (x0 ó x0,y0):", "entry_idx": 3, "bind_to": 4},
            
            {"text": "Sigma (Propuesta):", "entry_idx": 4, "bind_to": None},
        ]
    },
    "Metropolis Poisson": {
        "params": [
            
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 2}, 
            
            {"text": "BursTime:", "entry_idx": 2, "bind_to": 3},

            {"text": "Punto inicial:", "entry_idx": 3, "bind_to": 6},

            {"text": "Lambda (λ):", "entry_idx": 6, "bind_to": None},
            
        ]
    },
    "Metropolis Beta": { 
        "params": [
        
            {"text": "Cantidad de muestras:", "entry_idx": 1, "bind_to": 2},

            {"text": "BursTime:", "entry_idx": 2, "bind_to": 4},

            {"text": "Sigma (Propuesta):", "entry_idx": 4, "bind_to": 3},
          
            {"text": "Punto inicial:", "entry_idx": 3, "bind_to": 5},

            {"text": "Beta (β):", "entry_idx": 5, "bind_to": 6},

            {"text": "alpha (α):", "entry_idx": 6, "bind_to": None},
        ]
    },
}

info_dist = {
    "Binomial Puntual": "Genera una secuencia de éxitos o fracasos. También se conoce como la distribución de Bernoulli.\n\n"
                      "Fórmula de la función de masa de probabilidad (PMF):\n"
                      "P(X=k) = θᵏ ⋅ (1 - θ)¹⁻ᵏ\n\n"
                      "Parámetros:\n"
                      "- Theta (θ): La probabilidad de éxito (0 < θ < 1).\n"
                      "- Cantidad de muestras: El número de resultados a generar.",

    "Binomial": "Simula el número de éxitos en una secuencia de n ensayos de Bernoulli.\n\n"
                  "Fórmula de la función de masa de probabilidad (PMF):\n"
                  "             ( n ) \n"
                  "P(X=k) = ( k ) ⋅ θᵏ ⋅ (1 - θ)ⁿ⁻ᵏ\n\n"
                  "Parámetros:\n"
                  "- Theta (θ): La probabilidad de éxito en cada ensayo (0 < θ < 1).\n"
                  "- Número de ensayos (n).\n"
                  "- Cantidad de muestras: El número de veces que se repite la simulación.",
    
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
    
        "Gibbs": (
        "El método de Gibbs es un algoritmo de muestreo para generar muestras de una distribución conjunta.\n"
        "Funciona muestreando secuencialmente cada variable de acuerdo con su distribución condicional dado el resto:\n"
        "  X | Y ~ P(X | Y=y)\n"
        "  Y | X ~ P(Y | X=x)\n\n"
        "Parámetros:\n"
        "- Función f(x,y): Una función que relaciona las variables; no se verifica automáticamente que sea una funcion de densidad.\n"
        "- Punto inicial (x₀, y₀): Valores de inicio para las variables.\n"
        "- Intervalos [a, b]: Rango de valores permitido para cada variable.\n"
        "- Cantidad de muestras: Número de puntos a generar mediante el método de Gibbs."
    ),

    
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
                          "- Punto inicial (x₀, y₀): El primer valor de x, y.\n"
                          "- Cantidad de muestras: Número de puntos a generar mediante Gibbs.",
    
    "Lineal Bivariada": "Distribución bivariada lineal (por ejemplo, f(x,y) = (2x + 3y + 2)/28) en un dominio rectangular.\n\n"
                      "Parámetros:\n"
                      "- Punto inicial (x₀, y₀): El primer valor de x, y.\n"
                      "- Cantidad de muestras: Número de puntos a generar mediante muestreo condicional.",
    
    "Multinomial": "Generalización de la distribución binomial para más de dos resultados posibles.\n\n"
                  "Fórmula de la función de masa de probabilidad (PMF):\n"
                  "                   n!      \n"
                  "P(x) = --------------- ⋅ θ₁ⁿ¹ ⋅ ... ⋅ θₖⁿᵏ\n"
                  "             n₁! ⋅ ... ⋅ nₖ!    \n\n"
                  "Parámetros:\n"
                  "- Probabilidades (θ₁, θ₂, ...): Las probabilidades de cada uno de los k resultados, que deben sumar 1.\n"
                  "- Número de ensayos: El número total de resultados en cada intento.\n"
                  "- Cantidad de muestras: El número de intentos a simular.",

    "Metropolis Poisson": (
        "Genera muestras de una distribución de Poisson usando el algoritmo Metropolis-Hastings (MCMC).\n"
        "Este método 'camina' por los enteros no negativos (0, 1, 2, ...) para encontrar la distribución.\n\n"
        "Fórmula de la función de masa de probabilidad (PMF):\n"
        "             λᵏ ⋅ e⁻λ\n"
        "P(X=k) = --------\n"
        "               k!\n\n"
        "El algoritmo MCMC no necesita la función completa, solo la parte proporcional (log-probabilidad):\n"
        "log(P) ∝ k ⋅ log(λ) - log(k!)\n\n"
        "Parámetros:\n"
        "- Lambda (λ): La tasa o media de eventos (λ > 0).\n"
        "- Punto inicial (k₀): Un entero >= 0 donde comienza la cadena.\n"
        "- Cantidad de muestras: Total de pasos de la simulación.\n"
        "- BursTime: Número de pasos iniciales a descartar (quemado)."
    ),

    "Metropolis Beta": (
        "Genera muestras de una distribución Beta usando el algoritmo Metropolis-Hastings (MCMC).\n"
        "Esta distribución vive exclusivamente en el dominio (0, 1) y se usa para modelar porcentajes o probabilidades.\n\n"
        "Fórmula de la función de densidad de probabilidad (PDF):\n"
        "                  xᵃ⁻¹ ⋅ (1-x)ᵝ⁻¹\n"
        "f(x; α, β) = -----------------\n"
        "                     B(α, β)\n\n"
        "Donde B(α, β) es la constante de normalización.\n\n"
        "El algoritmo usa la log-probabilidad (proporcional): \n"
        "log(P) ∝ (α-1)log(x) + (β-1)log(1-x)\n\n"
        "Parámetros:\n"
        "- Alpha (α): El primer parámetro de forma (α > 0).\n"
        "- Beta (β): El segundo parámetro de forma (β > 0).\n"
        "- Punto inicial (x₀): Un valor estrictamente entre 0 y 1 donde comienza la cadena.\n"
        "- Sigma (Propuesta): La desviación estándar de los 'saltos' aleatorios.\n"
        "- Cantidad de muestras: Total de pasos de la simulación.\n"
        "- BursTime: Número de pasos iniciales a descartar (quemado)."
    ),
    "Metropolis-Hasting Discreta": (
        "Implementa el algoritmo Metropolis-Hastings para un espacio de estados **discreto** (enteros).\n"
        "Este es un método MCMC (Monte Carlo por Cadenas de Markov) que 'camina' aleatoriamente por el espacio de estados (ej. k=0, 1, 2...) para generar muestras de una distribución.\n\n"
        "Es ideal para distribuciones como Poisson o Binomial.\n\n"
        "Parámetros:\n"
        "- Función f(k) o f(k,l): La **Log-Probabilidad** de la distribución (ej. 'k*log(5) - log(fac(k))' para Poisson).\n"
        "- Punto(s) inicial(es): Dónde empieza la cadena (ej. '1' o '1,1').\n"
        "- Cantidad de muestras: Total de pasos de la simulación.\n"
        "- BursTime: Número de pasos iniciales a descartar. La cadena necesita 'calentar' antes de converger a la distribución real. Un 10% del total es común.\n"
        "- Rango Finito: Si se marca, el algoritmo usará límites (ej. de 0 a N). Si se desmarca, asume un dominio infinito (ej. k >= 0)."
    ),

    "Metropolis-Hasting Continua": (
        "Implementa el algoritmo Metropolis-Hastings para un espacio de estados **continuo** (decimales).\n"
        "Este es un método MCMC que genera muestras de una distribución proponiendo 'saltos' aleatorios (basados en Sigma).\n\n"
        "Es ideal para distribuciones como la Normal o Beta.\n\n"
        "Parámetros:\n"
        "- Función f(x) o f(x,y): La **Log-Probabilidad** de la distribución (ej. '-pow(x-10, 2)/8' para una Normal).\n"
        "- Punto(s) inicial(es): Dónde empieza la cadena (ej. '0.5' o '0.1, 0.1').\n"
        "- Sigma (Propuesta): La 'agresividad' del salto. Un sigma pequeño explora lento; un sigma grande es rechazado a menudo. Es un parámetro clave a sintonizar.\n"
        "- Cantidad de muestras: Total de pasos de la simulación.\n"
        "- BursTime: Número de pasos iniciales a descartar. La cadena necesita 'calentar' antes de converger a la distribución real."
    ),
}

cargando = False


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
    if dist in ["Normal Bivariada", "Gibbs", "Triangulo con Gibbs", "Lineal Bivariada", "Metropolis-Hasting Continua", "Metropolis-Hasting Discreta"]:
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
    return bool(re.match(r'^[0-9a-z+\-*/^()., ]*$', valor))

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

frame_grafica.config(height=(alto/2)+alto*0.15)
frame_tabla.config(height=(alto/2)-alto*0.15)

frame_mh_config = tb.Frame(panel_izq) # Un frame para agruparlos

tb.Label(frame_mh_config, text="Dimensión:", font=("Helvetica", 12)).pack(fill=X, pady=(5,0))
combo_dim_mh = tb.Combobox(frame_mh_config, values=["1D (f(x))", "2D (f(x,y))"], bootstyle="secondary", state="readonly")
combo_dim_mh.set("1D (f(x))") # Valor por defecto
combo_dim_mh.pack(fill=X, pady=(0,5))

# Checkbox para Finito/Infinito (solo para Discreto)
check_finito_var = tk.BooleanVar(value=False) # Empieza como infinito
check_finito = tb.Checkbutton(frame_mh_config, text="Rango Finito", variable=check_finito_var, bootstyle="info-round-toggle")
# Este checkbutton se mostrará/ocultará junto con el Entry de N max

# Frame para agrupar N max (solo aparece si check_finito está marcado)
frame_n_max = tb.Frame(frame_mh_config)
lbl_n_max = tb.Label(frame_n_max, text="Límite(s) N max:", font=("Helvetica", 12))
entry_n_max = tb.Entry(frame_n_max, bootstyle="secondary")


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
                f"{v:.6f}" if isinstance(v, (float,np.floating)) else v
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
                f"{v:.6f}" if isinstance(v, (float, np.floating)) else v
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

    frame_mh_config.pack_forget() 
    frame_n_max.pack_forget() 
    check_finito.pack_forget()

    

    for ent in entries:
        ent.unbind("<Return>")

    if dist in ["Metropolis-Hasting Discreta", "Metropolis-Hasting Continua"]:
        # --- Mostrar Configuración de M-H ---
        frame_mh_config.pack(fill=X, pady=(10,5)) # Mostrar el frame
        
        # Mostrar ComboBox de Dimensión siempre
        combo_dim_mh.pack(fill=X, pady=(0,5)) 
        
        es_discreto = (dist == "Metropolis-Hasting Discreta")
        
        # Mostrar Checkbox y N max SOLO si es Discreto
        if es_discreto:
            check_finito.pack(fill=X, pady=(5,0))
            # Mostrar N max SOLO si el checkbox está marcado
            if check_finito_var.get(): 
                frame_n_max.pack(fill=X, pady=(0,5))
                lbl_n_max.pack(fill=X, pady=(2,0))
                entry_n_max.pack(fill=X, pady=(0,5))
            else: # Si no está marcado, N max va oculto
                 frame_n_max.pack_forget()
        
        # Configurar campos comunes de M-H (usando tu config_dist actualizada)
        current_params = config_dist[dist]["params"]
        for param in current_params:
            entry_idx = param["entry_idx"]
            bind_to_idx = param["bind_to"]
            
            # Ajustar texto del label según 1D/2D
            param_text = param["text"]
            if "Punto(s) inicial(es)" in param_text:
                param_text = "Punto inicial (x0):" if combo_dim_mh.get() == "1D (f(x))" else "Puntos iniciales (x0,y0):"
            elif "Función" in param_text:
                 param_text = "Función f(x):" if combo_dim_mh.get() == "1D (f(x))" else "Función f(x,y):"
            
            labels[entry_idx].config(text=param_text)
            labels[entry_idx].pack(fill=X, pady=(2,0))
            entries[entry_idx].pack(fill=X, pady=(0,5))
            
            
            if bind_to_idx is not None:
                entries[entry_idx].bind("<Return>", lambda e, next_entry=entries[bind_to_idx]: pasar_siguiente(e, next_entry))
            else:
                entries[entry_idx].bind("<Return>", lambda e: graficar())

    else: # Si NO es Metropolis-Hastings
            # Ocultar el frame de config de M-H por si acaso
        frame_mh_config.pack_forget()

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
combo_dim_mh.bind("<<ComboboxSelected>>", actualizar_parametros) # Que se re-dibuje al cambiar dimensión
check_finito.config(command=actualizar_parametros)
actualizar_parametros()

def mostrar_cargando():
    """Muestra un indicador de carga en la interfaz"""
    global cargando, lbl_cargando
    cargando = True
    
    # Crear label de carga si no existe
    if 'lbl_cargando' not in globals():
        lbl_cargando = tb.Label(
            frame_grafica, 
            text="⏳ Procesando...", 
            font=("Helvetica", 14, "bold"),
            bootstyle="info"
        )
    
    lbl_cargando.pack(expand=True)
    root.update_idletasks()

def ocultar_cargando():
    """Oculta el indicador de carga"""
    global cargando, lbl_cargando
    cargando = False
    if 'lbl_cargando' in globals():
        lbl_cargando.pack_forget()

def deshabilitar_controles():
    """Deshabilita controles durante el procesamiento"""
    boton.config(state='disabled')
    distribucion.config(state='disabled')
    for entry in entries:
        entry.config(state='disabled')

def habilitar_controles():
    """Habilita controles después del procesamiento"""
    boton.config(state='normal')
    distribucion.config(state='readonly')
    for entry in entries:
        entry.config(state='normal')


# ====== FUNCIÓN GRAFICAR CON PARALELIZACIÓN ======
def graficar():
    """Versión paralelizada de la función graficar"""
    
    # Deshabilitar interfaz mientras procesa
    deshabilitar_controles()
    mostrar_cargando()
    
    def tarea_calcular():
        """Tarea que se ejecuta en segundo plano"""
        try:
            fund = fd.FuncionDensidad()
            dist = distribucion.get()
            p = [var.get() for var in param_vars]
            # Diccionario para empaquetar los resultados
            resultado = {'extra': {}}
            datos_tabla = []
            k = 1
            if dist == "Binomial":
                theta = float(p[0])
                num_ensayos = int(p[1])
                cantidad_muestras = int(p[2])
                
                datos_grafica = fund.binomial(theta, num_ensayos, cantidad_muestras)
                datos_tabla = [(int(valores), int(frecuencia)) 
                   for valores, frecuencia in datos_grafica.items()]
                k = len(datos_tabla[0]) if datos_tabla else 0
                
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = datos_grafica
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'histograma'
            elif dist == "Binomial Puntual":
                theta = float(p[0])
                cantidad_muestras = int(p[1])
                
                datos_grafica, datos_tabla_lista = fund.binomial_puntual(theta, cantidad_muestras)
                datos_tabla = np.array(datos_tabla_lista)
                k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = datos_grafica
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'histograma'
            elif dist == "Exponencial":
                lmbda = float(p[6])
                cantidad_muestras = int(p[1])
                if lmbda < 0:
                    raise ValueError("Error Lambda debe ser >=")
                    
                datos_grafica, datos_tabla_lista = fund.exponencial(cantidad_muestras, lmbda)
                datos_tabla = np.array(datos_tabla_lista)
                k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
                
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = datos_grafica
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'normal' # Usas graficador.normal
            elif dist == "Normal":
                cantidad_muestras = int(p[1])
                sigma = float(p[3])
                mu = float(p[4])
                if sigma <= 0:
                    raise ValueError("Error de Parámetro La varianza (σ²) debe ser un número positivo mayor que cero.")
                    
                datos_grafica, datos_tabla_lista = fund.normal(cantidad_muestras, sigma, mu)
                datos_tabla = np.array(datos_tabla_lista)
                k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
                
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = datos_grafica
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'normal'
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
                    raise ValueError("Error Debe ser dos numero valido separado por comas")
                    
                if len(xy) != 2 or len(intervalos_x) != 2 or len(intervalos_y) != 2:
                    raise ValueError("Error La funcion debe ser bivariada")
                    
                datos_grafica_raw = fund.gibbs_sample(fxy, xy,cantidad_muestras, intervalos=[intervalos_x[0],intervalos_x[1], intervalos_y[0], intervalos_x[1]] )
                if datos_grafica_raw == None:
                    raise ValueError("Error La funcion no converge")
                    
                arr = np.array(datos_grafica_raw)
                x = arr[:,0]; y = arr[:,1]
                datos_tabla = np.column_stack((x,y))
                k = datos_tabla.shape[1]
                
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = (x, y) # Pasar (x, y)
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'gibbs_2d'
            elif dist == "Normal Bivariada":
                cantidad_muestras = int(p[1])
                media_string = re.split(r"[ ,]+", p[3].strip())
                desviacion_string = re.split(r"[ ,]+", p[4].strip())
                covarianza = float(p[6])
                try:
                    media = [float(t) for t in media_string if t]
                    desviacion = [float(t) for t in desviacion_string if t]
                except ValueError:
                    raise ValueError("Error Deben ser numeros validos separados por comas")     
                if len(media) != 2 or len(desviacion) != 2:
                    raise ValueError("Error EL conjunto de la media y la desviacion debe ser de dos valores separados por coma")
                if desviacion[0] <= 0 or desviacion[1] <= 0:
                    raise ValueError("Error La desviacion debe ser un valor real mayor a 0")
                if abs(covarianza) >= desviacion[0] * desviacion[1]:
                    raise ValueError("Error la covarianza debe ser menor a la multiplicacion de la desviacion")
                if media[0] == 0 and media[1] == 0:
                    media[0] = 1e-9; media[1] = 1e-9
                datos_grafica_raw, parametros = fund.normal_bivariada(cantidad_muestras, media, desviacion, covarianza)
                arr = np.array(datos_grafica_raw)
                x = arr[:,0]; y = arr[:,1]
                datos_tabla = np.column_stack((x,y))
                k = datos_tabla.shape[1]
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = (x, y) # Pasar (x, y)
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'normal_bivariada'
                resultado['extra']['parametros'] = parametros # Extra data
            elif dist == "Triangulo con Gibbs":
                cantidad_muestras = int(p[1])
                punto_string = re.split(r"[ ,]+", p[3].strip())
                try:
                    punto_inicial = [float(t) for t in punto_string if t]
                except ValueError:
                    raise ValueError("Error Punto inicial debe ser dos numeros separados por comas")
                if len(punto_inicial) != 2:
                    raise ValueError("Error EL punto inicial deben ser dos numeros separados por comas")
                if punto_inicial[0] < 0 or punto_inicial[1] < 0:
                    raise ValueError("Error el punto inicial debe estar en los reales positivos")
                    
                datos_grafica_raw = fund.triangulo(cantidad_muestras, punto_inicial)
                arr = np.array(datos_grafica_raw)
                x = arr[:,0]; y = arr[:,1]
                datos_tabla = np.column_stack((x,y))
                k = datos_tabla.shape[1]
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = (x, y) # Pasar (x, y)
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'gibbs_2d'
            elif dist == "Lineal Bivariada":
                cantidad_muestras = int(p[1])
                punto_string = re.split(r"[ ,]+", p[3].strip())
                try:
                    punto_inicial = [float(t) for t in punto_string if t]
                except ValueError:
                    raise ValueError("Error Punto inicial debe ser dos numeros separados por comas")
                if len(punto_inicial) != 2:
                    raise ValueError("Error EL punto inicial deben ser dos numeros separados por comas")
                if punto_inicial[0] < 0 or punto_inicial[1] < 0:
                    raise ValueError("Error el punto inicial debe estar en los reales positivos")
                    
                datos_grafica_raw = fund.lineal(cantidad_muestras, punto_inicial)
                arr = np.array(datos_grafica_raw)
                x = arr[:,0]; y = arr[:,1]
                datos_tabla = np.column_stack((x,y))
                k = datos_tabla.shape[1]
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = (x, y) # Pasar (x, y)
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'gibbs_2d'
            elif dist in ["Metropolis-Hasting Discreta", "Metropolis-Hasting Continua"]:
                tipo_mh = "Discreto" if "Discreta" in dist else "Continuo"
                dimension_mh = combo_dim_mh.get() 
                es_1D = (dimension_mh == "1D (f(x))")
                cantidad_muestras = int(p[1])
                burn = int(p[2])
                funcion_str = p[5] 
                xy_string = re.split(r"[ ,]+", p[3].strip()) 
                
                if es_1D and "y" in funcion_str.lower():
                    raise ValueError("Error La función solo puede ser respecto a x")
                
                # Validación de 'burn' (corregida)
                if burn >= cantidad_muestras:
                    raise ValueError("Error: El burn debe ser menor a las muestras")
                    
                if tipo_mh == "Continuo":
                    sigma = float(p[4])
                    if es_1D:
                        punto_inicial = float(xy_string[0])
                        datos_grafica, datos_tabla_lista = fund.metropolis_1d_continuo(funcion_str, punto_inicial, sigma, cantidad_muestras, burn)
                        datos_tabla = np.array(datos_tabla_lista)
                        k = 1 # 1D
                        
                        # ASIGNAR TODAS LAS CLAVES
                        resultado['dist'] = dist
                        resultado['datos_grafica'] = datos_grafica
                        resultado['datos_tabla'] = datos_tabla
                        resultado['k'] = k
                        resultado['extra']['tipo_grafica'] = 'normal'
                    
                    else: # 2D
                        punto_inicial = [float(t) for t in xy_string if t]
                        datos_grafica_raw = fund.metropolis_2d_continuo(funcion_str, punto_inicial, sigma, cantidad_muestras, burn)
                        arr = np.array(datos_grafica_raw)
                        x = arr[:,0]; y = arr[:,1]
                        datos_tabla = np.column_stack((x,y))
                        k = 2 # 2D
                        
                        # ASIGNAR TODAS LAS CLAVES
                        resultado['dist'] = dist
                        resultado['datos_grafica'] = (x, y)
                        resultado['datos_tabla'] = datos_tabla
                        resultado['k'] = k
                        resultado['extra']['tipo_grafica'] = 'gibbs_2d'
                
                else: # Discreto
                    es_finito = check_finito_var.get()
                    n_max = [-1] if es_1D else [-1, -1] # Valor por defecto
                    if es_finito:
                        n_max_list_str = re.split(r"[ ,]+", entry_n_max.get().strip())
                        n_max_int = [int(t) for t in n_max_list_str if t]
                        if es_1D and len(n_max_int) >= 1:
                            n_max = [n_max_int[0]]
                        elif not es_1D and len(n_max_int) >= 2:
                            n_max = [n_max_int[0], n_max_int[1]]
                        
                    if es_1D:
                        punto_inicial = int(xy_string[0])
                        limite_n = n_max[0] 
                        datos_grafica, datos_tabla_lista = fund.metropolis_1d_discreta(funcion_str, punto_inicial, limite_n, cantidad_muestras, burn)
                        datos_tabla = np.array(datos_tabla_lista)
                        k = 1 # 1D
                        
                        # ASIGNAR TODAS LAS CLAVES
                        resultado['dist'] = dist
                        resultado['datos_grafica'] = datos_grafica
                        resultado['datos_tabla'] = datos_tabla
                        resultado['k'] = k
                        resultado['extra']['tipo_grafica'] = 'normal'
                    
                    else: # 2D
                        punto_inicial = [int(t) for t in xy_string if t]
                        datos_grafica_raw = fund.metropolis_2d_discreta(funcion_str, punto_inicial, n_max, cantidad_muestras, burn)
                        arr = np.array(datos_grafica_raw)
                        x = arr[:,0]; y = arr[:,1]
                        datos_tabla = np.column_stack((x,y))
                        k = 2 # 2D
                        
                        # ASIGNAR TODAS LAS CLAVES
                        resultado['dist'] = dist
                        resultado['datos_grafica'] = (x, y)
                        resultado['datos_tabla'] = datos_tabla
                        resultado['k'] = k
                        resultado['extra']['tipo_grafica'] = 'gibbs_2d'

            elif dist == "Multinomial":
                tokens = re.split(r"[ ,]+", p[0].strip())
                try:
                    probabilidades = [float(t) for t in tokens if t]
                except ValueError:
                    raise ValueError("Error Las probabilidades debe numeros reales > 0 separados por comas")
                cantidad_muestras = int(p[1]) if p[1] else 1000
                n_lanzamientos = int(p[2])
                if not 0.95 <= sum(probabilidades) <= 1.05:
                    raise ValueError("Error La suma de probabilidades debe ser 1, usa comas para separarlas")
                    
                datos_tabla = np.array(fund.multinomial(probabilidades, cantidad_muestras, n_lanzamientos))
                k = len(probabilidades)
                # --- Datos para retornar ---
                resultado['dist'] = dist
                resultado['datos_grafica'] = datos_tabla # Pasa los datos crudos
                resultado['datos_tabla'] = datos_tabla
                resultado['k'] = k
                resultado['extra']['tipo_grafica'] = 'multinomial'
                resultado['extra']['n_lanzamientos'] = n_lanzamientos # Extra data

            elif dist == "Metropolis Poisson":
                cantidad_muestras = int(p[1]) 
                burn = int(p[2])
                xy_string = re.split(r"[ ,]+", p[3].strip()) 
                punto_inicial = int(xy_string[0])
                lmbda = float(p[6])
                fx = f"(x * log({lmbda})) - log(fac(x))"

                if lmbda <= 0:
                    raise ValueError("Error Lambda debe ser > 0")
                
                if burn > cantidad_muestras:
                    raise ValueError("Error el burn debe ser menor a las muestras")
                
                datos_grafica, datos_tabla_lista = fund.metropolis_1d_discreta(fx, punto_inicial, -1, cantidad_muestras, burn)
                        
                datos_tabla = np.array(datos_tabla_lista)
                k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
                
                # --- Datos para retornar ---
                resultado['dist'] = dist # <-- ¡AÑADE ESTO!
                resultado['datos_grafica'] = datos_grafica # <-- ¡AÑADE ESTO!
                resultado['datos_tabla'] = datos_tabla # <-- ¡AÑADE ESTO!
                resultado['k'] = k # <-- ¡AÑADE ESTO!
                resultado['extra']['tipo_grafica'] = 'normal'

            elif dist == "Metropolis Beta":  
                cantidad_muestras = int(p[1]) 
                burn = int(p[2])
                xy_string = re.split(r"[ ,]+", p[3].strip()) 
                alpha = float(p[6])
                sigma = float(p[4])

                try:
                    beta = float(p[5])
                except ValueError:
                    raise ValueError("Error Beta debe ser un numero > 0")
                
                

                
                if alpha <= 0:
                    raise ValueError("Error alpha debe ser > 0")
                
                if beta <= 0:
                    raise ValueError("Error beta debe ser > 0 ")
                
                if burn >= cantidad_muestras:
                    raise ValueError("Error el burn debe ser menor a las muestras")
                
                fx = f"({alpha}-1)*log(x) + ({beta}-1)*log(1-x)"

                punto_inicial = float(xy_string[0])

                if punto_inicial <= 0 or punto_inicial >= 1:
                    raise ValueError("Error el punto inicial debe estar entre 0 y 1")

                datos_grafica, datos_tabla_lista = fund.metropolis_1d_continuo(fx, punto_inicial, sigma, cantidad_muestras, burn)
                
                datos_tabla = np.array(datos_tabla_lista)
                k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
                
                # --- Datos para retornar ---
                resultado['dist'] = dist # <-- ¡AÑADE ESTO!
                resultado['datos_grafica'] = datos_grafica # <-- ¡AÑADE ESTO!
                resultado['datos_tabla'] = datos_tabla # <-- ¡AÑADE ESTO!
                resultado['k'] = k # <-- ¡AÑADE ESTO!
                resultado['extra']['tipo_grafica'] = 'normal' # Graficador normal/hist

                    
            return resultado
        except  Exception as e:
            raise ValueError(f"Error Inesperado Ocurrió un error en la simulación:\n{e}")

    

    def on_success_main_thread(resultado):
        """Callback que se ejecuta cuando la tarea termina exitosamente (EN HILO PRINCIPAL)"""
        try:
            # Limpiar interfaz
            for w in frame_grafica.winfo_children():
                if isinstance(w, (tk.Scale, ttk.Treeview, tb.Button)):
                    w.destroy()
            
            # ====== GRAFICAR (Esta parte corre en el hilo principal) ======
            tipo_graf = resultado['extra'].get('tipo_grafica')
            
            if tipo_graf == 'histograma':
                graficador.histograma(resultado['dist'], resultado['datos_grafica'])
            
            elif tipo_graf == 'normal':
                graficador.normal(resultado['dist'], resultado['datos_grafica'])
            
            elif tipo_graf == 'gibbs_2d':
                x, y = resultado['datos_grafica']
                graficador.gibbs_bivariante_2D(x, y)
            
            elif tipo_graf == 'normal_bivariada':
                x, y = resultado['datos_grafica']
                parametros = resultado['extra']['parametros']
                graficador.normal_bivariada(x, y, parametros)
            
            elif tipo_graf == 'multinomial':
                # ... (resto de tu código de on_success) ...
                datos = resultado['datos_grafica']
                n_lanz = resultado['extra']['n_lanzamientos']
                k = resultado['k']
                
                slider_var = tk.IntVar(value=0)
                graficador.graficar_multinomial(datos, n_lanz, 0)
                
                def on_release(event):
                    idx = int(round(float(slider.get())))
                    graficador.graficar_multinomial(datos, n_lanz, idx)
                
                slider = tb.Scale(
                    frame_grafica, from_=0, to=k-1,
                    bootstyle="info", orient="horizontal",
                    length=250, variable=slider_var
                )
                slider.pack(fill=X, pady=5, padx=10)
                slider.bind("<ButtonRelease-1>", on_release)
            
            # ====== ACTUALIZAR TABLA ======
            root.update_idletasks()
            tabla(resultado['datos_tabla'], resultado['k'])
            
            columnas = [f"x{i}" for i in range(resultado['k'])]
            btn_abrir = tb.Button(
                frame_tabla,
                text="🔓 Ver todas las muestras",
                bootstyle="info-outline",
                padding=5,
                command=lambda: abrir_ventana_muestras(
                    resultado['datos_tabla'], columnas, resultado['dist']
                )
            )
            btn_abrir.pack(side=BOTTOM, pady=5, fill=X)
            
        finally:
            ocultar_cargando()
            habilitar_controles()

    def on_error_main_thread(error):
        """Callback que se ejecuta si hay un error (EN HILO PRINCIPAL)"""
        ocultar_cargando()
        habilitar_controles()
        messagebox.showerror(
            "Error en la Simulación",
            f"Ocurrió un error:\n{str(error)}",
            parent=root
        )

    # --- NUEVAS FUNCIONES "MENSAJERAS" ---
    def on_success(resultado):
        """
        Este callback SÍ se ejecuta en el hilo secundario.
        Usa root.after() para enviar el resultado al hilo principal.
        """
        root.after(0, lambda: on_success_main_thread(resultado))

    def on_error(error):
        """
        Este callback SÍ se ejecuta en el hilo secundario.
        Usa root.after() para enviar el error al hilo principal.
        """
        root.after(0, lambda: on_error_main_thread(error))
    
    # ====== INICIAR THREAD ======
    # (El resto de tu función 'graficar' no cambia)
    thread = TareaThread(
        target=tarea_calcular,
        callback=on_success,       # Sigue usando las nuevas 'on_success'
        error_callback=on_error   # Sigue usando las nuevas 'on_error'
    )
    thread.start()

# -------- Botón graficar principal --------
boton = tb.Button(panel_izq, text="📊 Graficar", bootstyle="success-outline-toolbutton", padding=10, command=graficar)
boton.pack(pady=20, fill=X)

btn_salir = tb.Button(panel_izq, text="❌ Salir", bootstyle="danger", command=cerrar)
btn_salir.pack(side=BOTTOM, fill=X, pady=(5,0))

# -------- Cierre seguro --------
root.protocol("WM_DELETE_WINDOW", cerrar)
root.mainloop()