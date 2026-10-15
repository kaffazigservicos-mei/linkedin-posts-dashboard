# buffer_export1.py — VERSÃO FINAL BLINDADA (Compatível com Automação)
# Caminho: C:\Users\dilma\Documents\Linkedinposts\buffer_export1.py

import os
import sys
import time
import csv
import re
from datetime import datetime

print("[0/8] Importando Selenium...", flush=True)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("[1/8] Configurando variáveis...", flush=True)
BASE_FOLDER = r"C:\Users\dilma\Documents\Linkedinposts"
CSV_PATH = os.path.join(BASE_FOLDER, "posts_buffer_texto_data1.csv")
TIMEOUT = 60
MAX_SCROLLS = 1000
MAX_REPEATS = 60
TARGET_COUNT = 800
os.makedirs(BASE_FOLDER, exist_ok=True)

MESES = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'june': 6, 'july': 7, 'august': 8, 'september': 9,
    'october': 10, 'november': 11, 'december': 12
}

print("[2/8] Criando ChromeDriver...", flush=True)
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1280,2000")

try:
    driver = webdriver.Chrome(options=options)
    print("[2/8] ChromeDriver criado com sucesso.", flush=True)
except Exception as e:
    print(f"[ERRO] Falha ao criar ChromeDriver: {e}", flush=True)
    print("[DICA] Verifique se o Chrome está instalado e atualizado.", flush=True)
    if sys.stdin.isatty():
        input("Pressione ENTER para sair...")
    sys.exit(1)

driver.set_page_load_timeout(TIMEOUT)
driver.set_script_timeout(TIMEOUT)
driver.implicitly_wait(10)

print("[3/8] Abrindo Buffer...", flush=True)
try:
    driver.get("https://buffer.com/app/posts/sent")
    print("[3/8] Página carregada. Aguardando 15s...", flush=True)
    time.sleep(15)
except Exception as e:
    print(f"[ERRO] Falha ao carregar página: {e}", flush=True)
    driver.quit()
    if sys.stdin.isatty():
        input("Pressione ENTER para sair...")
    sys.exit(1)

print("[4/8] Verificando sessão...", flush=True)
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//article"))
    )
    print("[4/8] Sessão válida, posts visíveis.", flush=True)
except Exception:
    print("[4/8] Sessão não válida. Login necessário.", flush=True)
    print("[INFO] Faça login no Buffer no navegador que abriu.", flush=True)
    
    # PROTEÇÃO: Só pede input se houver terminal interativo
    if sys.stdin.isatty():
        link = input("Cole o link de confirmação e pressione ENTER: ").strip()
        if not link.startswith("http"):
            print("[ERRO] URL inválida.", flush=True)
            driver.quit()
            input("Pressione ENTER para sair...")
            sys.exit(1)
        driver.get(link)
        time.sleep(20)
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//article"))
            )
            print("[4/8] Login concluído.", flush=True)
        except Exception:
            print("[ERRO] Não foi possível localizar posts após login.", flush=True)
            driver.quit()
            input("Pressione ENTER para sair...")
            sys.exit(1)
    else:
        # Modo automático: não pode pedir login, então encerra graciosamente
        print("[AVISO] Sessão expirada e sem terminal para login manual.", flush=True)
        print("[DICA] Execute 'python buffer_export1.py' manualmente para renovar a sessão.", flush=True)
        driver.quit()
        sys.exit(1)

print("[5/8] Scroll para carregar posts...", flush=True)
last_count = 0
same_count_repeats = 0
for i in range(1, MAX_SCROLLS + 1):
    posts = driver.find_elements(By.XPATH, "//article")
    if posts:
        driver.execute_script("arguments[0].scrollIntoView(true);", posts[-1])
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(1.5)
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.5)
    
    posts = driver.find_elements(By.XPATH, "//article")
    new_count = len(posts)
    
    if i % 10 == 0 or new_count != last_count:
        print(f"[5/8] Scroll {i} -> {new_count} posts", flush=True)
        
    if new_count >= TARGET_COUNT:
        print(f"[5/8] Alvo atingido ({new_count} posts).", flush=True)
        break
        
    if new_count == last_count:
        same_count_repeats += 1
        if same_count_repeats >= MAX_REPEATS:
            print(f"[5/8] Fim do scroll - {new_count} posts.", flush=True)
            break
    else:
        same_count_repeats = 0
    last_count = new_count

