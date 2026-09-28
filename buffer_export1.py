# buffer_export1.py — Extração de posts do Buffer
import os
import re
import csv
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== Configurações (Caminhos Relativos) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_FOLDER = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(BASE_DIR, "posts_buffer_texto_data1.csv")

FORCAR_VISIVEL = True
TIMEOUT = 120
PAUSA_SCROLL = 2
MAX_SCROLLS = 3000
MAX_REPEATS = 100
TARGET_COUNT = 2000

os.makedirs(BASE_FOLDER, exist_ok=True)

MESES = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'june': 6, 'july': 7, 'august': 8, 'september': 9,
    'october': 10, 'november': 11, 'december': 12
}

def criar_driver(visivel: bool):
    options = Options()
    if not visivel:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,2000")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(TIMEOUT)
    driver.set_script_timeout(TIMEOUT)
    driver.implicitly_wait(30)
    return driver

def carregar_sessao():
    driver = criar_driver(visivel=FORCAR_VISIVEL)
    driver.get("https://buffer.com/app/posts/sent")
    time.sleep(10)
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//article")))
        print("✅ Sessão já válida, posts visíveis.")
        return driver
    except Exception:
        print("👉 Sessão não válida. Faça login manual e cole o link de confirmação.")
        link_confirmacao = input("Cole aqui o link de confirmação e pressione ENTER: ").strip()
        if not link_confirmacao.startswith("http"):
            print("⚠️ URL inválida. Encerrando.")
            driver.quit()
            sys.exit(1)
        driver.get(link_confirmacao)
        print("👉 Aguarde validando...")
        time.sleep(20)
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//article")))
        print("✅ Login concluído.")
        return driver

def rolar_ate_carregar_todos(driver):
    last_count = 0
    same_count_repeats = 0
    for i in range(1, MAX_SCROLLS + 1):
        posts = driver.find_elements(By.XPATH, "//article")
        if posts:
            driver.execute_script("arguments[0].scrollIntoView(true);", posts[-1])
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(PAUSA_SCROLL)
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(0.5)

        posts = driver.find_elements(By.XPATH, "//article")
        new_count = len(posts)
        print(f"📌 Scroll {i} → {new_count} posts")

        if new_count >= TARGET_COUNT:
            print(f"✅ Alvo atingido ({new_count} posts).")
            break
        if new_count == last_count:
            same_count_repeats += 1
            if same_count_repeats >= MAX_REPEATS:
                print(f"✅ Fim do scroll — {new_count} posts carregados.")
                break
        else:
            same_count_repeats = 0
        last_count = new_count

    if last_count == 0:
        print("⚠️ Nenhum post encontrado. Encerrando.")
        driver.quit()
        sys.exit(1)

def expandir_see_more(driver):
    print("🔄 Expandindo posts ('See more')...")
    total_clicados = 0
    tempo_inicio = time.time()
    TIMEOUT_EXPANSAO = 600

    for tentativa in range(1, 15):
        if time.time() - tempo_inicio > TIMEOUT_EXPANSAO:
            print(f"⚠️ Timeout de {TIMEOUT_EXPANSAO}s atingido. Parando expansão.")
            break

        botoes = driver.find_elements(By.XPATH,
            "//button[contains(translate(text(), 'SEEMORE', 'seemore'), 'see more') "
            "or contains(translate(text(), 'VERMAIS', 'vermais'), 'ver mais')]")

        if not botoes:
            print(f"✅ Sem botões na tentativa {tentativa}. Expansão concluída.")
            break

        print(f"📌 {len(botoes)} botões — tentativa {tentativa}")

        for idx, botao in enumerate(botoes, 1):
            try:
                driver.execute_script("arguments[0].click();", botao)
                total_clicados += 1
                if idx % 50 == 0:
                    print(f"   → {idx}/{len(botoes)} cliques (total: {total_clicados})")
            except Exception:
                pass

        time.sleep(2)

        if len(botoes) < 10:
            print(f"✅ Poucos botões restantes ({len(botoes)}). Fim da expansão.")
            break

    tempo_total = time.time() - tempo_inicio
    print(f"✅ Expansão concluída: {total_clicados} cliques em {tempo_total:.1f}s")
    time.sleep(3)

