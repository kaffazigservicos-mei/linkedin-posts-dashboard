# corrigir_indentacao.py - Corrige automaticamente a indentação dos input()
import os
import re

PASTA = r"C:\Users\dilma\Documents\Linkedinposts"

def corrigir_arquivo(nome_arquivo):
    caminho = os.path.join(PASTA, nome_arquivo)
    if not os.path.exists(caminho):
        print(f"[ERRO] {nome_arquivo} nao encontrado.")
        return False
    
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    
    linhas_corrigidas = []
    alteracoes = 0
    
    for i, linha in enumerate(linhas):
        # Detecta linha com "if sys.stdin.isatty():"
        if "if sys.stdin.isatty():" in linha:
            linhas_corrigidas.append(linha)
            # Verifica a próxima linha
            if i + 1 < len(linhas):
                proxima = linhas[i + 1]
                # Se a próxima linha tem input() mas não está indentada após o if
                if "input(" in proxima and not proxima.startswith("    "):
                    # Adiciona 4 espaços de indentação
                    linhas_corrigidas.append("    " + proxima.lstrip())
                    alteracoes += 1
                    print(f"  -> Corrigida linha {i+2} em {nome_arquivo}")
                else:
                    linhas_corrigidas.append(proxima)
            # Pula a próxima linha pois já foi processada
            continue
        else:
            linhas_corrigidas.append(linha)
    
    if alteracoes > 0:
        with open(caminho, "w", encoding="utf-8") as f:
            f.writelines(linhas_corrigidas)
        print(f"[OK] {nome_arquivo}: {alteracoes} correcao(oes) aplicada(s).")
        return True
    else:
        print(f"[INFO] {nome_arquivo} ja esta correto.")
        return True

print("=" * 60)
print("CORREÇÃO AUTOMÁTICA DE INDENTAÇÃO")
print("=" * 60)
corrigir_arquivo("buffer_export1.py")
corrigir_arquivo("classificar_pilares.py")
print("=" * 60)
print("CORREÇÃO CONCLUÍDA.")
print("=" * 60)