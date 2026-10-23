# classificar_pilares.py - VERSÃO FINAL COM CORREÇÃO ISATTY
import os
import sys
import csv
import re
import unicodedata
from collections import Counter
from datetime import datetime

PASTA = r"C:\Users\dilma\Documents\Linkedinposts"
CSV_ORIGEM = os.path.join(PASTA, "posts_buffer_texto_data1.csv")
CSV_SAIDA = os.path.join(PASTA, "posts_com_pilares.csv")

PILARES = {
    "Riscos, Orçamento e Governança": {
        "risco": 3, "riscos": 3, "contingência": 4, "contingencia": 4,
        "reserva": 3, "reservas": 3, "orçamento": 3, "orcamento": 3,
        "custo": 2, "custos": 2, "baseline": 3, "linha de base": 3,
        "cpi": 4, "spi": 4, "eap": 3, "wbs": 3, "pre-mortem": 4,
        "premortem": 4, "governança": 3, "governanca": 3, "governar": 2,
        "matriz de tolerância": 4, "gatilho": 2, "gatilhos": 2,
        "incerteza": 3, "incertezas": 3, "contenção": 3, "contencao": 3,
        "aditivo": 3, "aditivo contratual": 4, "desvio": 2, "desvios": 2,
        "mitigar": 3, "mitigação": 3, "mitigacao": 3, "absorver": 2,
        "imprevisto": 3, "imprevistos": 3, "volatilidade": 2,
        "capital": 2, "caixa": 2, "financeiro": 2, "financeira": 2,
        "rentabilidade": 3, "roi": 3, "orçamentária": 3, "orcamentaria": 3,
        "proteção": 2, "protecao": 2, "proteger": 2
    },
    "Liderança, Fator Humano e Inteligência Política": {
        "liderança": 3, "lideranca": 3, "líder": 2, "lider": 2,
        "equipe": 2, "equipes": 2, "time": 2, "times": 2, "grupo": 2, "grupos": 2,
        "pessoas": 2, "pessoa": 2, "humano": 2, "humana": 2,
        "inteligência política": 4, "inteligencia politica": 4,
        "segurança psicológica": 4, "seguranca psicologica": 4,
        "burnout": 4, "esgotamento": 3, "fadiga": 3,
        "cnv": 4, "comunicação não violenta": 4, "comunicacao nao violenta": 4,
        "mediação": 3, "mediacao": 3, "conflito": 2, "conflitos": 2,
        "motivação": 2, "motivacao": 2, "engajamento": 2,
        "feedback": 2, "feed-back": 2, "feedbacks": 2,
        "delegar": 2, "delegação": 2, "delegacao": 2,
        "onboarding": 3, "integração": 2, "integracao": 2,
        "stakeholder": 2, "stakeholders": 2, "patrocinador": 2,
        "silêncio": 2, "silencio": 2, "omissão": 2, "omissao": 2,
        "empatia": 2, "escuta": 2, "escuta ativa": 3,
        "confiança": 2, "confianca": 2, "confiar": 2,
        "cultura": 2, "organizacional": 2, "clima": 2,
        "cansaço": 2, "cansaco": 2, "sociedade do cansaço": 4,
        "sombras no trono": 4, "vies": 2, "vieses": 2,
        "dunning-kruger": 4, "dunning kruger": 4
    },
    "Estratégia, Valor e Negócios": {
        "estratégia": 3, "estrategia": 3, "estratégico": 3, "estrategico": 3,
        "valor": 2, "valores": 2, "negócio": 2, "negocio": 2, "negócios": 2,
        "negocios": 2, "pmo": 4, "escritório de projetos": 4,
        "escritorio de projetos": 4, "sensemaking": 4,
        "spin": 3, "spin selling": 4, "bant": 4,
        "portfólio": 3, "portfolio": 3, "programa": 2,
        "esg": 4, "sustentabilidade": 2, "sustentável": 2, "sustentavel": 2,
        "business acumen": 4, "utilidade": 2, "útil": 2, "util": 2,
        "justificativa de negócio": 4, "justificativa de negocio": 4,
        "viabilidade": 3, "investimento": 2, "investir": 2,
        "rentável": 2, "rentavel": 2, "lucro": 2, "lucratividade": 3,
        "decisão": 2, "decisao": 2, "decisões": 2, "decisoes": 2,
        "objetivo": 2, "objetivos": 2, "meta": 2, "metas": 2,
        "resultado": 2, "resultados": 2, "entrega": 2, "entregas": 2,
        "cliente": 2, "clientes": 2, "patrocinador": 2, "sponsor": 3,
        "roadmap": 3, "visão": 2, "visao": 2, "longo prazo": 3,
        "perenidade": 3, "posicionamento": 2, "marca": 2,
        "bússola": 3, "bussola": 3, "norte": 2
    },
    "Metodologias, Inovação e Futuro": {
        "metodologia": 2, "metodologias": 2, "método": 2, "metodo": 2, "métodos": 2, "metodos": 2,
        "framework": 3, "frameworks": 3, "pmbok": 4,
        "ágil": 2, "agil": 2, "agile": 3, "scrum": 3, "kanban": 3, "lean": 3,
        "ia": 2, "inteligência artificial": 4, "inteligencia artificial": 4, "ai": 2,
        "gêmeos digitais": 4, "gemeos digitais": 4, "digital twins": 4,
        "tailoring": 4, "adaptação": 2, "adaptacao": 2, "inovar": 2,
        "inovação": 3, "inovacao": 3, "inovador": 2, "disruptivo": 3, "disruptiva": 3,
        "transformação": 2, "transformacao": 2, "tecnologia": 2, "tecnologias": 2,
        "digital": 2, "digitais": 2, "automação": 2, "automacao": 2, "automatizar": 2,
        "futuro": 2, "tendência": 2, "tendencia": 2, "tendências": 2, "tendencias": 2,
        "hiperpersonalização": 4, "hiperpersonalizacao": 4, "ambidestria": 4,
        "híbrido": 2, "hibrido": 2, "cynefin": 4, "complexidade": 2, "complexo": 2, "complexa": 2,
        "aprendizado": 2, "lições aprendidas": 3, "licoes aprendidas": 3,
        "retrospectiva": 3, "micro-retrospectiva": 4, "microretrospectiva": 4,
        "iteração": 2, "iteracao": 2, "incremental": 2, "protótipo": 2, "prototipo": 2,
        "teste": 2, "testar": 2, "experimento": 2, "experimentar": 2, "curva s": 3
    }
}

