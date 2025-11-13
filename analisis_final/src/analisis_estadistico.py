"""Módulo para análisis estadístico"""

import pandas as pd
import numpy as np
from scipy import stats

class AnalisisUNO:
    """Clase para realizar análisis estadístico del dataset UNO"""

    def __init__(self, df):
        self.df = df
        self.resultados = {}

    def ejecutar_analisis_completo(self):
        """Ejecuta todo el análisis estadístico"""
        print("\nEJECUTANDO ANÁLISIS ESTADÍSTICO COMPLETO")

        # Análisis de victorias
        self.analizar_victorias()

        # Análisis de tiempos
        self.analizar_tiempos()

        # Análisis de turnos
        self.analizar_turnos()

        # Pruebas estadísticas
        self.pruebas_estadisticas()

        # Análisis comparativo
        self.analisis_comparativo()

        # Análisis de eficiencia
        self.analizar_eficiencia()

        return self.resultados

    def analizar_victorias(self):
        """Análisis de tasas de victoria por agente"""
        print("Analizando victorias...")

        # Calcular estadísticas de victorias
        victorias_stats = self.df.groupby('agent_name')['wins'].agg([
            'sum', 'count', 'mean', 'std'
        ]).round(4)

        victorias_stats['tasa_victoria'] = victorias_stats['mean'] * 100
        victorias_stats['partidas'] = victorias_stats['count']

        self.resultados['victorias_stats'] = victorias_stats
        self.resultados['tasa_victoria'] = victorias_stats['tasa_victoria']

        print("=== TASAS DE VICTORIA ===")
        for agente, stats in victorias_stats.iterrows():
            print(f"  {agente}: {stats['tasa_victoria']:.2f}% ({stats['sum']}/{stats['count']} victorias)")

    def analizar_tiempos(self):
        """Análisis de tiempos de ejecución"""
        print("⏱️ Analizando tiempos de ejecución...")

        tiempo_stats = self.df.groupby('agent_name')['execution_time_ms'].agg([
            'mean', 'std', 'min', 'max', 'median'
        ]).round(6)  # Más decimales para tiempos pequeños

        self.resultados['tiempo_stats'] = tiempo_stats

        print("=== ESTADÍSTICAS DE TIEMPOS (ms) ===")
        print(tiempo_stats)

    def analizar_turnos(self):
        """Análisis de duración de partidas"""
        print("Analizando duración de partidas...")

        turnos_stats = self.df.groupby('agent_name')['total_turns'].agg([
            'mean', 'std', 'min', 'max', 'median'
        ]).round(2)

        self.resultados['turnos_stats'] = turnos_stats

        print("=== ESTADÍSTICAS DE TURNOS ===")
        print(turnos_stats)

    def pruebas_estadisticas(self):
        """Realiza pruebas estadísticas"""
        print("Realizando pruebas estadísticas...")

        # ANOVA para tiempos entre agentes
        grupos_tiempos = [group['execution_time_ms'].values
                         for name, group in self.df.groupby('agent_name')]

        if len(grupos_tiempos) > 1:
            f_stat, p_value = stats.f_oneway(*grupos_tiempos)
            self.resultados['anova_tiempos'] = (f_stat, p_value)

            print(f"ANOVA tiempos: F={f_stat:.4f}, p={p_value:.4f}")

            if p_value < 0.05:
                print("  → DIFERENCIA SIGNIFICATIVA en tiempos entre agentes")
            else:
                print("  → Sin diferencia significativa en tiempos")

        # Test chi-cuadrado para victorias
        tabla_contingencia = pd.crosstab(self.df['agent_name'], self.df['wins'])
        chi2, p_chi, dof, expected = stats.chi2_contingency(tabla_contingencia)

        self.resultados['chi2_victorias'] = (chi2, p_chi)

        print(f"Chi-cuadrado victorias: χ²={chi2:.4f}, p={p_chi:.4f}")

        if p_chi < 0.05:
            print("  → DIFERENCIA SIGNIFICATIVA en distribución de victorias")
        else:
            print("  → Sin diferencia significativa en victorias")

    def analisis_comparativo(self):
        """Análisis comparativo entre pares de agentes"""
        print("\nAnálisis comparativo entre agentes...")

        agentes = self.df['agent_name'].unique()

        comparaciones = []
        for i in range(len(agentes)):
            for j in range(i + 1, len(agentes)):
                agente1, agente2 = agentes[i], agentes[j]

                # Comparar victorias
                wins1 = self.df[self.df['agent_name'] == agente1]['wins']
                wins2 = self.df[self.df['agent_name'] == agente2]['wins']

                # Test t para victorias
                t_stat, p_value = stats.ttest_ind(wins1, wins2)

                # Comparar tiempos
                tiempo1 = self.df[self.df['agent_name'] == agente1]['execution_time_ms']
                tiempo2 = self.df[self.df['agent_name'] == agente2]['execution_time_ms']
                t_tiempo, p_tiempo = stats.ttest_ind(tiempo1, tiempo2)

                comparacion = {
                    'agente1': agente1,
                    'agente2': agente2,
                    't_stat_victorias': t_stat,
                    'p_value_victorias': p_value,
                    'significativo_victorias': p_value < 0.05,
                    't_stat_tiempos': t_tiempo,
                    'p_value_tiempos': p_tiempo,
                    'significativo_tiempos': p_tiempo < 0.05
                }
                comparaciones.append(comparacion)

                print(f"{agente1} vs {agente2}:")
                print(f"  Victorias: p={p_value:.4f} {'V' if p_value < 0.05 else 'X'}")
                print(f"  Tiempos: p={p_tiempo:.4f} {'V' if p_tiempo < 0.05 else 'X'}")

        self.resultados['comparaciones'] = comparaciones

    def analizar_eficiencia(self):
        """Análisis de eficiencia: victorias por tiempo y turnos"""
        print("\nAnalizando eficiencia...")

        # Eficiencia = victorias / tiempo
        eficiencia_stats = self.df.groupby('agent_name').agg({
            'wins': 'mean',
            'execution_time_ms': 'mean',
            'total_turns': 'mean'
        })

        eficiencia_stats['eficiencia_tiempo'] = eficiencia_stats['wins'] / eficiencia_stats['execution_time_ms']
        eficiencia_stats['eficiencia_turnos'] = eficiencia_stats['wins'] / eficiencia_stats['total_turns']

        # Normalizar para mejor interpretación
        eficiencia_stats['eficiencia_tiempo_norm'] = (
            eficiencia_stats['eficiencia_tiempo'] / eficiencia_stats['eficiencia_tiempo'].max() * 100
        )
        eficiencia_stats['eficiencia_turnos_norm'] = (
            eficiencia_stats['eficiencia_turnos'] / eficiencia_stats['eficiencia_turnos'].max() * 100
        )

        self.resultados['eficiencia_stats'] = eficiencia_stats

        print("=== MÉTRICAS DE EFICIENCIA ===")
        print(eficiencia_stats[['eficiencia_tiempo_norm', 'eficiencia_turnos_norm']].round(2))