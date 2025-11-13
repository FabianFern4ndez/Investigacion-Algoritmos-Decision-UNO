"""Módulo para visualizaciones mejoradas del análisis UNO"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Paleta personalizada para consistencia visual
palette = {
    'Random': '#F87171',          # Rojo coral
    'Reglas': '#60A5FA',          # Azul claro
    'Probabilistico': '#FBBF24',  # Amarillo suave
    'CFR': '#4ADE80'              # Verde lima
}

sns.set_theme(style="whitegrid", context="talk")


class VisualizacionesUNO:
    """Clase para generar visualizaciones del análisis UNO"""

    def __init__(self, df, resultados):
        self.df = df.copy()
        self.resultados = resultados
        self._preparar_datos()
        self._configurar_estilo()

    # ============================
    # 🔧 CONFIGURACIÓN GENERAL
    # ============================

    def _configurar_estilo(self):
        """Configura el estilo de las visualizaciones"""
        plt.rcParams.update({
            'figure.figsize': (12, 7),
            'axes.titlesize': 16,
            'axes.titleweight': 'bold',
            'axes.labelsize': 12,
            'axes.labelweight': 'regular',
            'font.size': 12,
            'grid.alpha': 0.3
        })
        sns.set_palette(list(palette.values()))

    def _preparar_datos(self):
        """Ajusta unidades y limpia datos extremos"""
        # Convertir tiempos a milisegundos si necesario
        if self.df['execution_time_ms'].max() < 1:
            self.df['execution_time_ms'] *= 1000

        # Agregar tasa de victoria si no existe
        if 'win_rate' not in self.df.columns:
            tasas = self.df.groupby('agent_name')['wins'].mean() * 100
            self.df = self.df.merge(tasas.rename('win_rate'), on='agent_name', how='left')

    def generar_todas_visualizaciones(self):
        """Genera todas las visualizaciones"""
        print("🎨 Generando visualizaciones...")

        os.makedirs('results/graficos', exist_ok=True)

        self.grafico_tasas_victoria()
        self.grafico_tiempo_ejecucion()
        self.grafico_duracion_partidas()
        self.grafico_distribucion_tiempos()
        self.grafico_distribucion_turnos()
        self.grafico_eficiencia()
        self.grafico_correlaciones()

        plt.close('all')
        print("✅ Gráficos guardados en carpeta results/graficos/")

    # ============================
    # 🏆 TASA DE VICTORIAS
    # ============================

    def grafico_tasas_victoria(self):
        """Gráfico de barras de tasa de victoria por agente"""
        fig, ax = plt.subplots()

        resumen = self.df.groupby('agent_name')['win_rate'].mean().reset_index()
        resumen = resumen.sort_values('win_rate', ascending=False)

        bars = sns.barplot(
            data=resumen,
            x='agent_name',
            y='win_rate',
            palette=palette,
            ax=ax
        )

        ax.set_title('🏆 Promedio de Tasa de Victorias por Agente')
        ax.set_xlabel('Agente de IA')
        ax.set_ylabel('Tasa de Victoria (%)')

        # Etiquetas sobre barras
        for container in bars.containers:
            bars.bar_label(container, fmt="%.1f%%", label_type='edge', fontsize=11)

        plt.tight_layout()
        plt.savefig('results/graficos/tasas_victoria.png', dpi=300, bbox_inches='tight')
        plt.show()

    # ============================
    # ⚙️ TIEMPO DE EJECUCIÓN
    # ============================

    def grafico_tiempo_ejecucion(self):
        """Gráfico clásico de dispersión vertical por agente (claro, profesional y legible)"""
        import seaborn as sns
        import matplotlib.pyplot as plt

        # Crear figura
        fig, ax = plt.subplots(figsize=(9, 6))

        # Dibujar la dispersión vertical (puntos individuales por agente)
        sns.stripplot(
            data=self.df,
            x='agent_name',
            y='execution_time_ms',
            jitter=0.3,  # ligera dispersión lateral
            alpha=0.85,  # leve transparencia
            size=6,  # tamaño de punto más visible
            edgecolor='black',  # borde para contraste
            linewidth=0.4,
            palette=palette,  # tus colores personalizados
            ax=ax
        )

        # Títulos y etiquetas
        ax.set_title('Distribución de tiempos de ejecución por agente', fontsize=15, fontweight='bold', pad=15)
        ax.set_xlabel('Agente de Inteligencia Artificial', fontsize=12)
        ax.set_ylabel('Tiempo por jugada (milisegundos)', fontsize=12)

        # Estilo clásico y limpio
        ax.set_facecolor('white')
        ax.grid(True, linestyle='--', alpha=0.4)
        sns.despine(left=False, bottom=False)

        # Ajustes visuales finales
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)
        plt.tight_layout()

        # Guardar y mostrar
        plt.savefig('results/graficos/tiempos_ejecucion_clasico.png', dpi=300, bbox_inches='tight')
        plt.show()

    # ============================
    # 🕓 DURACIÓN DE PARTIDAS
    # ============================

    def grafico_duracion_partidas(self):
        """Duración promedio de partidas (turnos)"""
        fig, ax = plt.subplots()

        sns.boxplot(
            data=self.df,
            x='agent_name',
            y='total_turns',
            palette=palette,
            showfliers=False,
            ax=ax
        )

        ax.set_title('🕓 Duración de Partidas por Agente')
        ax.set_xlabel('Agente de IA')
        ax.set_ylabel('Número de Turnos')
        plt.tight_layout()
        plt.savefig('results/graficos/duracion_partidas.png', dpi=300, bbox_inches='tight')
        plt.show()

    # ============================
    # 📊 DISTRIBUCIÓN DE TIEMPOS
    # ============================

    import pandas as pd
    import matplotlib.pyplot as plt

    # Cargar el CSV
    df = pd.read_csv("uno_agents_detailed.csv")

    # Limpiar columnas innecesarias
    df = df[['Agente', 'Partida', 'Tiempo_Jugada_ms']]

    # Crear figura con subgráficas
    agentes = df['Agente'].unique()
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, agente in enumerate(agentes):
        subset = df[df['Agente'] == agente]
        axes[i].scatter(subset['Partida'], subset['Tiempo_Jugada_ms'], alpha=0.7)
        axes[i].set_title(f"Tiempo de juego por partida - {agente}")
        axes[i].set_xlabel("Partida")
        axes[i].set_ylabel("Tiempo de Juego (ms)")
        axes[i].grid(True)

    # Ajustar espacio y mostrar
    plt.tight_layout()
    plt.show()

    # ============================
    # 📈 DISTRIBUCIÓN DE TURNOS
    # ============================

    def grafico_distribucion_turnos(self):
        """Boxplot de distribución de turnos"""
        fig, ax = plt.subplots()

        sns.boxplot(
            data=self.df,
            x='agent_name',
            y='total_turns',
            palette=palette,
            showfliers=False,
            width=0.5,
            ax=ax
        )

        ax.set_title('📈 Distribución de Turnos por Partida')
        ax.set_xlabel('Agente de IA')
        ax.set_ylabel('Turnos Totales')
        plt.tight_layout()
        plt.savefig('results/graficos/distribucion_turnos.png', dpi=300, bbox_inches='tight')
        plt.show()

    # ============================
    # ⚡ EFICIENCIA
    # ============================

    def grafico_eficiencia(self):
        """Comparación de eficiencia entre agentes"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        eficiencia = self.resultados['eficiencia_stats']

        sns.barplot(
            x=eficiencia.index,
            y='eficiencia_tiempo_norm',
            data=eficiencia,
            ax=axes[0],
            palette='coolwarm'
        )
        axes[0].set_title('⚡ Eficiencia por Tiempo')
        axes[0].set_ylabel('Eficiencia Normalizada (%)')

        sns.barplot(
            x=eficiencia.index,
            y='eficiencia_turnos_norm',
            data=eficiencia,
            ax=axes[1],
            palette='crest'
        )
        axes[1].set_title('🔄 Eficiencia por Turnos')
        axes[1].set_ylabel('Eficiencia Normalizada (%)')

        for ax in axes:
            ax.set_xlabel('Agente')
            ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig('results/graficos/eficiencia_agentes.png', dpi=300, bbox_inches='tight')
        plt.show()

    # ============================
    # 🔥 MATRIZ DE CORRELACIÓN
    # ============================

    def grafico_correlaciones(self):
        """Matriz de correlaciones entre variables numéricas"""
        fig, ax = plt.subplots(figsize=(8, 6))

        numeric_df = self.df.select_dtypes(include=['number']).drop(columns=['game_id'], errors='ignore')
        corr = numeric_df.corr().round(2)

        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap='Spectral',
            center=0,
            linewidths=0.5,
            square=True,
            cbar_kws={'shrink': 0.8, 'label': 'Coeficiente de Correlación'},
            ax=ax
        )

        ax.set_title('🔥 Correlación entre Variables Numéricas')
        plt.tight_layout()
        plt.savefig('results/graficos/matriz_correlacion.png', dpi=300, bbox_inches='tight')
        plt.show()
