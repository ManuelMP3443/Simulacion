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
        int(valor)
        return True
    except ValueError:
        return False

def validar_funcion(valor):
    return bool(re.match(r'^[0-9a-zA-Z+\-*/^()., ]*$', valor))

def pasar_siguiente(event, siguiente_entry):
    siguiente_entry.focus_set()

# -------- Inicialización de ventana --------
root = tb.Window(themename="cosmo")
root.title("Simulación de Distribuciones")

ancho = int(root.winfo_screenwidth() * 0.7)
alto = int(root.winfo_screenheight() * 0.6)
root.geometry(f"{ancho}x{alto}")
root.minsize(600, 400)

vcmdf = (root.register(validar_entradaf), '%P') 
vcmdi = (root.register(validar_entradai), '%P') 
vcmdif = (root.register(validar_entradaif), '%P') 
vcmdfx = (root.register(validar_funcion), '%P')

# -------- Panel izquierdo --------
panel_izq = tb.Frame(root, bootstyle=LIGHT, width=250, padding=15)
panel_izq.pack(side=LEFT, fill=Y, padx=5, pady=5)

frame_central = tb.Frame(root)
frame_central.pack(side=LEFT, fill=BOTH, expand=True)

frame_grafica = tb.Frame(frame_central)
frame_grafica.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

# Tabla siempre visible, con altura mínima
frame_tabla = tb.Frame(frame_central, bootstyle=LIGHT, padding=5)
frame_tabla.pack(side=TOP, fill=BOTH, expand=False, padx=5, pady=5)
frame_tabla.config(height=200)
frame_tabla.pack_propagate(False)  # evita que el frame se achique con la ventana

tb.Label(panel_izq, text="Selección", font=("Arial", 16, "bold"), bootstyle=INFO).pack(fill=X, pady=(0,15))

distribucion = tb.Combobox(panel_izq, values=["Binomial", "Binomial Puntual", "Multinomial", "exponencial", "Normal", "Gibbs"], bootstyle="info")
distribucion.pack(fill=X, pady=(0,5))
distribucion.current(0)

frame_parametros = tb.Frame(panel_izq, bootstyle=LIGHT)
frame_parametros.pack(fill=X, pady=(10,5))

# -------- Variables y widgets --------
param_vars = [tk.StringVar() for _ in range(8)]
labels = [tb.Label(frame_parametros, text=f"Parámetro {i+1}:", font=("Arial",12), anchor="w") for i in range(8)]
entries = [tb.Entry(frame_parametros, textvariable=param_vars[i], bootstyle="info") for i in range(8)]

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

