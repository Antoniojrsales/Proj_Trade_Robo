import pandas as pd
import streamlit as st
from utils.data_processing import render_card
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
