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
    if dist in ["Multinomial"]:
        return True
    else: 
        if valor == "":
            return True
        try:
            numero = float(valor)
            return 0 <= numero <= 1
        except ValueError:
            return False
        
def validar_entradaif(valor):
    if valor =="":
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
    

    
def pasar_siguiente(event, siguiente_entry):
    siguiente_entry.focus_set()   

if __name__ == '__main__':
    root = tb.Window(themename="cosmo")
    root.title("Simulación de Distribuciones")

    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight()

    root.geometry(f"{int(ancho*0.7)}x{int(alto*0.6)}")



    vcmdf = (root.register(validar_entradaf), '%P') 
    vcmdi = (root.register(validar_entradai), '%P') 
    vcmdif = (root.register(validar_entradaif), '%P') 

    # Panel izquierdo
    panel_izq = tb.Frame(root, bootstyle=LIGHT, width=250, padding=15)
    panel_izq.pack(side=LEFT, fill=Y, padx=5, pady=5)

    frame_central = tb.Frame(root)
    frame_central.pack(side=LEFT, fill=BOTH, expand=True)

    # Gráfico arriba
    frame_grafica = tb.Frame(frame_central)
    frame_grafica.pack(side=TOP, fill=X, expand=True, padx = 5, pady= 5)

    # Tabla abajo
    frame_tabla = tb.Frame(frame_central, bootstyle=LIGHT,width =300, height = 200, padding =15)
    frame_tabla.pack(side=TOP, fill= X, expand = False, padx = 5, pady= 5)


    tb.Label(panel_izq, text="Selección", font=("Arial", 16, "bold"), bootstyle=INFO).pack(fill=X, pady=(0,15))

    distribucion = tb.Combobox(panel_izq, values=["Binomial", "Binomial Puntual", "Multinomial", "exponencial", "Normal", "Gibbs"], bootstyle="info")
    distribucion.pack(fill=X, pady=(0,5))
    distribucion.current(0)

    frame_parametros = tb.Frame(panel_izq, bootstyle=LIGHT)
    frame_parametros.pack(fill=X, pady=(10,5))

    param1_var = tk.StringVar()
    param2_var = tk.StringVar()
    param3_var = tk.StringVar()
    param4_var = tk.StringVar()
    param5_var = tk.StringVar()

    label1 = tb.Label(frame_parametros, text="Parámetro 1:", font=("Arial",12))
    entry1 = tb.Entry(frame_parametros, textvariable=param1_var, bootstyle="info")
    entry1.configure(validate="key", validatecommand=vcmdf)

    label2 = tb.Label(frame_parametros, text="Parámetro 2:", font=("Arial",12))
    entry2 = tb.Entry(frame_parametros, textvariable=param2_var, bootstyle="info")
    entry2.configure(validate="key", validatecommand=vcmdi)

    label3 = tb.Label(frame_parametros, text="Parámetro 3:", font=("Arial",12))
    entry3 = tb.Entry(frame_parametros, textvariable=param3_var, bootstyle="info")
    entry3.configure(validate="key", validatecommand=vcmdi)

    label4 = tb.Label(frame_parametros, text="Parámetro 4:", font=("Arial",12))
    entry4 = tb.Entry(frame_parametros, textvariable=param4_var, bootstyle="info")
    entry4.configure(validate="key", validatecommand=vcmdif)

    label5 = tb.Label(frame_parametros, text="Parámetro 5:", font=("Arial",12))
    entry5 = tb.Entry(frame_parametros, textvariable=param5_var, bootstyle="info")
    entry5.configure(validate="key", validatecommand=vcmdif)


    entry1.bind("<Return>", lambda e: pasar_siguiente(e, entry2))
    entry2.bind("<Return>", lambda e: graficar())
    entry3.bind("<Return>", lambda e: graficar())
    entry4.bind("<Return>", lambda e: pasar_siguiente(e, entry5))
    entry5.bind("<Return>", lambda e: graficar())



    fig, ax = plt.subplots(figsize=(6,4))
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    graficador = Graficacion.Graficar(fig, canvas)

    # Función para abrir ventana con todas las muestras y exportar a Excel
    def abrir_ventana_muestras(datos, columnas, titulo):
        ventana = tk.Toplevel(root)
        ventana.title(f"Todas las muestras - {titulo}")
        ventana.geometry(f"{int(ancho*0.7)}x{int(alto*0.6)}")  # Tamaño inicial, ajustable

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
        tree["columns"] = columnas
        tree["show"] = "headings"
        for c in columnas:
            tree.heading(c, text=c)

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
                    df = pd.DataFrame(np.array(datos), columns=columnas)
                    df.to_excel(file_path, index=False, engine='openpyxl')
                    messagebox.showinfo("Exportar", f"Archivo guardado en: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

        btn_exportar = tb.Button(
        ventana,
        text="Exportar a Excel",
        bootstyle="success-outline",  # estilos: primary, secondary, success, info, warning, danger
        command=exportar_excel
        )
        btn_exportar.pack(pady=10, fill=X)



    def tabla(datos, k):
        # Limpiar tabla anterior
        for w in frame_tabla.winfo_children():
            w.destroy()

        tree = ttk.Treeview(frame_tabla)
        tree.pack(fill=BOTH, expand=True,pady=2)
        tree["columns"] = [f"x{i}" for i in range(k)]
        tree["show"] = "headings"
        for i in range(k):
            tree.heading(f"x{i}", text=f"x{i}")
            tree.column(f"x{i}",width=10, anchor="center")
        for fila in datos[:min(20, len(datos))]:
            tree.insert("", "end", values=fila)


    # Función para actualizar parámetros visibles
    def actualizar_parametros(event=None):
        param1_var.set("")
        param2_var.set("")
        param3_var.set("")
        param4_var.set("")
        param5_var.set("")

        for widget in frame_parametros.winfo_children():
            widget.pack_forget()

        dist = distribucion.get()
        entry2.unbind("<Return>")
        if dist == "Binomial Puntual" or dist == "exponencial":
            entry2.bind("<Return>", lambda e: graficar()) 
        else:
            entry2.bind("<Return>", lambda e: pasar_siguiente(e, entry3))  

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
        elif dist == "exponencial":
            label1.config(text="lambda:")
            label2.config(text="Cantidad de muestras:")
            label1.pack(pady=(5,2)); entry1.pack(fill=X,pady=(0,5))
            label2.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))
        elif dist == "Normal":
            label1.config(text="Cantidad de Muestras:")
            label4.config(text="Varianza:")
            label5.config(text="media: ")
            label1.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))
            label4.pack(pady=(5,2)); entry4.pack(fill=X,pady=(0,5))
            label5.pack(pady=(5,2)); entry5.pack(fill=X,pady=(0,5))
        elif dist in "Gibbs": 
            label1.config(text="convarianza p:")
            label2.config(text="Cantidad de muestras:")
            label4.config(text="X")
            label5.config(text="Y")

            label1.pack(pady=(5,2)); entry1.pack(fill=X,pady=(0,5))
            label2.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))
            label4.pack(pady=(5,2)); entry4.pack(fill=X,pady=(0,5))
            label5.pack(pady=(5,2)); entry5.pack(fill=X,pady=(0,5))
        
        elif dist in ["Multinomial"]:
            label1.config(text="Theta (prob. éxito):")
            label2.config(text="Número de ensayos:")
            label3.config(text="Numero de intentos:")
            label1.pack(pady=(5,2)); entry1.pack(fill=X,pady=(0,5))
            label2.pack(pady=(5,2)); entry2.pack(fill=X,pady=(0,5))
            label3.pack(pady=(5,2)); entry3.pack(fill=X,pady=(0,5))

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
        p4 = param4_var.get()
        p5 = param5_var.get()

        if dist == "Binomial":
            theta = float(p1)
            num_ensayos = int(p2)
            cantidad_muestras = int(p3)
            datos_grafica, datos_tabla = fund.binomial(theta, num_ensayos, cantidad_muestras)
            graficador.histograma(dist, datos_grafica)
            datos_tabla = np.array(datos_tabla)  # convertir a array para consistencia
            k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
            print(f"datos_tabla: {datos_tabla}, k: {k}")
        elif dist == "Binomial Puntual":
            theta = float(p1)
            cantidad_muestras = int(p2)
            datos_grafica, datos_tabla = fund.binomial_puntual(theta, cantidad_muestras)
            graficador.histograma(dist, datos_grafica)
            datos_tabla = np.array(datos_tabla)  # convertir a array para consistencia
            k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
        elif dist == "exponencial":
            lmbda = float(p1)
            cantidad_muestras = int(p2)
            datos_grafica, datos_tabla = fund.exponencial(cantidad_muestras,lmbda)
            graficador.normal(dist, datos_grafica)
            datos_tabla = np.array(datos_tabla)  # convertir a array para consistencia
            k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
        elif dist == "Normal":
            cantidad_muestras = int(p2)
            sigma = float(p4)
            mu = float(p5)
            datos_grafica, datos_tabla = fund.normal(cantidad_muestras, sigma, mu)
            graficador.normal(dist, datos_grafica)
            datos_tabla = np.array(datos_tabla)  # convertir a array para consistencia
            k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1
        elif dist == "Gibbs":
                rho = float(p1)
                cantidad_muestras = int(p2)
                x = float(p4)
                y = float(p5)
                
                x, y = fund.gibbs_bivariante(rho, cantidad_muestras, x, y)
                graficador.gibbs_bivariante_2D(x, y)

                datos_tabla = [x, y]
                datos_tabla = np.column_stack((x,y))
                k = datos_tabla.shape[1] if len(datos_tabla.shape) > 1 else 1

                
        elif dist in ["Multinomial"]:
            tokens = re.split(r"[ ,]+", p1.strip())
            probabilidades = [float(t) for t in tokens if t]
            cantidad_muestras = int(p2) if p2 else 1000
            n_lanzamientos = int(p3)

            suma = sum(probabilidades)
            if not 0.95 <= suma <= 1.05 :
                messagebox.showerror("Error", "La suma de probabilidades debe ser 1")
                return

            if dist == "Multinomial":
                datos_tabla = fund.multinomial(probabilidades, cantidad_muestras, n_lanzamientos)
            else:
                datos_tabla = fund.multinomial_exponencial(probabilidades, cantidad_muestras, n_lanzamientos)

            datos_tabla = np.array(datos_tabla)
            k = len(probabilidades)

            if hasattr(root, 'slider_prob') and root.slider_prob.winfo_exists():
                root.slider_prob.destroy()


            slider_var = tk.IntVar(value=0)

            def on_release(event):
                # obtener el valor actual y graficar (solo al soltar)
                idx = int(round(float(slider.get())))
                graficador.graficar_multinomial(datos_tabla, n_lanzamientos, idx)

            # slider estilizado con ttkbootstrap
            slider = tb.Scale(
                frame_grafica,
                from_=0,
                to=k-1,
                bootstyle="info",
                orient="horizontal",
                length=250,
                variable=slider_var,
                  # SOLO actualiza la etiqueta en tiempo real
            )
            slider.pack(fill=X, pady=5)

            slider.bind("<ButtonRelease-1>", on_release)


        root.update_idletasks()  
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")    

        tabla(datos_tabla, k)    

        columnas = [f"x{i}" for i in range(k)]

        btn_abrir = tb.Button(
        frame_grafica,
        text="📑 Ver todas las muestras",
        bootstyle=(INFO, "outline"),
        padding=5,
        command=lambda: abrir_ventana_muestras(datos_tabla, columnas, dist)
        )
        btn_abrir.pack(pady=10, fill=X)

    boton = tb.Button(
        panel_izq,
        text="📊 Graficar",
        bootstyle=(SUCCESS, "outline-toolbutton"),
        padding=10,
        command=graficar
    )
    boton.pack(pady=20, fill=X)

    # Cierre seguro
    root.protocol("WM_DELETE_WINDOW", cerrar)
    root.mainloop()
