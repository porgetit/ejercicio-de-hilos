# -*- coding: utf-8 -*-
"""
Ejercicio (según enunciado del notebook):
- Dos matrices n x n
- Usar SOLO 2 hilos (uno por matriz)
- Primera ejecución: cada hilo calcula la SUMA de la diagonal PRINCIPAL de su matriz y la almacena
- Segunda ejecución: cada hilo MUESTRA el resultado calculado para su matriz
Notas:
- Código intencionalmente simple, con buenas prácticas y comentarios descriptivos.
"""
from __future__ import annotations
import threading
from dataclasses import dataclass
from typing import List
import random
import pprint

# -----------------------------
# Configuración inicial (tamaño n decidido al inicio del programa)
# -----------------------------
n: int = 4  # puedes cambiar este valor si deseas probar con otras dimensiones
random.seed(42)

# -----------------------------
# Utilidades simples de matrices
# -----------------------------
def crear_matriz(n: int, minimo: int = 1, maximo: int = 9) -> List[List[int]]:
    """Crea y retorna una matriz n x n con enteros aleatorios en [minimo, maximo]."""
    return [[random.randint(minimo, maximo) for _ in range(n)] for _ in range(n)]

def suma_diagonal_principal(m: List[List[int]]) -> int:
    """Calcula la suma de la diagonal principal de una matriz cuadrada."""
    return sum(m[i][i] for i in range(len(m)))

# -----------------------------
# Estructura para compartir resultados entre hilos de forma segura
# -----------------------------
@dataclass
class ResultadoDiagonal:
    """Contenedor seguro para la suma de la diagonal principal."""
    valor: int | None = None
    lock: threading.Lock = threading.Lock()

    def guardar(self, v: int) -> None:
        with self.lock:
            self.valor = v

    def leer(self) -> int | None:
        with self.lock:
            return self.valor

# -----------------------------
# "Primera ejecución": cada hilo calcula y ALMACENA la suma de su matriz
# -----------------------------
def trabajador_calcular(matriz: List[List[int]], resultado: ResultadoDiagonal, nombre: str) -> None:
    """Hilo que calcula la suma de la diagonal principal y la guarda."""
    suma = suma_diagonal_principal(matriz)
    resultado.guardar(suma)

# -----------------------------
# "Segunda ejecución": cada hilo MUESTRA el resultado ya calculado
# -----------------------------
def trabajador_mostrar(resultado: ResultadoDiagonal, etiqueta: str) -> None:
    """Hilo que imprime la suma previamente calculada."""
    suma = resultado.leer()
    print(f"{etiqueta}: suma diagonal principal = {suma}")

# -----------------------------
# Crear matrices
# -----------------------------
matriz_1 = crear_matriz(n)
matriz_2 = crear_matriz(n)

print("Matriz 1:")
pprint.pp(matriz_1)
print("\nMatriz 2:")
pprint.pp(matriz_2)

# Contenedores de resultados (uno por matriz)
res_m1 = ResultadoDiagonal()
res_m2 = ResultadoDiagonal()

# -----------------------------
# PRIMERA EJECUCIÓN (cálculo y almacenamiento)
# -----------------------------
hilo1 = threading.Thread(target=trabajador_calcular, args=(matriz_1, res_m1, "Hilo 1"), daemon=True)
hilo2 = threading.Thread(target=trabajador_calcular, args=(matriz_2, res_m2, "Hilo 2"), daemon=True)

hilo1.start()
hilo2.start()
hilo1.join()
hilo2.join()

# -----------------------------
# SEGUNDA EJECUCIÓN (mostrar resultados calculados)
# -----------------------------
hilo1_m = threading.Thread(target=trabajador_mostrar, args=(res_m1, "Hilo 1 (matriz 1)"), daemon=True)
hilo2_m = threading.Thread(target=trabajador_mostrar, args=(res_m2, "Hilo 2 (matriz 2)"), daemon=True)

hilo1_m.start()
hilo2_m.start()
hilo1_m.join()
hilo2_m.join()