if last_count == 0:
    print("[ERRO] Nenhum post encontrado.", flush=True)
    driver.quit()
    if sys.stdin.isatty():
        input("Pressione ENTER para sair...")
    sys.exit(1)

print(f"[6/8] Expandindo 'See more'...", flush=True)
for tentativa in range(1, 10):
    botoes = driver.find_elements(By.XPATH,
        "//button[contains(translate(text(), 'SEEMORE', 'seemore'), 'see more') "
        "or contains(translate(text(), 'VERMAIS', 'vermais'), 'ver mais')]")
    if not botoes:
        print(f"[6/8] Sem botões na tentativa {tentativa}.", flush=True)
        break
    print(f"[6/8] {len(botoes)} botões - tentativa {tentativa}", flush=True)
    for botao in botoes:
        try:
            driver.execute_script("arguments[0].click();", botao)
        except Exception:
            pass
    time.sleep(2)
    if len(botoes) < 5:
        break
    time.sleep(3)

print("[7/8] Extraindo dados...", flush=True)
driver.execute_script("""
document.querySelectorAll('article p, article span, article div').forEach(el => {
    el.style.maxHeight = 'none';
    el.style.overflow = 'visible';
});
""")
time.sleep(2)

js_code = """
const posts = document.querySelectorAll('article');
const resultados = [];
posts.forEach(post => {
    let texto = '';
    try { texto = (post.innerText || '').trim(); } catch(e) {}
    let aria_label = post.getAttribute('aria-label') || '';
    let link = '';
    const linkEl = post.querySelector('a[href*="linkedin.com"]');
    if (linkEl) link = linkEl.href || '';
    resultados.push({ texto: texto, aria_label: aria_label, link: link });
});
return resultados;
"""

try:
    dados_js = driver.execute_script(js_code)
    print(f"[7/8] Extração concluída: {len(dados_js)} posts.", flush=True)
except Exception as e:
    print(f"[ERRO] Falha na extração: {e}", flush=True)
    dados_js = []

if not dados_js:
    print("[ERRO] Nenhum dado extraído.", flush=True)
    driver.quit()
    if sys.stdin.isatty():
        input("Pressione ENTER para sair...")
    sys.exit(1)

print("[8/8] Processando datas e salvando CSV...", flush=True)

def extrair_mes_dia(aria_label):
    if not aria_label:
        return None
    m = re.search(
        r'\bon\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})',
        aria_label, re.IGNORECASE
    )
    if m:
        mes_nome = m.group(1).lower()[:3]
        dia = int(m.group(2))
        mes_num = MESES.get(mes_nome)
        if mes_num and 1 <= dia <= 31:
            return (mes_num, dia)
    return None

def inferir_anos(lista_mes_dia):
    ano_atual = datetime.now().year
    resultados = []
    ano_corrente = ano_atual
    mes_anterior = None
    ultima_data_valida = None
    
    for md in lista_mes_dia:
        if md is None:
            if ultima_data_valida:
                resultados.append(ultima_data_valida)
            else:
                resultados.append(f"{ano_atual}-01-01")
            continue
            
        mes_atual, dia = md
        if mes_anterior is not None and mes_atual > mes_anterior:
            ano_corrente -= 1
            
        data_formatada = f"{ano_corrente}-{mes_atual:02d}-{dia:02d}"
        resultados.append(data_formatada)
        ultima_data_valida = data_formatada
        mes_anterior = mes_atual
        
    return resultados

lista_mes_dia = [extrair_mes_dia(item.get("aria_label", "")) for item in dados_js]
datas_completas = inferir_anos(lista_mes_dia)

registros = []
for i, item in enumerate(dados_js):
    texto = item.get("texto", "") or ""
    link = item.get("link", "") or ""
    data = datas_completas[i] if i < len(datas_completas) else f"{datetime.now().year}-01-01"
    registros.append((data, texto, link))

try:
    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Data", "Texto", "Link"])
        for data, texto, link in registros:
            writer.writerow([data, texto, link])
    print(f"[8/8] Exportados {len(registros)} posts para {CSV_PATH}", flush=True)
except Exception as e:
    print(f"[ERRO] Falha ao salvar CSV: {e}", flush=True)

print("\n[OK] Script finalizado!", flush=True)
try:
    driver.quit()
    print("[OK] Navegador fechado.", flush=True)
except Exception:
    pass

# PROTEÇÃO FINAL: Só pede ENTER se houver terminal interativo
if sys.stdin.isatty():
    input("\nPressione ENTER para sair...")