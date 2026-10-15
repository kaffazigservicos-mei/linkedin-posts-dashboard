import pandas as pd
import os
import re
import nltk
from datetime import datetime
import locale 
import re # Necessário para a Regex

# ==========================================================
# DEFINIÇÃO DE PASTAS E ARQUIVOS
# ==========================================================
BASE_FOLDER_NAME = "LinkedInposts"
CSV_INPUT_FILE = "posts_buffer_texto_data1.csv"
CSV_OUTPUT_FILE = "posts_curadoria_filtrada_FINAL_ANO_LINK.csv"

# ==========================================================
# FUNÇÃO PRINCIPAL DE FILTRAGEM
# ==========================================================

def filtrar_e_exportar_curadoria():
    
    CSV_PATH_CURRENT = CSV_INPUT_FILE
    
    if os.path.exists(CSV_PATH_CURRENT):
        csv_final_path = CSV_PATH_CURRENT
    else:
        print("-" * 60)
        print(f"❌ ERRO: O arquivo de dados '{CSV_INPUT_FILE}' não foi encontrado.")
        return

    try:
        df = pd.read_csv(csv_final_path, delimiter=";", encoding='latin-1')
        print(f"✅ Carregados {len(df)} registros do arquivo: {csv_final_path}")
    except Exception as e:
        print(f"❌ ERRO ao carregar o CSV. Verifique o delimitador ou o encoding: {e}")
        return

    # --- Limpa Nomes das Colunas ---
    df.columns = df.columns.str.strip()
    
    # -------------------------------------------------------------
    # DIAGNÓSTICO E SELEÇÃO DAS COLUNAS ESSENCIAIS
    # -------------------------------------------------------------
    
    print("\n----------------------------------------------------------------------")
    print("👉 Por favor, selecione os números das colunas corretas na lista:")
    
    colunas_validas = df.columns.tolist()
    coluna_map = {i: colunas_validas[i] for i in range(len(colunas_validas))}
    
    for i, col_name in coluna_map.items():
        print(f"[{i}]: {col_name}")
        
    try:
        # Seleção da Coluna de Data Original (para formatação de Mês/Dia)
        data_idx = int(input("Digite o número da coluna que contém a DATA original (Ex: 0): "))
        COLUNA_DATA = coluna_map[data_idx]
        print(f"✅ Coluna de data original: '{COLUNA_DATA}'")
        
        # Seleção da Coluna de Link (para extração do Ano)
        link_idx = int(input("Digite o número da coluna que contém o LINK (Geralmente 'Link'): "))
        COLUNA_LINK = coluna_map[link_idx]
        print(f"✅ Coluna de link: '{COLUNA_LINK}'")
        
    except (ValueError, KeyError):
        print("❌ Seleção inválida. Encerrando o script.")
        return

    # -------------------------------------------------------------
    # ETAPA 1: EXTRAÇÃO DO ANO DO LINK E FORMATAÇÃO DA DATA
    # -------------------------------------------------------------
    
    # 1. Tenta extrair o ano (2020 a 2029) da string do link usando Regex
    def extrair_ano_do_link(link_str):
        if pd.isna(link_str) or not isinstance(link_str, str):
            return None
        # Procura por um ano de 4 dígitos começando com 202x
        match = re.search(r'(202[0-9])', link_str)
        return match.group(1) if match else None

    # Aplica a extração
    df['Ano'] = df[COLUNA_LINK].apply(extrair_ano_do_link).fillna('Sem Ano')
    
    # 2. Formatação da Data Original (Mês/Dia/Hora)
    # Tenta definir o locale para Inglês para reconhecer 'Oct', 'Jul', etc.
    try:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    except locale.Error:
        pass

    def parse_data_limpa(date_str):
        if pd.isna(date_str) or not isinstance(date_str, str):
            return "Data Inválida"
        
        # Formato exato do Buffer: 'Oct 14, 8:00 AM'
        try:
            dt_parcial = datetime.strptime(date_str, '%b %d, %I:%M %p')
            # Retorna a data limpa no formato MM/DD HH:MM
            return dt_parcial.strftime('%m/%d %I:%M %p')
        except:
            return date_str

    df['Data Formatada'] = df[COLUNA_DATA].apply(parse_data_limpa)
    
    print(f"\n✅ Anos extraídos dos links. 'Sem Ano' indica que o ano não foi encontrado no URL.")

    # -------------------------------------------------------------
    # ETAPA 2: SOLICITAR PALAVRA-CHAVE E FILTRAR
    # -------------------------------------------------------------
    
    print("\n----------------------------------------------------------------------")
    print("👉 DIGITE o(s) termo(s). Use o hífen (-) para EXCLUIR uma palavra.")
    palavra_chave_bruta = input("   Ex: 'riscos -gestão': ").strip()
    print("----------------------------------------------------------------------")
    
    if not palavra_chave_bruta:
        print("❌ Palavra-chave não informada. Encerrando o filtro.")
        return

    # Lógica de filtro (Inclusão/Exclusão)
    termos_incluir = [t.strip() for t in palavra_chave_bruta.split() if not t.startswith('-')]
    termos_excluir = [t.strip()[1:] for t in palavra_chave_bruta.split() if t.startswith('-')]

    if not termos_incluir:
        print("❌ Nenhum termo de INCLUSÃO ('riscos') foi especificado.")
        return
        
    filtro_posts = df.copy()
    for termo in termos_incluir:
        filtro_posts = filtro_posts[filtro_posts['Texto'].str.contains(termo, case=False, na=False)]
        
    for termo in termos_excluir:
        filtro_posts = filtro_posts[~filtro_posts['Texto'].str.contains(termo, case=False, na=False)]

    if filtro_posts.empty:
        print(f"\n❌ Nenhum post encontrado com o filtro aplicado: '{palavra_chave_bruta}'")
        return
        
    print(f"\n🎉 Filtrados {len(filtro_posts)} posts com o filtro '{palavra_chave_bruta}'.")
    
    # -------------------------------------------------------------
    # ETAPA 3: EXPORTAR O ARQUIVO DE CURADORIA FINAL
    # -------------------------------------------------------------
    
    df_curadoria = filtro_posts[[
        'Data Formatada', 
        'Ano', 
        'Texto', 
        'Link'
    ]].copy()
    
    output_path = os.path.join(os.path.dirname(csv_final_path), CSV_OUTPUT_FILE)

    try:
        df_curadoria.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')
        print("-" * 60)
        print(f"✅ Curadoria exportada com sucesso para: {output_path}")
        print(f"👉 O arquivo contém o ano extraído do Link ou 'Sem Ano'.")
        print("-" * 60)
    except PermissionError:
        print(f"❌ Erro de Permissão: Feche o arquivo '{CSV_OUTPUT_FILE}' e tente novamente.")

# ==========================================================
# EXECUÇÃO PRINCIPAL
# ==========================================================
if __name__ == '__main__':
    filtrar_e_exportar_curadoria()