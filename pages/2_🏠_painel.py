import pandas as pd
import streamlit as st
from utils.data_processing import render_card, calculate_trade_balance, calculate_trade_games
from utils.auth_check import check_login

# -------------------------------
# ⚙️ Configuração da página
# -------------------------------
st.set_page_config(
    page_title="Painel Geral | Trade Robo",
    page_icon="🏠",
    layout="wide"
)
st.sidebar.markdown('Desenvolvido por [AntonioJrSales](https://antoniojrsales.github.io/meu_portfolio/)')

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
        title='💰 Lucro Total:', 
        value=saldo,
         gradient= "#727272, #474747",
         prefix='R$' 
)
    
with col2:
    render_card(
        title='⬆️ Ganho Total:', 
        value=ganhos,
         gradient= "#727272, #474747",
         prefix='R$' 
)
    
with col3:
    render_card(
        title='⬇️ Perda Total:', 
        value=perdas_abs,
         gradient= "#727272, #474747",
         prefix='R$' 
)
    
col4, col5, col6 = st.columns([2, 2, 2])

total_jogos = calculate_trade_games(df_dados)
with col4:
    render_card(
        title='🪙 Total Apostas Finalizadas:', 
        value=total_jogos,
         gradient= "#727272, #474747",
         prefix=None 
)
    
# A Taxa Global é a média da coluna 'Acerto' de todo o df.
taxa_acerto_global = df_dados['is_win'].mean() * 100

with col5:
    render_card(
        title='🏆 Taxa de Acerto Global:', 
        value=taxa_acerto_global,
         gradient= "#727272, #474747",
         prefix='%' 
)
