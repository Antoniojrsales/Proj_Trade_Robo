import pandas as pd

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
        
        # Remove linhas sem data válida
        df = df.dropna(subset=['Data da aposta'])
        
        # Cria a coluna Mês/Ano
        df['Mes/Ano'] = df['Data da aposta'].dt.strftime('%b/%Y').astype('category')

    # C. Otimização de Tipo (Ex: Categoria de Mercado)
    if 'Estratégia' in df.columns:
        df['Estratégia'] = df['Estratégia'].astype('category')


    # --- 2. COLUNAS ANALÍTICAS DE TRADE ---

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
         # *IMPORTANTE: Assuma que a coluna Stake também foi limpa e convertida para float*
         # ...
         df['ROI (%)'] = (
             (df['L/P'] / df['Stake']) * 100
         ).mask(df['Stake'] == 0, 0)'''
         
    return df.reset_index(drop=True)