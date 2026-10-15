# analise_completa1.py — CAMINHO CORRIGIDO: C:\Users\dilma\Documents\Linkedinposts
import os
import re
import csv
import unicodedata

# ===== CAMINHO CORRIGIDO =====
PASTA = r"C:\Users\dilma\Documents\Linkedinposts"
ARQUIVO_ORIGEM = os.path.join(PASTA, "posts_buffer_texto_data1.csv")

def remover_acentos(texto):
    if not texto:
        return ""
    return "".join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    ).lower()

def executar_analise():
    if not os.path.exists(ARQUIVO_ORIGEM):
        print(f"❌ ERRO: '{ARQUIVO_ORIGEM}' não encontrado.")
        print(f"   Pasta esperada: {PASTA}")
        input("Pressione ENTER para fechar...")
        return

    # Carrega posts usando csv.DictReader (robusto, não quebra com ; no texto)
    posts = []
    with open(ARQUIVO_ORIGEM, 'r', encoding='utf-8-sig') as f:
        sample = f.read(4096)
        f.seek(0)
        delim = ";" if sample.count(";") > sample.count(",") else ","
        reader = csv.DictReader(f, delimiter=delim)
        for row in reader:
            posts.append(row)

    print(f"✅ {len(posts)} posts carregados de {ARQUIVO_ORIGEM}")
    print("📢 Digite 'SAIR' para encerrar.")

    while True:
        print("\n" + "=" * 50)
        palavra_alvo = input("👉 Pesquisar: ").strip()
        if palavra_alvo.upper() == 'SAIR':
            print("👋 Até logo!")
            break
        if not palavra_alvo:
            continue

        termo = remover_acentos(palavra_alvo)
        encontrados = []
        for p in posts:
            blob = remover_acentos(" ".join(str(v) for v in p.values()))
            if termo in blob:
                encontrados.append(p)

        if encontrados:
            print(f"🎯 {len(encontrados)} posts com '{palavra_alvo}'.")
            nome = re.sub(r'[^\w\s-]', '', palavra_alvo).strip().replace(" ", "_")
            out = os.path.join(PASTA, f"posts_filtrados_{nome}.csv")
            with open(out, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=["Data", "Texto", "Link"], delimiter=";")
                w.writeheader()
                w.writerows(encontrados)
            print(f"💾 Salvo: {out}")
            print(f"📝 Amostra: {encontrados[0].get('Texto', '')[:200]}...")
        else:
            print(f"❌ Nada encontrado para '{palavra_alvo}'.")

if __name__ == "__main__":
    executar_analise()