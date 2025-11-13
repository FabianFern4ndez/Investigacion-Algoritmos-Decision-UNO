"""Módulo para carga y exploración de datos"""

import pandas as pd
import numpy as np

def cargar_datos(ruta_archivo):
    """
    Carga el dataset UNO desde un archivo CSV

    Parameters:
    ruta_archivo (str): Ruta al archivo CSV

    Returns:
    pandas.DataFrame: Dataset cargado
    """
    try:
        df = pd.read_csv(ruta_archivo)

        # Renombrar columnas para consistencia
        df = df.rename(columns={
            'Agente': 'agent_name',
            'Victoria': 'wins',
            'Tiempo_Jugada_ms': 'execution_time_ms',
            'Turnos_Totales': 'total_turns',
            'Partida': 'game_id'
        })

        print(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
        print(f"Agentes encontrados: {df['agent_name'].unique()}")

        return df
    except Exception as e:
        raise Exception(f"Error cargando datos: {e}")

def explorar_datos(df):
    """
    Realiza exploración inicial del dataset

    Parameters:
    df (pandas.DataFrame): Dataset a explorar
    """
    print("\n=== INFORMACIÓN GENERAL ===")
    print(f"Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
    print(f"Columnas: {list(df.columns)}")

    print("\n=== TIPOS DE DATOS ===")
    print(df.dtypes)

    print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")
    print(df.describe())

    print("\n=== VALORES NULOS ===")
    nulos = df.isnull().sum()
    if nulos.sum() == 0:
        print("No hay valores nulos")
    else:
        print(nulos[nulos > 0])

    print("\n=== DISTRIBUCIÓN DE AGENTES ===")
    distribucion = df['agent_name'].value_counts()
    print(distribucion)

    # Estadísticas adicionales por agente
    print("\n=== VICTORIAS POR AGENTE ===")
    victorias_por_agente = df.groupby('agent_name')['wins'].sum()
    print(victorias_por_agente)