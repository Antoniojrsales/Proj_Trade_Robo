import streamlit as st
from utils.auth_check import check_login 
# ... (outras importações)

# 1. Guardrail (Verifica se está logado)
# Se não estiver logado, ele para a execução aqui.
check_login() 

st.title("📊 Tabelas de Análise de Trade")

# 2. Acesso aos dados da sessão
if 'df_trade_robo' in st.session_state:
    df_dados = st.session_state['df_trade_robo']
    
else:
    st.error("Dados não encontrados na sessão. Por favor, volte para o login.")

aba1, aba2 = st.tabs(['Dados Brutos', 'Inserindo Dados na base']) 

with aba1:
    with st.sidebar.expander("🔍 Visualizar colunas"):
        options = st.multiselect('Escolha a Coluna:', df_dados.columns, default=list(df_dados.columns))

    options_dados = st.sidebar.radio('Escolha qual o filtro de visualização:',
                            ['Todos', 'Head', 'Tail'])

    if options:
        df_filtrado = df_dados[options]
        if options_dados == 'Todos':
            st.dataframe(df_filtrado)
        elif options_dados == 'Head':
            st.dataframe(df_filtrado.head(10))
        else:
            st.dataframe(df_filtrado.tail(10))
    else:
        st.write('Por favor, selecione ao menos uma coluna.')

    st.divider()
    st.markdown(f"O dataset possui :blue[{df_dados.shape[0]}] linhas e :blue[{df_dados.shape[1]}] colunas.")

    st.divider()