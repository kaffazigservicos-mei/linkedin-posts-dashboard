# corrigir_inputs.py - Corrige automaticamente os input() que travam o pipeline
import os
import sys

PASTA = r"C:\Users\dilma\Documents\Linkedinposts"

def corrigir_arquivo(nome_arquivo):
    caminho = os.path.join(PASTA, nome_arquivo)
    if not os.path.exists(caminho):
        print(f"[ERRO] {nome_arquivo} nao encontrado.")
        return False
    
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    original = conteudo
    
    # 1. Garantir que "import sys" existe no topo
    if "import sys" not in conteudo:
        conteudo = "import sys\n" + conteudo
    
    # 2. Substituir input() solto por versão protegida com isatty()
    # Padrão 1: input("\nPressione ENTER para sair...")
    conteudo = conteudo.replace(
        'input("\\nPressione ENTER para sair...")',
        'if sys.stdin.isatty():\n        input("\\nPressione ENTER para sair...")'
    )
    
    # Padrão 2: input("Pressione ENTER para sair...")
    conteudo = conteudo.replace(
        'input("Pressione ENTER para sair...")',
        'if sys.stdin.isatty():\n        input("Pressione ENTER para sair...")'
    )
    
    # Padrão 3: input() sozinho (sem mensagem)
    conteudo = conteudo.replace(
        'input()',
        'if sys.stdin.isatty():\n        input()'
    )
    
    # 3. Corrigir indentação duplicada (caso já tenha sido corrigido antes)
    conteudo = conteudo.replace(
        'if sys.stdin.isatty():\n        if sys.stdin.isatty():',
        'if sys.stdin.isatty():'
    )
    
    if conteudo != original:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"[OK] {nome_arquivo} corrigido.")
        return True
    else:
        print(f"[INFO] {nome_arquivo} ja estava correto.")
        return True

# Executa a correção nos dois arquivos problemáticos
print("=" * 60)
print("CORREÇÃO AUTOMÁTICA DE INPUT() EM ARQUIVOS DO PIPELINE")
print("=" * 60)
corrigir_arquivo("buffer_export1.py")
corrigir_arquivo("classificar_pilares.py")
print("=" * 60)
print("CORREÇÃO CONCLUÍDA. Pode rodar o pipeline agora.")
print("=" * 60)