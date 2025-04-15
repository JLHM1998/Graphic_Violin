# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:27:03 2025

@author: JAQUILLE
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Configuración global de fuente para gráficos
plt.rcParams['font.family'] = 'Palatino Linotype'

# Cargar los archivos CSV
df = pd.read_csv("C:/Users/joluh/OneDrive/Thesis/Articles/Satellite/Cod/2022_2023.csv", header=[0, 1])  # Archivo con datos principales
df1 = pd.read_csv("C:/Users/joluh/OneDrive/Thesis/Articles/Satellite/Cod/Numero_datos.csv", index_col='Years')  # Archivo con datos de días por año

# Extraer los valores de días para 2022 y 2023 desde df1
dias_2022 = pd.Series(df1.iloc[0].values).dropna()  # Días de 2022
dias_2023 = pd.Series(df1.iloc[1].values).dropna()  # Días de 2023

# Verificar que ambas series tengan la misma longitud
num_etapas = len(dias_2023)

# Cambiar el nombre de los niveles del encabezado para 'Año' y 'Etapa'
df.columns.names = ["Año", "Etapa"]

# Reorganizar los datos en formato largo (long format) con pd.melt
df_melted = df.melt(value_name="Valor", ignore_index=False).reset_index()

# Lista ordenada de etapas (limitar según la longitud de las etapas)
etapas_ordenadas = [
    '1.Enero', '2.Febrero', '3.Marzo', '4.Abril', '5.Mayo',
    '6.Junio', '7.Julio', '8.Agosto', '9.Setiembre', '10.Octubre', '11.Noviembre'
]
etapas_ordenadas = etapas_ordenadas[:num_etapas]

# Convertir 'Etapa' en una variable categórica ordenada
df_melted['Etapa'] = pd.Categorical(df_melted['Etapa'], categories=etapas_ordenadas, ordered=True)

# Crear la figura con dos subplots (uno arriba, otro abajo)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), dpi=300, sharex=True, gridspec_kw={'height_ratios': [1, 2]})

# PARTE SUPERIOR: Graficar los días de 2022 y 2023 en el primer subplot (ax1)
positions = list(range(num_etapas))
positions2 = list(range(dias_2022.index[0], dias_2022.index[6] + 1))

# Graficar los días de 2022 como una línea (verde)
ax1.plot(positions2, dias_2022, color='seagreen', marker='*', linestyle='--', label='2022', markersize=10)

# Graficar los días de 2023 como una línea (naranja)
ax1.plot(positions, dias_2023, color='chocolate', marker='o', linestyle='-', label='2023', markersize=10)

# Ajustar el límite del eje Y en ax1
ax1.set_ylim(0, max(max(dias_2022), max(dias_2023)))
ax1.set_ylabel('Number of plots ', fontsize=14, fontweight='bold', labelpad=20)

# Ajustar ticks del eje Y en ax1
max_value = max(max(dias_2022), max(dias_2023))
step_size = 10
yticks = np.arange(0, max_value + step_size, step_size)
ax1.set_yticks(yticks)

# Añadir leyenda y configuración de ticks en ax1
ax1.legend(title='Years', fontsize=12, title_fontsize=14,  loc='upper left')
ax1.grid(False)
ax1.tick_params(axis='both', direction='out', length=6, width=2, labelsize=14)

# Agregar la letra "a" en la esquina superior derecha del primer subplot (ax1)
ax1.text(0.994, 0.955, '(a)', transform=ax1.transAxes, ha='right', va='top', fontsize=16, fontweight='bold')

# PARTE INFERIOR: Graficar el violín en el segundo subplot (ax2)
sns.violinplot(
    x='Etapa', y='Valor', hue='Año', data=df_melted, split=True, 
    palette='Dark2', width=0.7, linewidth=1.5, order=etapas_ordenadas, 
    scale='width', dodge=True, ax=ax2, cut=0
)

# Ajustes para el segundo subplot (ax2)
ax2.set_xlabel('')
ax2.set_ylabel('Coefficient of determination (R$^{2}$)', fontsize=14, fontweight='bold', labelpad=5)
ax2.set_ylim(0.0, 1.15)
ax2.grid(False)
ax2.tick_params(axis='both', direction='out', length=6, width=2, labelsize=14)
ax2.legend(title='Years', fontsize=12, title_fontsize=14, loc='upper center', 
    ncol=3)

# Agregar la letra "b" en la esquina superior derecha del segundo subplot (ax2)
ax2.text(0.994, 0.98, '(b)', transform=ax2.transAxes, ha='right', va='top', fontsize=16, fontweight='bold')

# Rotar las etiquetas del eje X
plt.xticks(rotation=45, ha='right', fontsize=14)

# Mostrar el gráfico y guardarlo
plt.tight_layout()
plt.savefig('Violin.png', dpi=600, bbox_inches='tight')
plt.show()