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




# Función de cierre seguro
def cerrar():
    root.quit()
    root.destroy()

def validar_entradaf(valor):
    dist = distribucion.get()
    if dist in ["Multinomial", "Multinomial-exponencial"]:
        return True
    else: 
        if valor == "":
            return True
        try:
            numero = float(valor)
            return 0 <= numero <= 1
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

# --- Ventana principal ---
root = tb.Window(themename="cosmo")
root.title("Simulación de Distribuciones")
root.geometry("1200x650")

vcmdf = (root.register(validar_entradaf), '%P') 
vcmdi = (root.register(validar_entradai), '%P') 

# Panel izquierdo
panel_izq = tb.Frame(root, bootstyle=LIGHT, width=250, padding=15)
panel_izq.pack(side=LEFT, fill=Y, padx=5, pady=5)

frame_central = tb.Frame(root)
frame_central.pack(side=LEFT, fill=BOTH, expand=True)

# Gráfico arriba
frame_grafica = tb.Frame(frame_central)
frame_grafica.pack(side=TOP, fill=X, expand=True, padx = 5, pady= 5)

# Tabla abajo
frame_tabla = tb.Frame(frame_central, bootstyle=LIGHT, width =300, padding =15)
frame_tabla.pack(side=TOP, fill= X, expand = False, padx = 5, pady= 5)


tb.Label(panel_izq, text="Selección", font=("Arial", 16, "bold"), bootstyle=INFO).pack(fill=X, pady=(0,15))

distribucion = tb.Combobox(panel_izq, values=["Binomial", "Binomial Puntual", "Multinomial", "Multinomial-exponencial"], bootstyle="info")
distribucion.pack(fill=X, pady=(0,5))
distribucion.current(0)

frame_parametros = tb.Frame(panel_izq, bootstyle=LIGHT)
frame_parametros.pack(fill=X, pady=(10,5))

param1_var = tk.StringVar()
param2_var = tk.StringVar()
param3_var = tk.StringVar()

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



fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().pack(fill=BOTH, expand=True)

graficador = Graficacion.Graficar(fig, canvas)

def tabla(datos, k):
    # Limpiar tabla anterior
    for w in frame_tabla.winfo_children():
        w.destroy()

    tree = ttk.Treeview(frame_tabla)
    tree.pack(fill=X, pady=2)
    tree["columns"] = [f"x{i}" for i in range(k)]
    tree["show"] = "headings"
    for i in range(k):
        tree.heading(f"x{i}", text=f"x{i}")
    for fila in datos[:min(20, len(datos))]:
        tree.insert("", "end", values=fila)


# Función para actualizar parámetros visibles
def actualizar_parametros(event=None):
    for widget in frame_parametros.winfo_children():
        widget.pack_forget()

    dist = distribucion.get()
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
    elif dist in ["Multinomial", "Multinomial-exponencial"]:
        label1.config(text="Probabilidades (separadas por ,):")
        label2.config(text="Cantidad de muestras:")
        label1.pack(pady=(5,2)); entry1.pack(fill=X,pady=(0,5))
        label2.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))

distribucion.bind("<<ComboboxSelected>>", actualizar_parametros)
actualizar_parametros()

# Función graficar
def graficar():
    fund = fd.FuncionDensidad()
    dist = distribucion.get()

    # Limpiar sliders o tablas previas
    for w in frame_grafica.winfo_children():
        if isinstance(w, tk.Scale) or isinstance(w, ttk.Treeview) or isinstance(w, tb.Button):
            w.destroy()

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

        suma = sum(probabilidades)
        if not 0.95 <= suma <= 1.05 :
            messagebox.showerror("Error", "La suma de probabilidades debe ser 1")
            return

        n_lanzamientos = 10  # fijo, o agregar entrada dinámica

        if dist == "Multinomial":
            datos = fund.multinomial(probabilidades, cantidad_muestras, n_lanzamientos)
        else:
            datos = fund.multinomial_exponencial(probabilidades, cantidad_muestras, n_lanzamientos)

        datos = np.array(datos)
        k = len(probabilidades)

        graficador.multinomial(datos, n_lanzamientos, dist, k)
        tabla(datos, k)

        root.update_idletasks()  
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

        # Botón para ventana con todas las muestras
        def abrir_ventana_muestras():
            ventana = tk.Toplevel(root)
            ventana.title(f"Todas las muestras - {dist}")
            ventana.geometry("1400x700")  # Tamaño inicial, ajustable

            # Frame contenedor para tabla + scroll
            frame_tabla_sec = tb.Frame(ventana)
            frame_tabla_sec.pack(fill=BOTH, expand=True, padx=5, pady=5)

            # Scroll vertical
            scrollbar = ttk.Scrollbar(frame_tabla_sec, orient="vertical")
            scrollbar.pack(side=RIGHT, fill=Y)

            # Treeview con scroll
            tree = ttk.Treeview(frame_tabla_sec, yscrollcommand=scrollbar.set)
            tree.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.config(command=tree.yview)

            # Configurar columnas
            tree["columns"] = [f"x{i}" for i in range(k)]
            tree["show"] = "headings"
            for i in range(k):
                tree.heading(f"x{i}", text=f"x{i}")

            # Insertar todos los datos
            for fila in datos:
                tree.insert("", "end", values=fila)

            # Botón exportar Excel
            def exportar_excel():
                file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files","*.xlsx")]
                )
                if file_path:
                    try:
                        # Asegurarse de usar una copia de los datos
                        df = pd.DataFrame(np.array(datos), columns=[f"x{i}" for i in range(k)])
                        df.to_excel(file_path, index=False, engine='openpyxl')  # especificar engine
                        messagebox.showinfo("Exportar", f"Archivo guardado en: {file_path}")
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

            btn_export = tb.Button(ventana, text="Exportar a Excel", command=exportar_excel)
            btn_export.pack(pady=5)

        btn_abrir = tb.Button(frame_grafica, text="Ver todas las muestras", command=abrir_ventana_muestras)
        btn_abrir.pack(pady=5)

# Botón Graficar
boton = tb.Button(panel_izq, text="Graficar", bootstyle=(PRIMARY, OUTLINE), command=graficar)
boton.pack(pady=20, fill=X)

# Cierre seguro
root.protocol("WM_DELETE_WINDOW", cerrar)
root.mainloop()
