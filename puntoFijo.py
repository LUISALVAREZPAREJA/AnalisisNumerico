import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from tkinter import messagebox

def evaluar_funcion(funcion, x):
    local_scope = {'x': x, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 
                   'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt}
    try:
        result = eval(funcion, {"__builtins__": None}, local_scope)
        return result
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

def calcular_punto_fijo(g, x0, tolerancia, max_iter):
    xrold = x0
    iteraciones = []
    
    for i in range(max_iter):
        xr = g(xrold)
        error = abs(xr - xrold)
        iteraciones.append((i + 1, xr, error))
        
        if error < tolerancia:
            return xr, iteraciones
        
        xrold = xr

    raise ValueError("No se alcanzó la convergencia en el número máximo de iteraciones.")

def graficar(iteraciones):
    iteraciones_num = [i[0] for i in iteraciones]
    valores_x = [i[1] for i in iteraciones]
    errores = [i[2] for i in iteraciones]
    
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(iteraciones_num, valores_x, marker='o', label='Valores de x')
    plt.title('Convergencia de x en cada iteración')
    plt.xlabel('Iteración')
    plt.ylabel('Valor de x')
    plt.grid(True)
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(iteraciones_num, errores, marker='o', color='r', label='Error Absoluto')
    plt.title('Error Absoluto en cada iteración')
    plt.xlabel('Iteración')
    plt.ylabel('Error Absoluto')
    plt.yscale('log')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def calcular():
    try:
        funcion = entry_funcion.get()
        x0 = float(entry_x0.get())
        tolerancia = float(entry_tolerancia.get())
        max_iter = int(entry_max_iter.get())

        g = lambda x: evaluar_funcion(funcion, x)

        resultado, iteraciones = calcular_punto_fijo(g, x0, tolerancia, max_iter)

        for i in tree.get_children():
            tree.delete(i)

        for it in iteraciones:
            tree.insert("", "end", values=it)

        label_resultado.config(text=f"Resultado: {resultado:.6f}")

        graficar(iteraciones)

    except Exception as e:
        label_resultado.config(text=f"Error: {str(e)}")

def abrir_punto_fijo():
    global entry_funcion, entry_x0, entry_tolerancia, entry_max_iter, tree, label_resultado

    ventana_punto_fijo = tk.Toplevel(root)
    ventana_punto_fijo.title("Método de Punto Fijo")

    tk.Label(ventana_punto_fijo, text="Función g(x):").grid(row=0, column=0)
    entry_funcion = tk.Entry(ventana_punto_fijo)
    entry_funcion.grid(row=0, column=1)
    entry_funcion.insert(0, "cos(x)")

    tk.Label(ventana_punto_fijo, text="Valor inicial x0:").grid(row=1, column=0)
    entry_x0 = tk.Entry(ventana_punto_fijo)
    entry_x0.grid(row=1, column=1)
    entry_x0.insert(0, "0.5") 

    tk.Label(ventana_punto_fijo, text="Tolerancia:").grid(row=2, column=0)
    entry_tolerancia = tk.Entry(ventana_punto_fijo)
    entry_tolerancia.grid(row=2, column=1)
    entry_tolerancia.insert(0, "1e-5")

    tk.Label(ventana_punto_fijo, text="Máximo de iteraciones:").grid(row=3, column=0)
    entry_max_iter = tk.Entry(ventana_punto_fijo)
    entry_max_iter.grid(row=3, column=1)
    entry_max_iter.insert(0, "100") 

    button_calcular = tk.Button(ventana_punto_fijo, text="Calcular", command=calcular)
    button_calcular.grid(row=4, columnspan=2)

    tree = ttk.Treeview(ventana_punto_fijo, columns=('Iteración', 'x', 'Error Absoluto'), show='headings')
    tree.heading('Iteración', text='Iteración')
    tree.heading('x', text='x')
    tree.heading('Error Absoluto', text='Error Absoluto')
    tree.grid(row=5, columnspan=2)

    label_resultado = tk.Label(ventana_punto_fijo, text="")
    label_resultado.grid(row=6, columnspan=2)

def salir():
    root.quit()

def abrir_menu_metodos():
    ventana_menu = tk.Toplevel(root)
    ventana_menu.title("Banco de Métodos")

    tk.Label(ventana_menu, text="Banco de Métodos", font=("Arial", 16)).pack(pady=10)

    button_punto_fijo = tk.Button(ventana_menu, text="Método de Punto Fijo", command=abrir_punto_fijo)
    button_punto_fijo.pack(pady=5)


    button_salir = tk.Button(ventana_menu, text="Salir", command=salir)
    button_salir.pack(pady=5)

root = tk.Tk()
root.title("Banco de Métodos")

menu_abierto = False

abrir_menu_metodos()

root.mainloop()
