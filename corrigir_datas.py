# corrigir_datas.py — Corrige os anos no CSV existente instantaneamente
# Caminho: C:\Users\dilma\Documents\Linkedinposts\corrigir_datas.py

import csv
import os
from datetime import datetime

PASTA = r"C:\Users\dilma\Documents\Linkedinposts"
CSV_PATH = os.path.join(PASTA, "posts_com_pilares.csv")

def main():
    print("=" * 70)
    print("⚡ Correção Instantânea de Datas no CSV")
    print("=" * 70)

    if not os.path.exists(CSV_PATH):
        print(f"\n❌ ERRO: {CSV_PATH} não encontrado.")
        input("\nPressione ENTER para sair...")
        return

    posts = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            posts.append(row)

    print(f"\n📂 {len(posts)} posts carregados do CSV.")

    # Lógica de inferência de ano (Posts ordenados do mais recente para o mais antigo)
    ano_corrente = 2026  # Ano do post mais recente (topo da lista)
    mes_anterior = None
    novas_datas = []
    erros = 0

    for p in posts:
        data_str = p.get("Data", "").strip()
        try:
            dt = datetime.strptime(data_str, "%d/%m/%Y")
            mes_atual = dt.month
            dia = dt.day
            
            # CORREÇÃO: Se o mês aumentou, voltamos no tempo (ano anterior)
            if mes_anterior is not None and mes_atual > mes_anterior:
                ano_corrente -= 1
            
            nova_data = f"{dia:02d}/{mes_atual:02d}/{ano_corrente}"
            novas_datas.append(nova_data)
            mes_anterior = mes_atual
        except Exception:
            novas_datas.append(data_str)
            erros += 1

    # Atualiza o dicionário e salva
    for i, p in enumerate(posts):
        p["Data"] = novas_datas[i]

    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = posts[0].keys() if posts else []
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(posts)

    print(f"\n✅ Datas corrigidas e salvas com sucesso!")
    print(f" Data do primeiro post (mais recente): {novas_datas[0]}")
    print(f"📅 Data do último post (mais antigo): {novas_datas[-1]}")
    if erros > 0:
        print(f"⚠️ {erros} datas não puderam ser processadas e foram mantidas originais.")
    
    print(f"\n💡 Agora regenere o dashboard: python gerar_dashboard_conteudo.py")
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n💥 ERRO: {type(e).__name__}: {e}")
        input("\nPressione ENTER para sair...")