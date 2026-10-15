# parse_buffer_sent.py — CAMINHO CORRIGIDO: C:\Users\dilma\Documents\Linkedinposts
from bs4 import BeautifulSoup
import csv
import os
import re

# ===== CAMINHO CORRIGIDO =====
HTML_PATH = r"C:\Users\dilma\Documents\Linkedinposts\buffer_sent.html"
CSV_PATH = r"C:\Users\dilma\Documents\Linkedinposts\posts_buffer.csv"

DATA_REGEX = re.compile(
    r"([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4}"
    r"|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}"
    r"|\d{2}/\d{2}/\d{4})"
)

def detectar_rede(card):
    txt = card.get_text(" ", strip=True).lower()
    for rede in ["linkedin", "twitter", "facebook", "instagram"]:
        if rede in txt:
            return rede.title()
    return "Desconhecida"

def main():
    if not os.path.exists(HTML_PATH):
        print(f"❌ Arquivo não encontrado: {HTML_PATH}")
        print(f"   Pasta esperada: C:\\Users\\dilma\\Documents\\Linkedinposts")
        input("Pressione ENTER para sair...")
        return

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    print("✅ HTML carregado!")

    rows = []
    for card in soup.find_all(class_="publish_content_dM74X"):
        texto = card.get_text(" ", strip=True)
        if not texto:
            continue

        data = ""
        t = card.find("time")
        if t and t.get("datetime"):
            data = t["datetime"][:10]
        else:
            m = DATA_REGEX.search(texto)
            if m:
                data = m.group(1)

        rows.append({"Data": data, "Rede": detectar_rede(card), "Texto": texto})

    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["Data", "Rede", "Texto"], delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ {len(rows)} posts exportados para {CSV_PATH}")

if __name__ == "__main__":
    main()
    input("Pressione ENTER para sair...")