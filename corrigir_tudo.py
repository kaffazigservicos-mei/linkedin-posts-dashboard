import os

PASTA = r"C:\Users\dilma\Documents\Linkedinposts"

def corrigir(nome):
    caminho = os.path.join(PASTA, nome)
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    
    novas = []
    i = 0
    corrigidos = 0
    while i < len(linhas):
        linha = linhas[i]
        novas.append(linha)
        # Detecta "if sys.stdin.isatty():"
        if "if sys.stdin.isatty():" in linha:
            # Pega a próxima linha
            if i + 1 < len(linhas):
                prox = linhas[i + 1]
                # Se tem input() mas não está indentado o suficiente
                if "input(" in prox and not prox.startswith("        "):
                    # Adiciona 8 espaços de indentação
                    novas.append("        " + prox.lstrip())
                    corrigidos += 1
                    i += 2
                    continue
        i += 1
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.writelines(novas)
    print(f"[OK] {nome}: {corrigidos} correcao(oes)")

corrigir("buffer_export1.py")
corrigir("classificar_pilares.py")
print("PRONTO!")