def liberar_texto_com_js(driver):
    driver.execute_script("""
        document.querySelectorAll('article p, article span, article div').forEach(el => {
            el.style.maxHeight = 'none';
            el.style.overflow = 'visible';
        });
    """)
    time.sleep(2)

def extrair_mes_dia(texto):
    if not texto:
        return None
    m = re.search(r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})\b', texto, re.IGNORECASE)
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

    for i, md in enumerate(lista_mes_dia):
        if md is None:
            if ultima_data_valida:
                resultados.append(ultima_data_valida)
            else:
                resultados.append(f"{ano_atual}-01-01")
            continue

        mes_atual, dia = md

        # CORREÇÃO: Se o mês aumentou, virou ano anterior (ordem decrescente)
        if mes_anterior is not None and mes_atual > mes_anterior:
            ano_corrente -= 1

        data_formatada = f"{ano_corrente}-{mes_atual:02d}-{dia:02d}"
        resultados.append(data_formatada)
        ultima_data_valida = data_formatada
        mes_anterior = mes_atual

    return resultados

def extrair_posts(driver):
    print("📌 Iniciando extração em lote via JavaScript...")
    tempo_inicio = time.time()

    js_code = """
        const posts = document.querySelectorAll('article');
        const resultados = [];

        posts.forEach(post => {
            let texto = '';
            try { texto = (post.innerText || '').trim(); } catch(e) {}

            let texto_data = '';
            const timeEl = post.querySelector('time');
            if (timeEl) {
                texto_data = timeEl.textContent || timeEl.getAttribute('datetime') || '';
            }

            if (!texto_data || texto_data.length < 5) {
                const filhos = post.querySelectorAll('span, small, time, div');
                for (const el of filhos) {
                    const t = (el.textContent || '').trim();
                    if (/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/i.test(t) && /\\d{1,2}/.test(t)) {
                        texto_data = t;
                        break;
                    }
                }
            }

            let link = '';
            const linkEl = post.querySelector('a[href*="linkedin.com"]');
            if (linkEl) link = linkEl.href || '';

            resultados.push({ texto: texto, texto_data: texto_data, link: link });
        });

        return resultados;
    """

    try:
        dados_js = driver.execute_script(js_code)
    except Exception as e:
        print(f" Erro na extração JS: {e}")
        dados_js = []

    tempo_extracao = time.time() - tempo_inicio
    print(f" Extração bruta concluída em {tempo_extracao:.1f}s — {len(dados_js)} posts coletados")

    lista_mes_dia = []
    posts_com_data_bruta = 0
    for item in dados_js:
        texto_data = item.get("texto_data", "")
        texto_completo = item.get("texto", "")

        md = extrair_mes_dia(texto_data)
        if md is None:
            md = extrair_mes_dia(texto_completo)

        lista_mes_dia.append(md)
        if md is not None:
            posts_com_data_bruta += 1

    print(f"📊 Posts com mês/dia extraído: {posts_com_data_bruta}/{len(dados_js)}")

    print("📌 Inferindo anos baseado na ordem cronológica...")
    datas_completas = inferir_anos(lista_mes_dia)

    registros = []
    for i, item in enumerate(dados_js):
        texto = item.get("texto", "") or ""
        link = item.get("link", "") or ""
        data = datas_completas[i] if i < len(datas_completas) else f"{datetime.now().year}-01-01"
        registros.append((data, texto, link))

    datas_01_01 = sum(1 for d, _, _ in registros if d.endswith("-01-01"))
    print(f"📊 Resumo: {len(registros)} posts | {datas_01_01} com data estimada (01-01)")

    return registros

def salvar_csv(registros):
    try:
        with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Data", "Texto", "Link"])
            for data, texto, link in registros:
                writer.writerow([data, texto, link])
        print(f"🎉 Exportados {len(registros)} posts para {CSV_PATH}")
    except PermissionError:
        print("❌ Erro: CSV aberto no Excel. Feche-o e rode novamente.")

if __name__ == "__main__":
    driver = None
    try:
        driver = carregar_sessao()
        rolar_ate_carregar_todos(driver)
        expandir_see_more(driver)
        liberar_texto_com_js(driver)
        registros = extrair_posts(driver)
        salvar_csv(registros)
        print("✅ Script finalizado.")
    except KeyboardInterrupt:
        print("\n⛔ Interrompido.")
    finally:
        if driver:
            driver.quit()
    input("Pressione ENTER para sair...")