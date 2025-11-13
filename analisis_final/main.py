"""
ANÁLISIS ESTADÍSTICO - SIMULACIÓN UNO AGENTS
Autor: [Tu nombre]
Descripción: Análisis comparativo de agentes Random, Reglas y Probabilistico
"""

import pandas as pd
import numpy as np
from src.carga_datos import cargar_datos, explorar_datos
from src.analisis_estadistico import AnalisisUNO
from src.visualizaciones import VisualizacionesUNO
import warnings
warnings.filterwarnings('ignore')

def main():
    print("INICIANDO ANÁLISIS DE AGENTES UNO")
    print("=" * 50)

    try:
        # 1. CARGAR DATOS
        print("Cargando datos...")
        df = cargar_datos('data/uno_agents_detailed.csv')

        # 2. EXPLORACIÓN INICIAL
        print("Explorando datos...")
        explorar_datos(df)

        # 3. ANÁLISIS ESTADÍSTICO
        print("Realizando análisis estadístico...")
        analizador = AnalisisUNO(df)
        resultados = analizador.ejecutar_analisis_completo()

        # 4. VISUALIZACIONES
        print("Generando visualizaciones...")
        visualizador = VisualizacionesUNO(df, resultados)
        visualizador.generar_todas_visualizaciones()

        # 5. GUARDAR RESULTADOS
        print("Guardando resultados...")
        guardar_resultados(df, resultados)

        print("\n" + "=" * 50)


    except FileNotFoundError:
        print("Error: Archivo CSV no encontrado en la carpeta 'data/'")
        print("Asegúrate de que el archivo 'uno_agents_detailed.csv' esté en la carpeta 'data'")
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()

def guardar_resultados(df, resultados):
    """Guardar resultados del análisis"""
    import os

    # Crear carpetas si no existen
    os.makedirs('results/graficos', exist_ok=True)
    os.makedirs('results/datos', exist_ok=True)

    # Guardar datos procesados
    df.to_csv('results/datos/datos_procesados.csv', index=False)

    # Guardar resumen estadístico
    with open('results/resumen_analisis.txt', 'w', encoding='utf-8') as f:
        f.write("RESUMEN ANÁLISIS AGENTES UNO\n")
        f.write("=" * 50 + "\n\n")

        f.write("TASAS DE VICTORIA\n")
        f.write("-" * 30 + "\n")
        for agente, tasa in resultados['tasa_victoria'].items():
            f.write(f"{agente}: {tasa:.2f}% de victorias\n")

        f.write("\nESTADÍSTICAS DE TIEMPO\n")
        f.write("-" * 30 + "\n")
        f.write(resultados['tiempo_stats'].to_string())

        f.write("\n\nESTADÍSTICAS DE TURNOS\n")
        f.write("-" * 30 + "\n")
        f.write(resultados['turnos_stats'].to_string())

        f.write("\n\nPRUEBAS ESTADÍSTICAS\n")
        f.write("-" * 30 + "\n")
        if 'anova_tiempos' in resultados:
            f_stat, p_value = resultados['anova_tiempos']
            f.write(f"ANOVA Tiempos: F={f_stat:.4f}, p={p_value:.4f}\n")
            f.write("→ Diferencia significativa\n" if p_value < 0.05 else "→ Sin diferencia significativa\n")

        if 'chi2_victorias' in resultados:
            chi2, p_chi = resultados['chi2_victorias']
            f.write(f"Chi-cuadrado Victorias: χ²={chi2:.4f}, p={p_chi:.4f}\n")
            f.write("→ Diferencia significativa\n" if p_chi < 0.05 else "→ Sin diferencia significativa\n")

    print("Archivos guardados:")
    print("   - results/datos_procesados.csv")
    print("   - results/resumen_analisis.txt")
    print("   - results/graficos/ [varios gráficos PNG]")

if __name__ == "__main__":
    main()