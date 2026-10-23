import os

caminho = r"C:\Users\dilma\Documents\Linkedinposts\classificar_pilares.py"

with open(caminho, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Adiciona import sys se não existir
if "import sys" not in conteudo:
    conteudo = "import sys\n" + conteudo

# Substitui TODOS os input() soltos por versão protegida
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

# Remove duplicatas (caso já tenha sido corrigido parcialmente)
conteudo = conteudo.replace(
    'if sys.stdin.isatty():\n        if sys.stdin.isatty():',
    'if sys.stdin.isatty():'
)

with open(caminho, "w", encoding="utf-8") as f:
    f.write(conteudo)

print("✅ classificar_pilares.py corrigido automaticamente!")