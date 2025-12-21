import pandas as pd
import streamlit as st
import numpy as np

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa, converte tipos e adiciona colunas analíticas ao DataFrame.
    """
    if df.empty:
        return df

    # --- 1. LIMPEZA E CONVERSÃO DE TIPOS ---
    
    # A. Coluna 'L/P' (Lucro/Prejuízo): Tratamento robusto (formato BR)
    if 'L/P' in df.columns:
        df['L/P'] = df['L/P'].astype(str).str.strip()
        
        # 1. Remove tudo que não é dígito, vírgula ou sinal de menos (para prejuízo)
        df['L/P'] = df['L/P'].str.replace(r'[^\d,\-]', '', regex=True) 
        
        # 2. Troca vírgula decimal (BR) por ponto (Python/Float)
        df['L/P'] = df['L/P'].str.replace(',', '.', regex=False)

        # 3. Conversão segura para float
        df['L/P'] = pd.to_numeric(df['L/P'], errors='coerce')
    
    # B. Coluna 'Data da aposta': Conversão e Limpeza de Nulos
    '''if 'Data da aposta' in df.columns:
        df['Data da aposta'] = pd.to_datetime(df['Data da aposta'], format='%d/%m/%y', errors='coerce') 
        
        # 🛑 CORRIGIDO: Removido o inplace=True e o problema de reatribuição (df = None)
        df = df.dropna(subset=['Data da aposta'])
        
        # Cria uma coluna Mês/Ano (para análise de tendências)
        # 🛑 CORRIGIDO: Checa a coluna 'Data da aposta', não 'Data'
        df['Mes/Ano'] = df['Data da aposta'].dt.strftime('%b/%Y').astype('category') # Otimizado para 'category'''

    # C. Otimização de Tipo
    if 'Estratégia' in df.columns:
        df['Estratégia'] = df['Estratégia'].astype('category')


    # --- 2. COLUNAS ANALÍTICAS DE TRADE (Descomentar se necessário) ---
    # Se você precisa dessas colunas na análise, remova os comentários

    if 'L/P' in df.columns:
        # 1. Categoria de Resultado: WIN, LOSS ou PUSH/VOID
        df['Resultado'] = df['L/P'].apply(lambda x: 
            'WIN' if x > 0.001 else 
            ('LOSS' if x < -0.001 else 'PUSH/VOID')
        ).astype('category')
        
        # 2. Coluna Binária para Taxa de Acerto (para agregação)
        df['is_win'] = (df['Resultado'] == 'WIN').astype(int)

    # 3. Cálculo do ROI (Retorno sobre Investimento) - Requer a coluna 'Stake'
    if 'L/P' in df.columns and 'Stake' in df.columns:
        # Lembre-se que 'Stake' deve ser convertida para float antes deste ponto!
        df['ROI (%)'] = (
            (df['L/P'] / df['Stake']) * 100
        ).mask(df['Stake'] == 0, 0)
         
    return df.reset_index(drop=True)

def render_card(title, value, gradient, prefix, delta=None):
    # --- FORMATAÇÃO DOS VALORES ---
    if prefix == 'R$':
        valor_formatado = f"R$ {value:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
    elif prefix == '%':
        valor_formatado = f"{value:,.2f}".replace('.', ',') + "%"
    else:
        valor_formatado = f"{value}"

    # --- LÓGICA DO DELTA (Para remover o erro visual) ---
    delta_content = ""
    if delta is not None:
        cor_delta = "#00ff00" if delta >= 0 else "#ff4b4b"
        seta = "▲" if delta >= 0 else "▼"
        delta_content = f'<div style="margin-top:10px;color:{cor_delta};font-size:0.8em;">{seta} {abs(delta)}% vs anterior</div>'

    # --- ESTILIZAÇÃO DO CARD ---
    card_html = f"""
    <div style="background:linear-gradient(to right, {gradient});
                padding:20px;
                border-radius:15px;
                color:white;
                box-shadow:0 4px 10px rgba(0,0,0,0.3);
                min-height:100px;
                font-family: 'Segoe UI', sans-serif;
                margin-top:10px">
        <div style="font-size:1em;opacity:0.8;">{title}</div>
        <div style="font-size:1.7em;font-weight:bold;margin:5px 0;">{valor_formatado}</div>
        {delta_content}
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def calculate_trade_balance(df: pd.DataFrame) -> dict:
    """
    Calcula Lucros Totais, Perdas Totais e Saldo Acumulado (L/P).
    Assume que o DataFrame possui as colunas 'L/P' (float) e 'Resultado' (category/string).
    """
    if df.empty or 'L/P' not in df.columns or 'Resultado' not in df.columns:
        # Retorna zero se faltarem dados ou colunas
        return {
            "saldo_total": 0.0, 
            "total_ganhos": 0.0, 
            "total_perdas_abs": 0.0
        }

    # 1. Saldo Acumulado (Soma de toda a coluna L/P)
    saldo_total = df['L/P'].sum()

    # 2. Total de Ganhos (Soma dos L/P positivos)
    # 🛑 SINTAXE CORRIGIDA
    total_ganhos = df.loc[df['Resultado'] == 'WIN', 'L/P'].sum()

    # 3. Total de Perdas (Soma dos L/P negativos, pegando o valor absoluto para exibição)
    # 🛑 SINTAXE CORRIGIDA
    total_perdas_negativo = df.loc[df['Resultado'] == 'LOSS', 'L/P'].sum()
    total_perdas_abs = abs(total_perdas_negativo)

    return {
        "saldo_total": saldo_total, 
        "total_ganhos": total_ganhos, 
        "total_perdas_abs": total_perdas_abs
    }

def calculate_trade_accuracy(df: pd.DataFrame):
    """
    Calcula a Taxa de Acerto (Winning Rate) e Total de Trades por Estratégia.
    Assume que 'Resultado' e 'Estratégia' estão presentes.
    """
    
    required_cols = ['Resultado', 'Estratégia']
    if df.empty or not all(col in df.columns for col in required_cols):
        return pd.DataFrame() 
    
    # A coluna que possui 1 e 0 (is_win) é a que deve ser agregada.
    acertividade_por_estrategia = df.groupby('Estratégia').agg(
        # Use 'is_win' para calcular a média (assertividade)
        taxa_media=('is_win', 'mean'), 
        Total_Trades=('Estratégia', 'size') # Conta o número de trades
    ).reset_index()

    # O restante do seu script

    # Renomear a coluna para clareza
    acertividade_por_estrategia.rename(columns={'taxa_media': 'Assertividade (%)'}, inplace=True) 
    # Esta renomeação é redundante, mas inofensiva.

    # Converter para porcentagem
    acertividade_por_estrategia['Assertividade (%)'] = (
        acertividade_por_estrategia['Assertividade (%)'] * 100
    ).round(2)

    # Ordenar
    analise_final = acertividade_por_estrategia.sort_values(
        by='Assertividade (%)', 
        ascending=False
    )

    return analise_final

def calculate_trade_games(df: pd.DataFrame):
    # A. Verifica se a coluna Status existe e se o DataFrame não está vazio
    if 'Status' in df.columns and not df.empty:
        
        # B. Filtra somente as apostas finalizadas ('SETTLED') e usa .shape[0] para contar as linhas
        apostas_finalizadas_df = df.loc[df['Status'] == 'SETTLED']
        total_jogos_finalizados = apostas_finalizadas_df.shape[0] # <--- CORREÇÃO AQUI
        
    else:
        total_jogos_finalizados = 0

    return total_jogos_finalizados
