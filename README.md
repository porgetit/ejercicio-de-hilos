# Ejercicio de hilos

Este programa ejemplifica el uso basico de hilos en Python para trabajar en paralelo con dos matrices cuadradas.

## Flujo principal

- Se definen dos matrices aleatorias de tamano `n x n` (por defecto `n = 4`), con numeros enteros entre 1 y 9.
- Cada matriz tiene un contenedor `ResultadoDiagonal` que guarda de forma segura la suma de su diagonal principal.
- Fase 1: se crean dos hilos (`trabajador_calcular`) que calculan la suma diagonal de su matriz y almacenan el resultado.
- Fase 2: se lanzan dos hilos (`trabajador_mostrar`) que leen el valor previamente guardado y lo muestran en pantalla.
- Las matrices se muestran en bloques de columnas usando `rich` para mantener legible la salida en la consola.

## Requisitos

- Python 3.10 o superior (se usa anotacion `list[int] | None` y `dataclasses`).
- Biblioteca `rich` para mejorar la salida en consola (`pip install rich`).

## Ejecucion

En la carpeta del proyecto:

```bash
python main.py
```

La salida muestra las dos matrices generadas y, a continuacion, el valor de la suma de la diagonal principal calculada por cada hilo.

## Personalizacion

- Cambia la variable `n` en `main.py` para ajustar el tamano de las matrices.
- Modifica los parametros de `crear_matriz` si quieres otros rangos de valores o desactivar la semilla fija (`random.seed(42)`).

> Nota: Este proyecto se elaboro con ayuda del agente Codex usando el modelo GPT5-codex de OpenAI.
