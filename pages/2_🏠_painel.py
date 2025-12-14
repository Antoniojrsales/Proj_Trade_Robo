import pandas as pd
import streamlit as st
from utils.data_processing import render_card, calculate_trade_balance
from utils.auth_check import check_login

# -------------------------------
# ⚙️ Configuração da página
# -------------------------------
st.set_page_config(
    page_title="Painel Geral | Trade Robo",
    page_icon="🏠",
    layout="wide"
)

st.title('🏠 Painel - Trade Robo')

check_login()

# 2. Acesso aos dados da sessão
if 'df_trade_robo' in st.session_state:
    df_dados = st.session_state['df_trade_robo']
    
else:
    st.error("Dados não encontrados na sessão. Por favor, volte para o login.")

# 2. Calcula as Métricas
metrics = calculate_trade_balance(df_dados)

saldo = metrics['saldo_total']
ganhos = metrics['total_ganhos']
perdas_abs = metrics['total_perdas_abs'] # Valor positivo para o card

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    render_card(
        title='💰 Saldo Total:', 
        value=saldo,
         gradient= "#FF8C00, #E91E63" 
)
    
with col2:
    render_card(
        title='⬆️ Total de Ganhos:', 
        value=ganhos,
         gradient= "#FF8C00, #E91E63" 
)
    
with col3:
    render_card(
        title='⬇️ Total de Perdas:', 
        value=perdas_abs,
         gradient= "#FF8C00, #E91E63" 
)