# buffer_export1.py — VERSÃO FINAL COM SCROLL AGRESSIVO
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
MAX_SCROLLS = 3000
MAX_REPEATS = 150
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
    print("[ERRO] Falha ao criar ChromeDriver: " + str(e), flush=True)
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
    print("[ERRO] Falha ao carregar página: " + str(e), flush=True)
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
    
    if sys.stdin.isatty():
        link = input("Cole o link de confirmação e pressione ENTER: ").strip()
        if not link.startswith("http"):
            print("[ERRO] URL inválida.", flush=True)
            driver.quit()
            if sys.stdin.isatty():
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
            if sys.stdin.isatty():
        input("Pressione ENTER para sair...")
            sys.exit(1)
    else:
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
    
    time.sleep(3.0)
    
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(1.5)
    
    posts = driver.find_elements(By.XPATH, "//article")
    new_count = len(posts)
    
    if i % 10 == 0 or new_count != last_count:
        print("[5/8] Scroll " + str(i) + " -> " + str(new_count) + " posts", flush=True)
        
    if new_count >= TARGET_COUNT:
        print("[5/8] Alvo atingido (" + str(new_count) + " posts).", flush=True)
        break
        
    if new_count == last_count:
        same_count_repeats += 1
        if same_count_repeats >= MAX_REPEATS:
            print("[5/8] Fim do scroll - " + str(new_count) + " posts.", flush=True)
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

print("[6/8] Expandindo 'See more'...", flush=True)
for tentativa in range(1, 15):
    botoes = driver.find_elements(By.XPATH,
        "//button[contains(translate(text(), 'SEEMORE', 'seemore'), 'see more') "
        "or contains(translate(text(), 'VERMAIS', 'vermais'), 'ver mais')]")
    if not botoes:
        print("[6/8] Sem botões na tentativa " + str(tentativa) + ".", flush=True)
        break
    print("[6/8] " + str(len(botoes)) + " botões - tentativa " + str(tentativa), flush=True)
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
    
    const allLinks = post.querySelectorAll('a[href*="linkedin.com"]');
    for (const linkEl of allLinks) {
        const href = linkEl.href || '';
        if (href.includes('/posts/') || href.includes('/feed/update/') || href.includes('/pulse/')) {
            link = href;
            break;
        }
    }
    
    if (!link && allLinks.length > 0) {
        link = allLinks[0].href || '';
    }
    
    resultados.push({ texto: texto, aria_label: aria_label, link: link });
});
return resultados;
"""

try:
    dados_js = driver.execute_script(js_code)
    print("[7/8] Extração concluída: " + str(len(dados_js)) + " posts.", flush=True)
except Exception as e:
    print("[ERRO] Falha na extração: " + str(e), flush=True)
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
    agora = datetime.now()
    ano_atual = agora.year
    mes_atual_real = agora.month
    
    resultados = []
    ano_corrente = ano_atual
    mes_anterior = None
    
    for i, md in enumerate(lista_mes_dia):
        if md is None:
            if resultados:
                resultados.append(resultados[-1])
            else:
                resultados.append(str(ano_atual) + "-01-01")
            continue
            
        mes_atual, dia = md
        
        if i == 0 and mes_atual > mes_atual_real:
            ano_corrente = ano_atual - 1
        elif mes_anterior is not None and mes_atual > mes_anterior:
            ano_corrente -= 1
            
        data_formatada = str(ano_corrente) + "-" + str(mes_atual).zfill(2) + "-" + str(dia).zfill(2)
        resultados.append(data_formatada)
        mes_anterior = mes_atual
        
    return resultados

lista_mes_dia = [extrair_mes_dia(item.get("aria_label", "")) for item in dados_js]
datas_completas = inferir_anos(lista_mes_dia)

registros = []
for i, item in enumerate(dados_js):
    texto = item.get("texto", "") or ""
    link = item.get("link", "") or ""
    data = datas_completas[i] if i < len(datas_completas) else str(datetime.now().year) + "-01-01"
    registros.append((data, texto, link))

try:
    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Data", "Texto", "Link"])
        for data, texto, link in registros:
            writer.writerow([data, texto, link])
    print("[8/8] Exportados " + str(len(registros)) + " posts para " + CSV_PATH, flush=True)
except Exception as e:
    print("[ERRO] Falha ao salvar CSV: " + str(e), flush=True)

print("\n[OK] Script finalizado!", flush=True)
try:
    driver.quit()
    print("[OK] Navegador fechado.", flush=True)
except Exception:
    pass

if sys.stdin.isatty():
    if sys.stdin.isatty():
        input("\nPressione ENTER para sair...")