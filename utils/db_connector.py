import pandas as pd
import streamlit as st

#-- 🗂️Acessa as credenciais do secrets.toml --#
try:
    SHEET_ID = st.secrets["SHEET"]["sheet_id"]
except Exception as e:
    st.error("Erro de configuração: 'sheet_id' não encontrado no [SHEET] do secrets.toml.")
    SHEET_ID = None

# Função para buscar e cachear os dados
@st.cache_data(ttl=600)  # TTL (Time to Live) para recarregar a cada 10 minutos
def load_data(sheet_id: str):
    if not sheet_id:
        st.warning("ID da planilha não fornecido. Retornando DataFrame vazio.")
        return pd.DataFrame()
    
    try:
        # Construir a URL de exportação pública do CSV
        url = (
            f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        )

        df = pd.read_csv(url, sep=',')
        return df

    except Exception as e:
        # st.exception(e) # Exibe o erro completo no Streamlit
        st.error(f"Erro ao ler o Google Sheet via CSV: Verifique se o Sheet está 'Publicado na Web' e se o separador ('sep') está correto. Erro: {e}")
        return pd.DataFrame()
