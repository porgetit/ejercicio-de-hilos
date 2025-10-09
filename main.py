"""
Enunciado:
- Se tienen dos matrices cuadradas de tamano n x n.
- Utilizar unicamente 2 hilos, uno para cada matriz.
- En la primera fase, cada hilo debe calcular la suma de la diagonal principal de su respectiva matriz y guardar el resultado.
- En la segunda fase, cada hilo debe mostrar el resultado previamente calculado para su matriz.
"""
from __future__ import annotations
import threading
from dataclasses import dataclass
from typing import List
import random
from rich.console import Console
from rich.table import Table
from rich import box

# -----------------------------
# Configuracion inicial (tamano n decidido al inicio del programa)
# -----------------------------
n: int = 4  # Tamano de las matrices (n x n)
random.seed(42)
console = Console()

# -----------------------------
# Utilidades simples de matrices
# -----------------------------
def crear_matriz(n: int, minimo: int = 1, maximo: int = 9) -> List[List[int]]:
    """Crea y retorna una matriz n x n con enteros aleatorios en [minimo, maximo]."""
    return [[random.randint(minimo, maximo) for _ in range(n)] for _ in range(n)]

def suma_diagonal_principal(m: List[List[int]]) -> int:
    """Calcula la suma de la diagonal principal de una matriz cuadrada."""
    return sum(m[i][i] for i in range(len(m)))

def mostrar_matriz(matriz: List[List[int]], titulo: str, columnas_por_bloque: int = 8) -> None:
    """Muestra la matriz dividiendola en bloques de columnas para mantenerla legible."""
    if not matriz:
        console.print(f"[bold red]{titulo}[/]: matriz vacia")
        return

    total_columnas = len(matriz[0])
    columnas_por_bloque = max(1, min(columnas_por_bloque, total_columnas))

    for inicio in range(0, total_columnas, columnas_por_bloque):
        fin = min(inicio + columnas_por_bloque, total_columnas)
        titulo_bloque = (
            f"{titulo} (columnas {inicio + 1}-{fin})"
            if total_columnas > columnas_por_bloque
            else titulo
        )

        tabla = Table(
            title=titulo_bloque,
            box=box.SIMPLE_HEAD,
            header_style="bold magenta",
            show_lines=False,
            expand=False,
        )
        tabla.add_column("Fila", justify="right", style="bold yellow")
        for col_idx in range(inicio, fin):
            tabla.add_column(f"C{col_idx + 1}", justify="center")

        for indice, fila in enumerate(matriz, start=1):
            celdas = [f"{fila[col_idx]:>2}" for col_idx in range(inicio, fin)]
            tabla.add_row(str(indice), *celdas)

        console.print(tabla)

# -----------------------------
# Estructura para compartir resultados entre hilos
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
# "Primera ejecucion": cada hilo calcula y ALMACENA la suma de su matriz
# -----------------------------
def trabajador_calcular(matriz: List[List[int]], resultado: ResultadoDiagonal, nombre: str) -> None:
    """Hilo que calcula la suma de la diagonal principal y la guarda."""
    suma = suma_diagonal_principal(matriz)
    resultado.guardar(suma)

# -----------------------------
# "Segunda ejecucion": cada hilo MUESTRA el resultado ya calculado
# -----------------------------
def trabajador_mostrar(resultado: ResultadoDiagonal, etiqueta: str) -> None:
    """Hilo que imprime la suma previamente calculada."""
    suma = resultado.leer()
    console.print(
        f"[bold green]{etiqueta}[/]: suma diagonal principal = [bold cyan]{suma}[/]",
        highlight=False,
    )

# -----------------------------
# Crear matrices
# -----------------------------
matriz_1 = crear_matriz(n)
matriz_2 = crear_matriz(n)

console.rule("[bold yellow]Matrices generadas")
mostrar_matriz(matriz_1, "Matriz 1")
mostrar_matriz(matriz_2, "Matriz 2")

# Contenedores de resultados (uno por matriz)
res_m1 = ResultadoDiagonal()
res_m2 = ResultadoDiagonal()

# -----------------------------
# PRIMERA EJECUCION (calculo y almacenamiento)
# -----------------------------
hilo1 = threading.Thread(target=trabajador_calcular, args=(matriz_1, res_m1, "Hilo 1"), daemon=True)
hilo2 = threading.Thread(target=trabajador_calcular, args=(matriz_2, res_m2, "Hilo 2"), daemon=True)

hilo1.start()
hilo2.start()
hilo1.join()
hilo2.join()

# -----------------------------
# SEGUNDA EJECUCION (mostrar resultados calculados)
# -----------------------------
console.rule("[bold yellow]Resultados")
hilo1_m = threading.Thread(target=trabajador_mostrar, args=(res_m1, "Hilo 1 (matriz 1)"), daemon=True)
hilo2_m = threading.Thread(target=trabajador_mostrar, args=(res_m2, "Hilo 2 (matriz 2)"), daemon=True)

hilo1_m.start()
hilo2_m.start()
hilo1_m.join()
hilo2_m.join()