# -------- Gráfica --------
fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().pack(fill=BOTH, expand=True)
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
        tree.column(f"x{i}", width=80, anchor="center")  # centrado

    for fila in datos[:min(20, len(datos))]:
    # Si no es iterable, lo dejamos tal cual
        if isinstance(fila, (list, tuple, np.ndarray)):
            fila_formateada = [
                f"{v:.6f}" if isinstance(v, (float, int, np.integer, np.floating)) else v
                for v in fila
            ]
        else:
            fila_formateada = fila  # un solo valor, lo dejamos
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

    # Insertar datos formateando condicionalmente
    for fila in datos:
        if isinstance(fila, (list, tuple, np.ndarray)):
            fila_formateada = [
                f"{v:.6f}" if isinstance(v, (float, int, np.integer, np.floating)) else v
                for v in fila
            ]
        else:
            fila_formateada = fila  # No iterable, se deja tal cual
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

    # Ocultar todos primero
    for lbl, ent in zip(labels, entries):
        lbl.pack_forget()
        ent.pack_forget()

    # Configuración según distribución
    if dist == "Binomial":
        labels[2].config(text="Cantidad de muestras:")
        labels[1].config(text="Número de ensayos:")
        labels[0].config(text="Theta (prob. éxito):")
        for i in [2,1,0]:
            labels[i].pack(fill=X, pady=(2,0))
            entries[i].pack(fill=X, pady=(0,5))
        entries[2].bind("<Return>", lambda e: pasar_siguiente(e, entries[1]))
        entries[1].bind("<Return>", lambda e: pasar_siguiente(e, entries[0]))
        entries[0].bind("<Return>", lambda e: graficar())

    elif dist == "Binomial Puntual":
        labels[1].config(text="Cantidad de muestras:")
        labels[0].config(text="Theta (prob. éxito):")
        for i in [1,0]:
            labels[i].pack(fill=X, pady=(2,0))
            entries[i].pack(fill=X, pady=(0,5))
        entries[1].bind("<Return>", lambda e: pasar_siguiente(e, entries[0]))
        entries[0].bind("<Return>", lambda e: graficar())

    elif dist == "exponencial":
        labels[1].config(text="Cantidad de muestras:")
        labels[0].config(text="lambda:")
        for i in [1,0]:
            labels[i].pack(fill=X, pady=(2,0))
            entries[i].pack(fill=X, pady=(0,5))
        entries[1].bind("<Return>", lambda e: pasar_siguiente(e, entries[0]))
        entries[0].bind("<Return>", lambda e: graficar())

    elif dist == "Normal":
        labels[1].config(text="Cantidad de Muestras:")
        labels[3].config(text="Varianza:")
        labels[4].config(text="Media:")
        for i in [1,3,4]:
            labels[i].pack(fill=X, pady=(2,0))
            entries[i].pack(fill=X, pady=(0,5))
        entries[1].bind("<Return>", lambda e: pasar_siguiente(e, entries[3]))
        entries[3].bind("<Return>", lambda e: pasar_siguiente(e, entries[4]))
        entries[4].bind("<Return>", lambda e: graficar())

    elif dist == "Gibbs":
        labels[1].config(text="Cantidad de muestras:")
        labels[5].config(text="Funcion F(X,Y)")
        labels[3].config(text="X")
        labels[4].config(text="Y")
        labels[6].config(text="a")
        labels[7].config(text="b")
        for i in [1,5,3,4,6,7]:
            labels[i].pack(fill=X, pady=(2,0))
            entries[i].pack(fill=X, pady=(0,5))
        entries[1].bind("<Return>", lambda e: pasar_siguiente(e, entries[5]))
        entries[5].bind("<Return>", lambda e: pasar_siguiente(e, entries[3]))
        entries[3].bind("<Return>", lambda e: pasar_siguiente(e, entries[4]))
        entries[4].bind("<Return>", lambda e: pasar_siguiente(e, entries[6]))
        entries[6].bind("<Return>", lambda e: pasar_siguiente(e, entries[7]))
        entries[7].bind("<Return>", lambda e: graficar())

    elif dist == "Multinomial":
        labels[1].config(text="Número de ensayos:")
        labels[2].config(text="Número de intentos:")
        labels[0].config(text="Theta (prob. éxito):")
        for i in [1,2,0]:
            labels[i].pack(fill=X, pady=(2,0))
            entries[i].pack(fill=X, pady=(0,5))
        entries[1].bind("<Return>", lambda e: pasar_siguiente(e, entries[2]))
        entries[2].bind("<Return>", lambda e: pasar_siguiente(e, entries[0]))
        entries[0].bind("<Return>", lambda e: graficar())

distribucion.bind("<<ComboboxSelected>>", actualizar_parametros)
actualizar_parametros()

# -------- Función graficar --------
def graficar():
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

    elif dist == "exponencial":
        lmbda = float(p[0])
        cantidad_muestras = int(p[1])
        datos_grafica, datos_tabla = fund.exponencial(cantidad_muestras, lmbda)
        graficador.normal(dist, datos_grafica)
        datos_tabla = np.array(datos_tabla)
        k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1

    elif dist == "Normal":
        cantidad_muestras = int(p[1])
        sigma = float(p[3])
        mu = float(p[4])
        datos_grafica, datos_tabla = fund.normal(cantidad_muestras, sigma, mu)
        graficador.normal(dist, datos_grafica)
        datos_tabla = np.array(datos_tabla)
        k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1

    elif dist == "Gibbs":
        cantidad_muestras = int(p[1])
        fxy = p[5]
        x0 = float(p[3])
        y0 = float(p[4])
        a = float(p[6])
        b = float(p[7])
        datos_grafica = fund.gibbs_sample(fxy, [x0, y0], cantidad_muestras, [a, b])
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
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")
    tabla(datos_tabla, k)

    columnas = [f"x{i}" for i in range(k)]
    btn_abrir = tb.Button(frame_grafica, text="📑 Ver todas las muestras", bootstyle=(INFO, "outline"), padding=5,
                          command=lambda: abrir_ventana_muestras(datos_tabla, columnas, dist))
    btn_abrir.pack(side=BOTTOM, pady=5, fill=X)

# -------- Botón graficar principal --------
boton = tb.Button(panel_izq, text="📊 Graficar", bootstyle=(SUCCESS, "outline-toolbutton"), padding=10, command=graficar)
boton.pack(pady=20, fill=X)

# -------- Cierre seguro --------
root.protocol("WM_DELETE_WINDOW", cerrar)
root.mainloop()
