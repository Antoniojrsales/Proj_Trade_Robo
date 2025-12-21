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

st.subheader('🏦 - Banca')
colbanca, colbanca2, colbanca3 = st.columns([1, 1, 1])
with colbanca:
    render_card(
        title='💰 Banca Atual:', 
        value=0,
        gradient= "#727272, #474747",
        prefix='R$' 
)
    
with colbanca2:
    render_card(
        title='💵 Meta Diária:', 
        value=0,
        gradient= "#727272, #474747",
        prefix='R$' 
)

with colbanca3:
    render_card(
        title='💵 Meta Mensal:', 
        value=0,
        gradient= "#727272, #474747",
        prefix='R$' 
)

st.subheader('❤️ - Saúde Financeira')
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
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
    
with col4:
    render_card(
        title='📊 ROI Global:', 
        value=2.5,
        gradient= "#727272, #474747",
        prefix='%'
)

st.subheader('🏆 - Operacional e Assertividade')    
col5, col6, col7, col8 = st.columns([2, 2, 2, 2])    
# A Taxa Global é a média da coluna 'Acerto' de todo o df.
taxa_acerto_global = df_dados['is_win'].mean() * 100
with col5:
    render_card(
        title='🏆 Taxa de Acerto Global:', 
        value=taxa_acerto_global,
         gradient= "#727272, #474747",
         prefix='%' 
)

with col6:
    render_card(
        title='✅ Taxa de Win (%):', 
        value=98,
        gradient= "#727272, #474747",
        prefix='%' 
)

total_jogos = calculate_trade_games(df_dados)
with col7:
    render_card(
        title='💪 Melhor Estratégia:', 
        value='Under 1.5FT',
         gradient= "#727272, #474747",
         prefix=None 
)
    
with col8:
    render_card(
        title='⚖️ Odd Média:', 
        value=1.5,
        gradient= "#727272, #474747",
        prefix='R$' 
)

st.subheader('🛡️ - Estratégia e Controle de Risco')    
col9, col10, col11, col12 = st.columns([3, 3, 3, 3])  
total_jogos = calculate_trade_games(df_dados)
with col9:
    render_card(
        title='🪙 Total Apostas Finalizadas:', 
        value=total_jogos,
         gradient= "#727272, #474747",
         prefix=None 
)
    
with col10:
    render_card(
        title='💸 Volume Total (Giro):', 
        value=2000,
         gradient= "#727272, #474747",
         prefix='R$' 
)

with col11:
    render_card(
        title='📉 Drawdown Máximo:', 
        value=200,
         gradient= "#727272, #474747",
         prefix='R$' 
)
    
with col12:
    render_card(
        title='📈 Profit Factor:', 
        value=1.3,
         gradient= "#727272, #474747",
         prefix='R$' 
)