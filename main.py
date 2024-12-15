import tkinter as tk
from tkinter import scrolledtext, messagebox


def procesar_entrada():
    try:
        # Obtener los datos ingresados por el usuario
        datos = text_area.get("1.0", tk.END).strip().split("\n")

        N = int(datos[0])  # Número de productos químicos
        M = int(datos[1])  # Número de materias primas

        # Extraer productos
        productos = []
        for i in range(2, 2 + N):
            productos.append(datos[i].split())

        # Extraer materias primas
        materias_primas = []
        for i in range(2 + N, 2 + N + M):
            materias_primas.append(datos[i].split())

        # Extraer restricciones de demanda
        demandas = []
        for i in range(2 + N + M, len(datos)):
            demandas.append(datos[i].split())

        # Generar el código MiniZinc
        codigo = generar_codigo_minizinc(N, M, productos, materias_primas, demandas)

        # Mostrar el código generado
        output_area.delete("1.0", tk.END)
        output_area.insert(tk.END, codigo)
        messagebox.showinfo("Éxito", "Código MiniZinc generado correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema con los datos ingresados.\n{e}")


def generar_codigo_minizinc(N, M, productos, materias_primas, demandas):
    # Encabezado del código
    codigo = f"int: N = {N};\nint: M = {M};\n\n"

    # Nombres y precios de productos
    nombres_productos = [f'"{p[0]}"' for p in productos]
    precios = [p[1] for p in productos]
    requerimientos = [p[2:] for p in productos]

    codigo += f"array[1..N] of string: productos = [{', '.join(nombres_productos)}];\n"
    codigo += f"array[1..N] of int: precios = [{', '.join(map(str, precios))}];\n"

    # Matriz de requerimientos
    codigo += "array[1..N, 1..M] of int: requerimientos =\n[| "
    for i, req in enumerate(requerimientos):
        fila = ', '.join(map(str, req))
        codigo += fila
        if i < N - 1:
            codigo += "\n | "
    codigo += " |];\n\n"

    # Datos de materias primas
    nombres_mp = [f'"{m[0]}"' for m in materias_primas]
    costos = [m[1] for m in materias_primas]
    disponibilidades = [m[2] for m in materias_primas]

    codigo += f"array[1..M] of string: materias_primas = [{', '.join(nombres_mp)}];\n"
    codigo += f"array[1..M] of int: costos = [{', '.join(map(str, costos))}];\n"
    codigo += f"array[1..M] of int: disponibilidad = [{', '.join(map(str, disponibilidades))}];\n\n"

    # Demandas mínimas y máximas
    min_demanda = ["0"] * N
    max_demanda = ["1000000"] * N

    for d in demandas:
        index = nombres_productos.index(f'"{d[0]}"')
        if d[1] == "minimo":
            min_demanda[index] = str(max(0, int(d[2])))  # Asegurar no negativos
        elif d[1] == "maximo":
            max_demanda[index] = str(int(d[2]))  # Convertir a entero correctamente

    codigo += f"array[1..N] of int: demanda_min = [{', '.join(min_demanda)}];\n"
    codigo += f"array[1..N] of int: demanda_max = [{', '.join(max_demanda)}];\n\n"

    # Variables, restricciones y función objetivo
    codigo += """
array[1..N] of var int: x;

var int: Z = sum(i in 1..N)(precios[i] * x[i]);

% Restricciones de disponibilidad
constraint forall(j in 1..M)(
    sum(i in 1..N)(requerimientos[i, j] * x[i]) <= disponibilidad[j]
);

% Restricciones de demanda mínima y máxima
constraint forall(i in 1..N)(
    demanda_min[i] <= x[i] /\\ x[i] <= demanda_max[i]
);

% Restricción explícita de no negatividad
constraint forall(i in 1..N)(x[i] >= 0);

% Restricción para validar valores no negativos en requerimientos
constraint forall(i in 1..N, j in 1..M)(
    requerimientos[i, j] >= 0
);

solve maximize Z;

output [
    "Ganancias ", show(Z), "\\n",
    "Producción óptima:\\n",
    concat([productos[i] ++ ": " ++ show(x[i]) ++ " unidades\\n" | i in 1..N])
];
"""
    return codigo



# Crear la interfaz gráfica
root = tk.Tk()
root.title("Generador de Código MiniZinc")

# Área de texto para la entrada
tk.Label(root, text="Entrada de Datos:").pack()
text_area = scrolledtext.ScrolledText(root, width=60, height=15)
text_area.pack()

# Botón para procesar
tk.Button(root, text="Generar Código MiniZinc", command=procesar_entrada).pack()

# Área de texto para el resultado
tk.Label(root, text="Código MiniZinc Generado:").pack()
output_area = scrolledtext.ScrolledText(root, width=60, height=15)
output_area.pack()

# Ejecutar la aplicación
root.mainloop()
