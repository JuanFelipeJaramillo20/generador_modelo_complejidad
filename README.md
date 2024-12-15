# Generador de Modelos MiniZinc

Este proyecto es una aplicación en Python que genera modelos de optimización en **MiniZinc** a partir de datos ingresados por el usuario. Permite maximizar las ganancias de productos químicos bajo restricciones de recursos y demanda.

---

## **Características Principales**
1. Generación automática de código **MiniZinc** con datos de entrada personalizados.
2. Evaluación de restricciones de recursos y demanda (mínimo y máximo).
3. Implementación de restricciones de **no negatividad** en las soluciones.
4. Detección de problemas con datos inconsistentes o no factibles (valores negativos).
5. Interfaz gráfica amigable usando **Tkinter**.

---

## **Requisitos del Sistema**
- Python 3.7 o superior.
- Bibliotecas adicionales:
  - `tkinter`
  - `messagebox` (incluido en Tkinter)
- MiniZinc instalado en el sistema para ejecutar los modelos generados.

---

## **Instalación**

1. **Clona el repositorio** en tu máquina local:
   ```bash
   git clone https://github.com/JuanFelipeJaramillo20/generador_modelo_complejidad
   cd generador-minizinc
   ```

2. **Instala Python** si no lo tienes instalado:
   - Descárgalo desde [python.org](https://www.python.org/downloads/).

3. **Ejecuta el script principal**:
   ```bash
   python main.py
   ```

4. Asegúrate de tener **MiniZinc** instalado para ejecutar el código generado. Descárgalo desde:
   [https://www.minizinc.org/](https://www.minizinc.org/).

---

## **Uso de la Aplicación**

1. **Ejecuta la aplicación**:
   ```bash
   python main.py
   ```

2. Ingresa los datos en el área de texto en el siguiente formato:

   ```
   N  # Número de productos
   M  # Número de materias primas

   # Productos: nombre, precio, requerimientos (M valores)
   Grasa_azul 20000 2 3 9
   Grasa_amarilla 50000 3 9 9

   # Materias primas: nombre, costo, disponibilidad
   Materia_prima_1 1000 300
   Materia_prima_2 2500 400

   # Restricciones de demanda: nombre, tipo (minimo/maximo), valor
   Grasa_azul minimo 20
   Grasa_blanca maximo 60
   ```

3. Haz clic en **"Generar Código MiniZinc"** para crear el modelo.

4. Copia el código generado y ejecútelo en **MiniZinc IDE** o en la terminal.

---

## **Ejemplo de Entrada**
Entrada de datos:
```
4
3
Grasa_azul 20000 2 3 9
Grasa_amarilla 50000 3 9 9
Grasa_negra 30000 2 0 4
Grasa_blanca 30000 1 2 0
Materia_prima_1 1000 300
Materia_prima_2 2500 400
Materia_prima_3 4000 520
Grasa_azul minimo 20
Grasa_azul maximo 60
Grasa_blanca minimo 7
```

---

## **Salida Generada**

El programa genera un modelo de MiniZinc como este:

```minizinc
int: N = 4;
int: M = 3;

array[1..N] of string: productos = ["Grasa_azul", "Grasa_amarilla", "Grasa_negra", "Grasa_blanca"];
array[1..N] of int: precios = [20000, 50000, 30000, 30000];
array[1..N, 1..M] of int: requerimientos =
[| 2, 3, 9
 | 3, 9, 9
 | 2, 0, 4
 | 1, 2, 0 |];

array[1..M] of int: disponibilidad = [300, 400, 520];
array[1..N] of int: demanda_min = [20, 0, 0, 7];
array[1..N] of int: demanda_max = [60, 1000000, 1000000, 1000000];

array[1..N] of var int: x;
var int: Z = sum(i in 1..N)(precios[i] * x[i]);

constraint forall(j in 1..M)(
    sum(i in 1..N)(requerimientos[i, j] * x[i]) <= disponibilidad[j]
);

constraint forall(i in 1..N)(
    demanda_min[i] <= x[i] /\ x[i] <= demanda_max[i]
);

constraint forall(i in 1..N)(x[i] >= 0); % Restricción de no negatividad

solve maximize Z;

output [
    "Ganancias ", show(Z), "\n",
    "Producción óptima:\n",
    concat([productos[i] ++ ": " ++ show(x[i]) ++ " unidades\n" | i in 1..N])
];
```

---

## **Pruebas Realizadas**

Se realizaron pruebas con los siguientes escenarios:
1. **Datos proporcionados en el enunciado**.
2. **Disponibilidad de materias primas en cero**.
3. **Grandes entradas sin solución**.
4. **Grandes entradas con solución factible**.
5. **Valores negativos en las restricciones y requerimientos**.

---

## **Problemas Conocidos**
- Asegúrate de ingresar los datos correctamente en el formato solicitado.
- Los valores negativos generan un estado **UNSATISFIABLE** debido a la restricción de no negatividad en MiniZinc (a propósito).

---


## **Licencia**
Este proyecto está bajo la licencia **MIT**.

---

## **Contacto**
Para dudas o sugerencias:
- **Nombre:** [Juan Felipe Jaramillo]
- **Correo:** [juanfelipejaramillolosada@gmail.com]
- **GitHub:** [https://github.com/JuanFelipeJaramillo20](https://github.com/JuanFelipeJaramillo20)
