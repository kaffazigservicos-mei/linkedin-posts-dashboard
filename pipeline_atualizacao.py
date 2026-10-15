# pipeline_atualizacao.py — Orquestrador Definitivo (Automação Completa)
# Caminho: C:\Users\dilma\Documents\Linkedinposts\pipeline_atualizacao.py

import os
import sys
import csv
import shutil
import subprocess
from datetime import datetime

# ===== Configurações =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_BRUTO = os.path.join(BASE_DIR, "posts_buffer_texto_data1.csv")
CSV_CLASSIFICADO = os.path.join(BASE_DIR, "posts_com_pilares.csv")
CSV_HISTORICO = os.path.join(BASE_DIR, "historico_posts.csv")
LOG_PATH = os.path.join(BASE_DIR, "pipeline.log")

TIMEOUT_ETAPA = 5400          # 90 minutos por etapa
PUBLICAR_GITHUB = False       # True = faz git push ao final


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{ts}] {msg}"
    print(linha, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(linha + "\n")
    except Exception:
        pass


def backup_arquivo(caminho):
    if os.path.exists(caminho):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(caminho)
        destino = f"{base}_backup_{ts}{ext}"
        shutil.copy2(caminho, destino)
        log(f"  💾 Backup criado: {os.path.basename(destino)}")


def executar_script(nome_script):
    """Executa script filho sem travar o console."""
    caminho = os.path.join(BASE_DIR, nome_script)
    if not os.path.exists(caminho):
        log(f"  ❌ ERRO: script nao encontrado -> {nome_script}")
        return False

    log(f"  ▶️ Executando: {nome_script}")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        resultado = subprocess.run(
            [sys.executable, caminho],
            env=env,
            stdin=subprocess.DEVNULL,
            timeout=TIMEOUT_ETAPA,
        )
        if resultado.returncode == 0:
            log(f"  ✅ {nome_script} concluido.")
            return True
        log(f"  ❌ {nome_script} FALHOU (codigo {resultado.returncode}).")
        return False
    except subprocess.TimeoutExpired:
        log(f"  ⏰ {nome_script} TIMEOUT ({TIMEOUT_ETAPA // 60} min).")
        return False
    except Exception as e:
        log(f"  💥 Erro ao executar {nome_script}: {e}")
        return False


def carregar_links_existentes(csv_path):
    links = set()
    if not os.path.exists(csv_path):
        return links
    try:
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                link = (row.get("Link") or row.get("Link_Original") or "").strip()
                if link:
                    links.add(link)
    except Exception:
        pass
    return links


def deduplicar_csv_bruto():
    if not os.path.exists(CSV_BRUTO):
        log("  ⚠️ CSV bruto nao encontrado.")
        return 0

    links_existentes = carregar_links_existentes(CSV_HISTORICO)

    if not links_existentes:
        log("  📌 Historico vazio. Todos os posts do bruto serao considerados novos.")
        with open(CSV_BRUTO, "r", encoding="utf-8-sig") as f:
            total = sum(1 for _ in csv.DictReader(f, delimiter=";"))
        return total if total > 0 else 0

    linhas_novas = 0
    registros_novos = []
    fieldnames = None

    with open(CSV_BRUTO, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        for row in reader:
            link = (row.get("Link") or "").strip()
            if link and link in links_existentes:
                continue
            registros_novos.append(row)
            linhas_novas += 1
            if link:
                links_existentes.add(link)

    if registros_novos and fieldnames:
        with open(CSV_BRUTO, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(registros_novos)

    log(f"  📊 Deduplicacao: {linhas_novas} posts novos mantidos.")
    return linhas_novas


def consolidar_historico():
    if not os.path.exists(CSV_BRUTO):
        return

    existe_historico = os.path.exists(CSV_HISTORICO)

    with open(CSV_BRUTO, "r", encoding="utf-8-sig") as f_in:
        reader = csv.DictReader(f_in, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    if not rows:
        log("  ℹ️ Nenhum post novo para consolidar.")
        return

    with open(CSV_HISTORICO, "a", newline="", encoding="utf-8-sig") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames, delimiter=";")
        if not existe_historico:
            writer.writeheader()
        writer.writerows(rows)

    log(f"  ✅ Historico atualizado: +{len(rows)} posts adicionados.")


def publicar_github():
    comandos = [
        ["git", "add", "dashboard_conteudo.html", "dashboard_recentes.html"],
        ["git", "commit", "-m", "Atualizacao automatica dos dashboards"],
        ["git", "push"],
    ]
    for cmd in comandos:
        try:
            subprocess.run(cmd, cwd=BASE_DIR, stdin=subprocess.DEVNULL, timeout=120)
        except Exception as e:
            log(f"  ⚠️ Aviso no git ({cmd[1]}): {e}")
            return False
    log("  ✅ Dashboards publicados no GitHub Pages.")
    return True


def main():
    log("=" * 70)
    log("🚀 INÍCIO DO PIPELINE AUTOMÁTICO")
    log("=" * 70)

    # Passo 1 - Backup (agora inclui o bruto)
    log("\n📦 Passo 1: Backup de seguranca")
    backup_arquivo(CSV_BRUTO)
    backup_arquivo(CSV_HISTORICO)
    backup_arquivo(CSV_CLASSIFICADO)

    # Passo 2 - Extração (falha não aborta)
    log("\n🌐 Passo 2: Extraindo posts do Buffer")
    if not executar_script("buffer_export1.py"):
        log("  ⚠️ Aviso: extracao falhou. Seguindo com dados existentes.")

    # Passo 3 - Deduplicação (NÃO encerra mais o pipeline)
    log("\n🔍 Passo 3: Filtrando posts duplicados")
    novos = deduplicar_csv_bruto()
    if novos == 0:
        log("  ℹ️ Nenhum post novo. Dashboards serao regenerados mesmo assim.")

    # Passo 4 - Consolidação
    log("\n📚 Passo 4: Salvando no historico acumulado")
    if novos > 0:
        consolidar_historico()
    else:
        log("  ℹ️ Pulado (sem posts novos)")

    # Passo 5 - Classificação (sempre executa)
    log("\n🎯 Passo 5: Classificando todo o historico por pilares")
    if os.path.exists(CSV_HISTORICO):
        shutil.copy2(CSV_HISTORICO, CSV_BRUTO)
    if not executar_script("classificar_pilares.py"):
        log("  ⚠️ Aviso: classificacao falhou. Tentando gerar dashboard mesmo assim.")

    # Passo 6 - Dashboards (sempre executa)
    log("\n📊 Passo 6: Gerando os dashboards HTML")
    ok_dash = executar_script("gerar_dashboard_conteudo.py")

    # Passo 7 - Publicação (opcional)
    if PUBLICAR_GITHUB and ok_dash:
        log("\n📤 Passo 7: Publicando no GitHub Pages")
        publicar_github()

    log("\n" + "=" * 70)
    log("✅ PIPELINE CONCLUÍDO")
    log("=" * 70)
    log("💡 Arquivos gerados: dashboard_conteudo.html e dashboard_recentes.html")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"💥 ERRO FATAL NO PIPELINE: {e}")
        import traceback
        traceback.print_exc()
        if sys.stdin.isatty():
            input("\nPressione ENTER para fechar...")