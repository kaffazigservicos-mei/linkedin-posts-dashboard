# main.py — Menu unificado do pacote LinkedInposts
import sys
import os

# Garante que o diretório atual está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BANNER = r"""
╔══════════════════════════════════════════════════════════╗
║   📊 LinkedInposts — Gerenciador de Posts               ║
╠══════════════════════════════════════════════════════════╣
║  [1] Exportar posts do BUFFER (Selenium)                ║
║  [2] Extrair posts do LINKEDIN direto (Selenium)        ║
║  [3] Parse de HTML estático do Buffer (offline)         ║
║  [4] Buscar / Filtrar posts (análise)                   ║
║  [5] Ver estatísticas dos posts exportados              ║
║  [0] Sair                                               ║
╚══════════════════════════════════════════════════════════╝
"""

def opcao1():
    from buffer_export1 import main as rodar
    rodar()

def opcao2():
    from extrair_posts import main as rodar
    rodar()

def opcao3():
    from parse_buffer_sent import main as rodar
    rodar()

def opcao4():
    from analise_completa1 import main as rodar
    rodar()

def opcao5():
    """Mostra estatísticas rápidas do CSV de posts."""
    import csv
    from collections import Counter
    caminho = os.path.join("LinkedInposts", "posts_buffer_texto_data1.csv")
    if not os.path.exists(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        return
    with open(caminho, encoding="utf-8-sig") as f:
        sample = f.read(4096); f.seek(0)
        delim = ";" if sample.count(";") > sample.count(",") else ","
        rows = list(csv.DictReader(f, delimiter=delim))
    print(f"\n📊 Total de posts: {len(rows)}")
    redes = Counter(r.get("Rede", "?") for r in rows)
    print("📡 Por rede:")
    for k, v in redes.most_common(): print(f"   • {k}: {v}")
    anos = Counter((r.get("Data", "")[-4:] or "?") for r in rows if r.get("Data"))
    print("📅 Por ano:")
    for k, v in sorted(anos.items()): print(f"   • {k}: {v}")

OPCOES = {
    "1": opcao1, "2": opcao2, "3": opcao3,
    "4": opcao4, "5": opcao5,
}

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER)
        escolha = input("👉 Escolha uma opção: ").strip()
        if escolha == "0":
            print("👋 Até logo!"); break
        fn = OPCOES.get(escolha)
        if not fn:
            print("⚠️ Opção inválida."); input("Enter para continuar..."); continue
        try:
            fn()
        except KeyboardInterrupt:
            print("\n⛔ Interrompido.")
        except Exception as e:
            print(f"💥 Erro: {e}")
        input("\n✅ Pressione ENTER para voltar ao menu...")

if __name__ == "__main__":
    main()