def normalizar(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", str(texto))
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.lower()

def classificar_post(texto):
    if not texto or not isinstance(texto, str):
        return ("Sem classificação", 0, [])
    texto_norm = normalizar(texto)
    scores = {}
    termos_por_pilar = {}
    for pilar, palavras in PILARES.items():
        score = 0
        termos = []
        for termo, peso in palavras.items():
            termo_norm = normalizar(termo)
            ocorrencias = min(texto_norm.count(termo_norm), 3)
            if ocorrencias > 0:
                score += peso * ocorrencias
                termos.append(termo + "(" + str(ocorrencias) + ")")
        scores[pilar] = score
        termos_por_pilar[pilar] = termos
    pilar_vencedor = max(scores, key=scores.get)
    score_max = scores[pilar_vencedor]
    if score_max < 4:
        return ("Transversal / Reflexivo", score_max, [])
    return (pilar_vencedor, score_max, termos_por_pilar[pilar_vencedor])

def limpar_texto_buffer(texto_bruto):
    if not texto_bruto:
        return ""
    texto = re.sub(r"^Notes\s*Dilma Balbi.*?\s*", "", texto_bruto, flags=re.IGNORECASE)
    texto = re.split(r"\nView\nAdd tags|\nAdd tags|\nSee Post Insights", texto, flags=re.IGNORECASE)[0]
    texto = re.sub(r"\nReactions\n\d+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nComments\n\d+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nEng\. Rate\n\d+%", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nImpressions\n\d+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nReach\n\d+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nRefreshed.*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nYou created this.*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nGo to post.*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nMore actions.*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nVideo Views\n\d+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nWatch Time.*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nUnique Viewers\n\d+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nScroll right", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\nPublished via.*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()

def extrair_titulo(texto):
    if not texto:
        return "Sem título"
    for linha in texto.split("\n"):
        linha = linha.strip()
        if linha and len(linha) > 10:
            if len(linha) > 100:
                linha = linha[:97] + "..."
            return linha
    return "Sem título"

def extrair_metricas(texto):
    if not texto:
        return {"reacoes": 0, "comentarios": 0, "impressoes": 0, "alcance": 0, "engajamento": "0%"}
    metricas = {}
    m = re.search(r"Reactions\s*\n?\s*(\d+)", texto, re.IGNORECASE)
    metricas["reacoes"] = int(m.group(1)) if m else 0
    m = re.search(r"Comments\s*\n?\s*(\d+)", texto, re.IGNORECASE)
    metricas["comentarios"] = int(m.group(1)) if m else 0
    m = re.search(r"Impressions\s*\n?\s*(\d+)", texto, re.IGNORECASE)
    metricas["impressoes"] = int(m.group(1)) if m else 0
    m = re.search(r"Reach\s*\n?\s*(\d+)", texto, re.IGNORECASE)
    metricas["alcance"] = int(m.group(1)) if m else 0
    m = re.search(r"Eng\.\s*Rate\s*\n?\s*(\d+%)", texto, re.IGNORECASE)
    metricas["engajamento"] = m.group(1) if m else "0%"
    return metricas

def main():
    print("=" * 70)
    print("Classificador Automático de Posts por Pilar Temático")
    print("=" * 70)
    if not os.path.exists(CSV_ORIGEM):
        print("\nERRO: Arquivo não encontrado: " + CSV_ORIGEM)
        if sys.stdin.isatty():
            if sys.stdin.isatty():
        input("\nPressione ENTER para sair...")
        return
    posts = []
    with open(CSV_ORIGEM, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            posts.append(row)
    print("\n" + str(len(posts)) + " posts carregados de " + CSV_ORIGEM)
    if len(posts) == 0:
        print("\nERRO: Nenhum post foi lido do CSV!")
        if sys.stdin.isatty():
            if sys.stdin.isatty():
        input("\nPressione ENTER para sair...")
        return
    print("\nClassificando posts...")
    resultados = []
    contador_pilares = Counter()
    for i, post in enumerate(posts, 1):
        texto_bruto = post.get("Texto", "") or ""
        data = post.get("Data", "") or ""
        link = post.get("Link", "") or ""
        pilar, score, termos = classificar_post(texto_bruto)
        texto_limpo = limpar_texto_buffer(texto_bruto)
        titulo = extrair_titulo(texto_limpo)
        metricas = extrair_metricas(texto_bruto)
        registro = {
            "Data": data,
            "Pilar_Tematico": pilar,
            "Score": score,
            "Titulo": titulo,
            "Corpo_Limpo": texto_limpo,
            "Reacoes": metricas["reacoes"],
            "Comentarios": metricas["comentarios"],
            "Impressoes": metricas["impressoes"],
            "Alcance": metricas["alcance"],
            "Taxa_Engajamento": metricas["engajamento"],
            "Termos_Chave": ", ".join(termos[:10]) if termos else "",
            "Link_Original": link
        }
        resultados.append(registro)
        contador_pilares[pilar] += 1
        if i % 50 == 0:
            print("   -> " + str(i) + "/" + str(len(posts)) + " classificados")
    print("Classificação concluída: " + str(len(resultados)) + " posts processados")
    print("\n" + "=" * 70)
    print("ESTATÍSTICAS DE CLASSIFICAÇÃO")
    print("=" * 70)
    for pilar, qtd in contador_pilares.most_common():
        pct = (qtd / len(resultados)) * 100
        print("   - " + pilar + ": " + str(qtd) + " posts (" + "{:.1f}".format(pct) + "%)")
    campos = ["Data", "Pilar_Tematico", "Score", "Titulo", "Corpo_Limpo",
              "Reacoes", "Comentarios", "Impressoes", "Alcance",
              "Taxa_Engajamento", "Termos_Chave", "Link_Original"]
    try:
        with open(CSV_SAIDA, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            writer.writeheader()
            writer.writerows(resultados)
        print("\nArquivo gerado: " + CSV_SAIDA)
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_alt = os.path.join(PASTA, "posts_com_pilares_" + timestamp + ".csv")
        with open(csv_alt, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            writer.writeheader()
            writer.writerows(resultados)
        print("\nCSV original aberto. Salvo em: " + csv_alt)
    print("\n" + "=" * 70)
    print("AMOSTRA DOS 10 POSTS MAIS RECENTES CLASSIFICADOS")
    print("=" * 70)
    for r in resultados[:10]:
        print("\n" + r['Data'] + " | " + r['Pilar_Tematico'] + " (score: " + str(r['Score']) + ")")
        print("   " + r['Titulo'])
        print("   " + str(r['Reacoes']) + " reacoes | " + str(r['Comentarios']) + " comentarios | " + str(r['Impressoes']) + " impressoes")
    print("\n" + "=" * 70)
    print("Processo concluído com sucesso!")
    print("=" * 70)
    # CORREÇÃO: Proteção isatty() aplicada aqui
    if sys.stdin.isatty():
        input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário.")
    except Exception as e:
        print("\nERRO: " + type(e).__name__ + ": " + str(e))
        import traceback
        traceback.print_exc()
        # CORREÇÃO: Proteção isatty() aplicada aqui também
        if sys.stdin.isatty():
            if sys.stdin.isatty():
        input("\nPressione ENTER para sair...")