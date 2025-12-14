import streamlit as st
from utils.auth_check import check_login 
from utils.data_processing import calculate_trade_accuracy

# -------------------------------
# ⚙️ Configuração da página
# -------------------------------
st.set_page_config(
    page_title="Análise de Trade | Trade Robo",
    page_icon="🎲",
    layout="wide"
)
st.sidebar.markdown('Desenvolvido por [AntonioJrSales](https://antoniojrsales.github.io/meu_portfolio/)')

st.title("🎲 Tabelas de Análise de Trade")

# Se não estiver logado, ele para a execução aqui.
check_login() 

# 2. Acesso aos dados da sessão
if 'df_trade_robo' in st.session_state:
    df_dados = st.session_state['df_trade_robo']
    
else:
    st.error("Dados não encontrados na sessão. Por favor, volte para o login.")

aba1, aba2 = st.tabs(['Dados Brutos', 'Eficiência / Assertividade']) 

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

with aba2:
    df_acertividade = calculate_trade_accuracy(df_dados)

    if not df_acertividade.empty:
    
        # 1. CÁLCULO DA TAXA DE ACERTO GLOBAL
        # A Taxa Global é a média da coluna 'Acerto' de todo o df.
        taxa_acerto_global = df_dados['is_win'].mean() * 100
        
        st.markdown("---")
        st.header("📈 Eficiência dos Trades")
        
        col1, col2 = st.columns([1, 2])
        
        # CARD 4: Taxa de Acerto Global (no primeiro painel)
        with col1:
            st.metric(
                label="🏆 Taxa de Acerto Global",
                value=f"{taxa_acerto_global:.2f}%",
                delta="Média de WINs / Trades Válidos"
            )
            
        # 2. TABELA DE ASSERTIVIDADE POR ESTRATÉGIA
        with col2:
            st.subheader("Assertividade por Estratégia")
            st.dataframe(df_acertividade, use_container_width=True)

    else:
        st.warning("Não foi possível calcular a assertividade. Verifique se as colunas 'Resultado' e 'Estratégia' estão disponíveis.")