import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Inversión Recurrente", layout='wide')
st.title("Simulador de Inversión Recurrente en Índices")

# --- Entradas de usuario ---
indices = {
    'S&P 500 (ETF SPY)': 'SPY',
    'S&P 500 (Índice)': '^GSPC',
    'MSCI World (ETF URTH)': 'URTH',
    'MSCI Japan (ETF EWJ)': 'EWJ',
    'Nikkei 225 (Índice)': '^N225',
    'Emerging Markets (ETF EEM)': 'EEM',
    'Europe (ETF VGK)': 'VGK'
}
selected = st.selectbox("Selecciona un índice/fondo", list(indices.keys()))
symbol = indices[selected]

col1, col2 = st.columns(2)
with col1:
    start_year = st.number_input("Año de inicio", min_value=1900, max_value=2025, value=2000)
    end_year = st.number_input("Año de fin", min_value=1900, max_value=2025, value=2024)
with col2:
    initial = st.number_input("Cantidad inicial (€)", min_value=0.0, value=1000.0, step=100.0)
    monthly = st.number_input("Cantidad mensual (€)", min_value=0.0, value=100.0, step=10.0)

if start_year >= end_year:
    st.error("El año de inicio debe ser menor que el año de fin.")
    st.stop()

# --- Obtención de datos históricos ---
start_date = f"{start_year}-01-01"
end_date = f"{end_year}-12-31"

data = yf.download(symbol, start=start_date, end=end_date, progress=False, interval='1mo')
if data.empty:
    st.error("No se han encontrado datos para el índice/fondo seleccionado en el periodo indicado.")
    st.stop()

# --- Determinar columna de precio de cierre ajustado ---
if 'Adj Close' in data.columns:
    price_col = 'Adj Close'
elif 'Adj_Close' in data.columns:
    price_col = 'Adj_Close'
else:
    price_col = 'Close'

# Calcular rentabilidades mensuales
data['Monthly Return'] = data[price_col].pct_change()

# --- Simulación de la inversión ---
years = list(range(start_year, end_year + 1))
results = pd.DataFrame(index=years, columns=['Contribución', 'Intereses', 'Valor final'], dtype=float)

balance = initial
initial_investment = initial
for year in years:
    df_year = data[data.index.year == year]
    contrib_this_year = monthly * 12
    interest_year = 0.0
    for ret in df_year['Monthly Return'].fillna(0):
        balance += monthly
        growth = balance * ret
        balance += growth
        interest_year += growth
    results.at[year, 'Contribución'] = contrib_this_year + (initial_investment if year == start_year else 0)
    results.at[year, 'Intereses'] = interest_year
    results.at[year, 'Valor final'] = balance
    initial_investment = 0.0

# Calcular valores acumulados
tot_contrib = results['Contribución'].cumsum()
tot_interes = results['Intereses'].cumsum()

# --- Visualización ---
fig, ax = plt.subplots(figsize=(10, 6))
# Barras acumulativas
ax.bar(results.index, tot_contrib, label='Aportado')
ax.bar(results.index, tot_interes, bottom=tot_contrib, label='Interés')
ax.set_xlabel('Año')
ax.set_ylabel('Euros acumulados')
ax.set_title(f'Inversión Recurrente Acumulada en {selected} ({start_year}-{end_year})')

# Línea de evolución del índice (normalizada)
ax2 = ax.twinx()
serie_index = data[price_col].resample('Y').last()
serie_index_norm = serie_index / serie_index.iloc[0] * results['Valor final'].iloc[0]
ax2.plot([d.year for d in serie_index_norm.index], serie_index_norm.values,
         linestyle='--', label='Índice', color='red')
ax2.set_ylabel('Valor índice normalizado')

# Ajustar límites dinámicos
ax.set_xlim(years[0] - 0.5, years[-1] + 0.5)
max_accum = float((tot_contrib + tot_interes).max())
ax.set_ylim(0, max_accum * 1.1)
idx_vals = serie_index_norm.values
min_idx = float(np.nanmin(idx_vals))
max_idx = float(np.nanmax(idx_vals))
ax2.set_ylim(min_idx * 0.9, max_idx * 1.1)

# Leyenda
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
legend = ax.legend(h1 + h2, l1 + l2, loc='upper left', bbox_to_anchor=(0.05, 0.95), borderaxespad=0.)

# Cálculo del % de interés recibido
total_contrib_total = tot_contrib.iloc[-1]
total_interest_total = tot_interes.iloc[-1]
percent_interest = (total_interest_total / total_contrib_total) * 100
textstr = f"% Interés: {percent_interest:.2f}%"
props = dict(boxstyle='round', facecolor='white', alpha=0.8)
# Añadir caja de texto a la derecha de la leyenda
ax.text(0.35, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

fig.tight_layout()
st.pyplot(fig)

# --- Tabla de resultados ---
st.subheader("Detalle anual")
st.dataframe(results.style.format("{:.2f}"))
