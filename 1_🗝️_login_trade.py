#-- Bibliotecas --#
import streamlit as st
from utils.auth_check import check_password 
from utils.db_connector import load_data 
from utils.data_processing import process_data 

# -------------------------------
# ⚙️ Configuração da página
# -------------------------------
st.set_page_config(page_title="Login | Trade Robo", 
                   page_icon="🔐", 
                   layout="centered")

st.sidebar.markdown('Desenvolvido por [AntonioJrSales](https://antoniojrsales.github.io/meu_portfolio/)')

# -------------------------------
# 🎨 Estilo CSS personalizado (Mantido)
# -------------------------------
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5em 1em;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 🗂️ Carregar Credenciais de Usuário
# -------------------------------
try:
    USERS = st.secrets["AUTH_USERS"]
    SHEET_ID = st.secrets["SHEET"]["sheet_id"] 
except KeyError as e:
    st.error(f"Erro de configuração: Chave '{e.args[0]}' ausente em secrets.toml.")
    st.stop()

# -------------------------------
# 🖼️ FUNÇÃO PRINCIPAL DO PAINEL PÓS-LOGIN (Onde o usuário vai após login)
# -------------------------------
def render_main_page():
    """Exibe o conteúdo da página após o login bem-sucedido."""
    
    st.title(f"🎉 Bem-vindo(a), {st.session_state.get('username', 'Usuário')}!")
    st.header("📈 Dados Carregados")
    
    # Botão de Logout para sair da sessão
    if st.button("🚪 Logout", type="secondary"):
        del st.session_state['logged_in']
        del st.session_state['username']
        st.rerun() 
        return

    try:
        # Carregamento e processamento dos dados
        df_bruto = load_data(SHEET_ID) 
        
        if not df_bruto.empty:
            df_dados = process_data(df_bruto)
            
            st.success("Dados da Planilha carregados e processados com sucesso!")
            
            st.markdown("---")
            #st.session_state['logged_in'] = True
            st.session_state['df_trade_robo'] = df_dados 

        else:
            st.warning("⚠️ Planilha acessada, mas está vazia após o processamento.")
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar/processar dados: {e}")
        # st.exception(e) # Comentado, mas útil para debug

# -------------------------------
# 🎨 Formulário de Login (Gatekeeper)
# -------------------------------
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    with st.form("login_form"):
        st.markdown("<h1 style='text-align: center;'>🔐 Login</h1>", unsafe_allow_html=True)
        st.divider()

        username = st.text_input("👤 Usuário").strip()
        password = st.text_input("🔒 Senha", type="password").strip()

        submit = st.form_submit_button("Entrar", type="primary")
        
        if submit: 
            if username in USERS and check_password(password, USERS[username]):
                
                st.session_state['logged_in'] = True
                st.session_state['username'] = username 

                st.toast("✅ Login bem-sucedido!", icon='🎉')
                
                st.rerun() # Recarrega a página para acionar o render_main_page()
                
            else:
                st.error("❌ Usuário ou senha inválidos.")
else:
    # 🚦 Se o usuário JÁ estiver logado (após o rerun)
    render_main_page()