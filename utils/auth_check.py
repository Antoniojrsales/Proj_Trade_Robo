import streamlit as st
import hashlib

# -------------------------------------------------
# 🔐 Função para verificar se o usuário está logado
# -------------------------------------------------
def check_login():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("🔒 Você precisa estar logado para acessar esta página.")
        st.info("Por favor, volte para a [página de login](/)")
        st.stop()

# -------------------------------
# 🔐 Função para verificar senha
# -------------------------------
def check_password(input_password, stored_password_hash):
    """
    Compara a senha de entrada (após hash SHA256) com o hash armazenado.
    """
    # 1. Validação Simples: Garante que os argumentos são strings
    if not isinstance(input_password, str) or not isinstance(stored_password_hash, str):
        # Logar um erro interno aqui seria bom, mas para o usuário, apenas falha
        return False
        
    try:
        # Codifica e aplica o hash na senha de entrada
        input_hash = hashlib.sha256(input_password.encode('utf-8')).hexdigest()
        
        # Compara
        return input_hash == stored_password_hash
    
    except Exception as e:
        # Se ocorrer um erro durante o hashing (ex: erro de codificação), falha o login
        # st.exception(e) # Não mostrar ao usuário, mas útil para debug
        return False