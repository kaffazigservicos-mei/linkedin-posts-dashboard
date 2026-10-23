# gerar_dashboard_conteudo.py — VERSÃO FINAL CORRETA (HTML REAL + LINKS FUNCIONAIS)
import os
import sys
import csv
import json
from datetime import datetime
from collections import Counter

# ===== Configurações =====
PASTA = r"C:\Users\dilma\Documents\Linkedinposts"
CSV_ORIGEM = os.path.join(PASTA, "posts_com_pilares.csv")
HTML_SAIDA_RELEVANCIA = os.path.join(PASTA, "dashboard_conteudo.html")
HTML_SAIDA_RECENTES = os.path.join(PASTA, "dashboard_recentes.html")

CORES_PILARES = {
    "Riscos, Orçamento e Governança": "#1E88E5",
    "Liderança, Fator Humano e Inteligência Política": "#43A047",
    "Estratégia, Valor e Negócios": "#FB8C00",
    "Metodologias, Inovação e Futuro": "#8E24AA",
    "Transversal / Reflexivo": "#757575",
    "Sem classificação": "#BDBDBD"
}

NOMES_CURTOS = {
    "Riscos, Orçamento e Governança": "Riscos & Governança",
    "Liderança, Fator Humano e Inteligência Política": "Liderança & Pessoas",
    "Estratégia, Valor e Negócios": "Estratégia & Negócios",
    "Metodologias, Inovação e Futuro": "Metodologias & Inovação",
    "Transversal / Reflexivo": "Transversal",
    "Sem classificação": "Sem Classificação"
}

MAPA_FRAMEWORKS = {
    "Riscos, Orçamento e Governança": {
        "pmbok": "Gestão de Riscos, Custos e Integração",
        "ipma": "Domínio de Contexto (Governança) e Prática (Riscos)",
        "foco": "Controle, Previsibilidade e Proteção do Valor"
    },
    "Liderança, Fator Humano e Inteligência Política": {
        "pmbok": "Gestão de Recursos e Partes Interessadas (Stakeholders)",
        "ipma": "Domínio de Pessoas (Liderança, Negociação, Conflitos)",
        "foco": "Soft Skills, Segurança Psicológica e Engajamento"
    },
    "Estratégia, Valor e Negócios": {
        "pmbok": "Entrega de Valor, Benefícios e Escopo",
        "ipma": "Domínio de Negócios (Estratégia e Benefícios)",
        "foco": "Alinhamento Estratégico e ROI"
    },
    "Metodologias, Inovação e Futuro": {
        "pmbok": "Abordagem de Desenvolvimento e Ciclo de Vida (Tailoring)",
        "ipma": "Domínio de Prática (Métodos e Ferramentas)",
        "foco": "Adaptação, IA e Melhoria Contínua"
    },
    "Transversal / Reflexivo": {
        "pmbok": "Transversal a todas as áreas de conhecimento",
        "ipma": "Transversal a todos os domínios",
        "foco": "Reflexão, Ética e Pensamento Sistêmico"
    }
}

def parse_int(valor):
    try:
        return int(str(valor).strip().replace('"', '').replace('%', ''))
    except (ValueError, TypeError):
        return 0

def parse_data(data_str):
    if not data_str:
        return None
    data_str = str(data_str).strip().replace('"', '')
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(data_str, fmt)
        except ValueError:
            continue
    return None

def calcular_bonus_recencia(data_post, data_mais_recente):
    if not data_post or not data_mais_recente:
        return 0
    diff_meses = (data_mais_recente.year - data_post.year) * 12 + (data_mais_recente.month - data_post.month)
    if diff_meses <= 0:
        return 50
    elif diff_meses <= 3:
        return 40
    elif diff_meses <= 6:
        return 25
    elif diff_meses <= 12:
        return 10
    else:
        return 0

def gerar_tabela_frameworks(contador_pilares):
    linhas = ""
    for pilar_nome in contador_pilares.keys():
        mapa = MAPA_FRAMEWORKS.get(pilar_nome, {"pmbok": "-", "ipma": "-", "foco": "-"})
        linhas += "<tr>"
        linhas += "<td><strong>" + NOMES_CURTOS.get(pilar_nome, pilar_nome) + "</strong></td>"
        linhas += "<td>" + mapa['pmbok'] + "</td>"
        linhas += "<td>" + mapa['ipma'] + "</td>"
        linhas += "<td>" + mapa['foco'] + "</td>"
        linhas += "</tr>"
    return linhas

def gerar_html_relevancia(top10, contador_pilares, total_posts, periodo_str, anos_str,
                          pilares_labels, pilares_counts, pilares_colors, pilares_pct_json):
    
    tabela_frameworks = gerar_tabela_frameworks(contador_pilares)
    
    linhas_top10 = ""
    for i, item in enumerate(top10, 1):
        p = item['post']
        titulo = (p.get("Titulo", "") or "Sem título")[:80]
        pilar = (p.get("Pilar_Tematico", "") or "").strip()
        pilar_nome = NOMES_CURTOS.get(pilar, pilar)
        pilar_cor = CORES_PILARES.get(pilar, "#BDBDBD")
        data = p.get("Data", "")
        # CORREÇÃO CRÍTICA: Pegar o link e usar no href
        link = (p.get("Link_Original", "") or "#").strip()
        
        score_orig = item['score_original']
        bonus = item['bonus_recencia']
        pont_final = item['pontuacao_final']
        
        linhas_top10 += "<tr>"
        linhas_top10 += "<td><strong>" + str(i) + "</strong></td>"
        linhas_top10 += "<td style='max-width: 400px;'>" + titulo + "</td>"
        linhas_top10 += "<td><span class='badge' style='background:" + pilar_cor + "'>" + pilar_nome + "</span></td>"
        linhas_top10 += "<td>" + data + "</td>"
        linhas_top10 += "<td><div style='font-size: 0.85em; line-height: 1.4;'>"
        linhas_top10 += "<div>Score: <strong>" + str(score_orig) + "</strong></div>"
        linhas_top10 += "<div style='color: #43A047;'>+ Recência: <strong>" + str(bonus) + "</strong></div>"
        linhas_top10 += "<div style='font-weight: bold; margin-top: 3px;'>Total: " + str(pont_final) + "</div>"
        linhas_top10 += "</div></td>"
        # CORREÇÃO CRÍTICA: Injetar o link no href
        linhas_top10 += "<td><a href='" + link + "' target='_blank' class='link-post'>Ler</a></td>"
        linhas_top10 += "</tr>"

    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Análise de Conteúdo: Relevância Temática - Gestão de Projetos</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
body { background: #f4f6f9; color: #2c3e50; padding: 20px; }
.container { max-width: 1300px; margin: 0 auto; }
.header { background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%); color: #fff; padding: 40px; border-radius: 12px; margin-bottom: 24px; text-align: center; }
.header h1 { font-size: 2.2em; margin-bottom: 10px; }
.header .periodo { font-size: 1.2em; opacity: 0.9; margin-bottom: 15px; }
.header .nota { font-size: 0.85em; opacity: 0.9; font-style: italic; max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; text-align: left; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
@media (max-width: 900px) { .grid-2 { grid-template-columns: 1fr; } }
.card { background: #fff; padding: 28px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 24px; }
.card h2 { color: #2c3e50; margin-bottom: 20px; font-size: 1.4em; border-bottom: 3px solid #4ca1af; padding-bottom: 10px; display: inline-block; }
.cc { position: relative; height: 400px; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th { background: #2c3e50; color: #fff; padding: 12px; text-align: left; font-weight: 600; }
td { padding: 12px; border-bottom: 1px solid #ecf0f1; vertical-align: middle; }
tr:hover { background: #f8f9fa; }
.badge { display: inline-block; padding: 4px 10px; border-radius: 12px; color: #fff; font-size: 0.8em; font-weight: 600; }
.link-post { color: #0077B5; text-decoration: none; font-weight: 600; }
.link-post:hover { text-decoration: underline; }
.insights { background: #eef2f5; padding: 20px; border-radius: 8px; margin-top: 15px; }
.insights h3 { color: #4ca1af; margin-bottom: 10px; }
.insights p { line-height: 1.6; }
.framework-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
.framework-table th { background: #4ca1af; }
.framework-table td { padding: 10px; border: 1px solid #ddd; font-size: 0.9em; }
.legenda-container { display: flex; flex-wrap: wrap; gap: 12px; justify-content: flex-start; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; }
.legenda-item { display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: #fff; border-radius: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); font-size: 0.9em; }
.legenda-cor { width: 16px; height: 16px; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
.footer { text-align: center; padding: 20px; color: #7f8c8d; font-size: 0.9em; }
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>Análise de Conteúdo: Gestão de Projetos</h1>
<div class="periodo">Período Analisado: """ + periodo_str + """</div>
<div class="nota"><strong>Nota Metodológica:</strong> O ano das publicações foi inferido algoritmicamente com base na ordem cronológica decrescente dos posts extraídos do Buffer, uma vez que a plataforma não exibe o ano na listagem de posts enviados. Os anos cobertos são: """ + anos_str + """.</div>
</div>

<div class="grid-2">
<div class="card">
<h2>Distribuição Temática (Pilares de Conteúdo)</h2>
<p style="margin-bottom: 15px; color: #555; font-size: 0.9em;"><strong>Pilar de Conteúdo</strong> = principais tópicos e temas abordados nos posts, agrupados por afinidade temática. A classificação é realizada por um algoritmo de scoring baseado em palavras-chave de cada pilar.</p>
<div class="cc"><canvas id="chartPilares"></canvas></div>
<div class="legenda-container" id="legendaPilares"></div>
</div>

<div class="card">
<h2>Alinhamento com Frameworks Globais (PMBOK e IPMA)</h2>
<p style="margin-bottom: 15px; color: #555; font-size: 0.9em;">
<strong>Pilar de Conteúdo</strong>: principais tópicos abordados nos posts.<br>
<strong>Foco Principal</strong>: objetivo e ênfase de cada pilar na prática da gestão.
</p>
<table class="framework-table">
<thead>
<tr><th>Pilar de Conteúdo</th><th>PMBOK (PMI)</th><th>IPMA (ICB4)</th><th>Foco Principal</th></tr>
</thead>
<tbody>
""" + tabela_frameworks + """
</tbody>
</table>
</div>
</div>

<div class="card">
<h2>Top 10 Posts Mais Representativos (Score + Recência)</h2>
<p style="margin-bottom: 15px; color: #555;"><strong>Como os posts são classificados:</strong> A pontuação final combina a <strong>aderência temática</strong> (Score original, baseado na densidade de palavras-chave dos pilares) com um <strong>bônus de recência</strong> (posts dos últimos 3 meses ganham até +40 pontos, últimos 6 meses +25, último ano +10). Essa fórmula equilibra profundidade técnica e atualidade.</p>
<table>
<thead>
<tr><th>#</th><th>Título do Post</th><th>Pilar</th><th>Data</th><th>Pontuação</th><th>Acesso</th></tr>
</thead>
<tbody>
""" + linhas_top10 + """
</tbody>
</table>
</div>

<div class="card">
<h2>Insights Estratégicos para a Comunidade de GP</h2>
<div class="insights">
<h3>1. A Transição do "Triângulo de Ferro" para a "Entrega de Valor"</h3>
<p>O conteúdo demonstra uma clara evolução da gestão tradicional (focada estritamente em Escopo, Prazo e Custo) para uma visão orientada a <strong>Benefícios e Resultados de Negócio</strong>. Isso reflete diretamente as mudanças consolidadas no PMBOK 8ª Edição e o foco do IPMA em "Business and Strategy".</p>
</div>
<div class="insights" style="margin-top: 15px;">
<h3>2. A Ascensão das "Power Skills" (Soft Skills)</h3>
<p>A alta representatividade do pilar "Liderança & Pessoas" confirma a tendência global do setor: a gestão de projetos deixou de ser apenas técnica para ser fundamentalmente <strong>humana e política</strong>. Temas como segurança psicológica, inteligência emocional e negociação são tão críticos quanto o cronograma.</p>
</div>
<div class="insights" style="margin-top: 15px;">
<h3>3. Gestão de Riscos Proativa vs. Reativa</h3>
<p>O foco em "Reservas de Contingência", "Pre-mortem" e "Gatilhos de Parada" indica uma maturidade em gestão de riscos que vai além do registro em planilhas, buscando a <strong>proteção financeira e a governança</strong> ativa da instituição.</p>
</div>
<div class="insights" style="margin-top: 15px;">
<h3>4. O Futuro: IA, Tailoring e Complexidade</h3>
<p>A menção a frameworks adaptativos, IA e o modelo Cynefin mostra que a gestão de projetos tem como desafio obter uma curadoria de métodos (Tailoring), para ser capaz de navegar na complexidade. É ir além de seguir processos rígidos.</p>
</div>
</div>

<div class="footer">
<p>Dashboard de Análise de Conteúdo gerado automaticamente.</p>
<p>Baseado em """ + str(total_posts) + """ publicações analisadas.</p>
</div>

</div>

<script>
Chart.register(ChartDataLabels);

new Chart(document.getElementById('chartPilares'), {
  type: 'doughnut',
  data: {
    labels: """ + pilares_labels + """,
    datasets: [{
      data: """ + pilares_counts + """,
      backgroundColor: """ + pilares_colors + """,
      borderWidth: 2,
      borderColor: '#fff'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      datalabels: {
        color: '#fff',
        font: { weight: 'bold', size: 14 },
        formatter: function(value, context) {
          return """ + pilares_pct_json + """[context.dataIndex];
        }
      }
    }
  }
});

const legendaContainer = document.getElementById('legendaPilares');
const labels = """ + pilares_labels + """;
const colors = """ + pilares_colors + """;
const counts = """ + pilares_counts + """;
const total = counts.reduce((a, b) => a + b, 0);

labels.forEach((label, i) => {
  const pct = ((counts[i] / total) * 100).toFixed(1);
  const item = document.createElement('div');
  item.className = 'legenda-item';
  item.innerHTML = '<span class="legenda-cor" style="background:' + colors[i] + '"></span>' + label + ' (' + pct + '%)';
  legendaContainer.appendChild(item);
});
</script>
</body>
</html>"""
    return html

def gerar_html_recentes(top10, contador_pilares, total_posts, periodo_str, anos_str,
                        pilares_labels, pilares_counts, pilares_colors, pilares_pct_json):
    
    tabela_frameworks = gerar_tabela_frameworks(contador_pilares)
    
    linhas_top10 = ""
    for i, p in enumerate(top10, 1):
        titulo = (p.get("Titulo", "") or "Sem título")[:80]
        pilar = (p.get("Pilar_Tematico", "") or "").strip()
        pilar_nome = NOMES_CURTOS.get(pilar, pilar)
        pilar_cor = CORES_PILARES.get(pilar, "#BDBDBD")
        data = p.get("Data", "")
        # CORREÇÃO CRÍTICA: Pegar o link e usar no href
        link = (p.get("Link_Original", "") or "#").strip()
        
        linhas_top10 += "<tr>"
        linhas_top10 += "<td><strong>" + str(i) + "</strong></td>"
        linhas_top10 += "<td style='max-width: 400px;'>" + titulo + "</td>"
        linhas_top10 += "<td><span class='badge' style='background:" + pilar_cor + "'>" + pilar_nome + "</span></td>"
        linhas_top10 += "<td style='font-weight: bold; color: #2c3e50;'>" + data + "</td>"
        # CORREÇÃO CRÍTICA: Injetar o link no href
        linhas_top10 += "<td><a href='" + link + "' target='_blank' class='link-post'>Ler</a></td>"
        linhas_top10 += "</tr>"

    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Análise de Conteúdo: Publicações Recentes - Gestão de Projetos</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
body { background: #f4f6f9; color: #2c3e50; padding: 20px; }
.container { max-width: 1300px; margin: 0 auto; }
.header { background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%); color: #fff; padding: 40px; border-radius: 12px; margin-bottom: 24px; text-align: center; }
.header h1 { font-size: 2.2em; margin-bottom: 10px; }
.header .periodo { font-size: 1.2em; opacity: 0.9; margin-bottom: 15px; }
.header .nota { font-size: 0.85em; opacity: 0.9; font-style: italic; max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; text-align: left; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
@media (max-width: 900px) { .grid-2 { grid-template-columns: 1fr; } }
.card { background: #fff; padding: 28px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 24px; }
.card h2 { color: #2c3e50; margin-bottom: 20px; font-size: 1.4em; border-bottom: 3px solid #4ca1af; padding-bottom: 10px; display: inline-block; }
.cc { position: relative; height: 400px; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th { background: #2c3e50; color: #fff; padding: 12px; text-align: left; font-weight: 600; }
td { padding: 12px; border-bottom: 1px solid #ecf0f1; vertical-align: middle; }
tr:hover { background: #f8f9fa; }
.badge { display: inline-block; padding: 4px 10px; border-radius: 12px; color: #fff; font-size: 0.8em; font-weight: 600; }
.link-post { color: #0077B5; text-decoration: none; font-weight: 600; }
.link-post:hover { text-decoration: underline; }
.framework-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
.framework-table th { background: #4ca1af; }
.framework-table td { padding: 10px; border: 1px solid #ddd; font-size: 0.9em; }
.legenda-container { display: flex; flex-wrap: wrap; gap: 12px; justify-content: flex-start; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; }
.legenda-item { display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: #fff; border-radius: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); font-size: 0.9em; }
.legenda-cor { width: 16px; height: 16px; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
.footer { text-align: center; padding: 20px; color: #7f8c8d; font-size: 0.9em; }
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>Publicações Recentes: Gestão de Projetos</h1>
<div class="periodo">Período Analisado: """ + periodo_str + """</div>
<div class="nota"><strong>Nota Metodológica:</strong> O ano das publicações foi inferido algoritmicamente com base na ordem cronológica decrescente dos posts extraídos do Buffer, uma vez que a plataforma não exibe o ano na listagem de posts enviados. Os anos cobertos são: """ + anos_str + """.</div>
</div>

<div class="grid-2">
<div class="card">
<h2>Distribuição Temática (Pilares de Conteúdo)</h2>
<p style="margin-bottom: 15px; color: #555; font-size: 0.9em;"><strong>Pilar de Conteúdo</strong> = principais tópicos e temas abordados nos posts, agrupados por afinidade temática. A classificação é realizada por um algoritmo de scoring baseado em palavras-chave de cada pilar.</p>
<div class="cc"><canvas id="chartPilares"></canvas></div>
<div class="legenda-container" id="legendaPilares"></div>
</div>

<div class="card">
<h2>Alinhamento com Frameworks Globais (PMBOK e IPMA)</h2>
<p style="margin-bottom: 15px; color: #555; font-size: 0.9em;">
<strong>Pilar de Conteúdo</strong>: principais tópicos abordados nos posts.<br>
<strong>Foco Principal</strong>: objetivo e ênfase de cada pilar na prática da gestão.
</p>
<table class="framework-table">
<thead>
<tr><th>Pilar de Conteúdo</th><th>PMBOK (PMI)</th><th>IPMA (ICB4)</th><th>Foco Principal</th></tr>
</thead>
<tbody>
""" + tabela_frameworks + """
</tbody>
</table>
</div>
</div>

<div class="card">
<h2>Top 10 Posts Mais Recentes</h2>
<p style="margin-bottom: 15px; color: #555;"><strong>Como os posts são classificados:</strong> Seleção baseada <strong>estritamente na data de publicação</strong>, do mais recente para o mais antigo. Esta lista garante a visualização imediata das últimas reflexões e tendências abordadas, independentemente da pontuação temática ou do Score de aderência aos pilares.</p>
<table>
<thead>
<tr><th>#</th><th>Título do Post</th><th>Pilar</th><th>Data</th><th>Acesso</th></tr>
</thead>
<tbody>
""" + linhas_top10 + """
</tbody>
</table>
</div>

<div class="footer">
<p>Dashboard de Publicações Recentes gerado automaticamente.</p>
<p>Baseado em """ + str(total_posts) + """ publicações analisadas.</p>
</div>

</div>

<script>
Chart.register(ChartDataLabels);

new Chart(document.getElementById('chartPilares'), {
  type: 'doughnut',
  data: {
    labels: """ + pilares_labels + """,
    datasets: [{
      data: """ + pilares_counts + """,
      backgroundColor: """ + pilares_colors + """,
      borderWidth: 2,
      borderColor: '#fff'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      datalabels: {
        color: '#fff',
        font: { weight: 'bold', size: 14 },
        formatter: function(value, context) {
          return """ + pilares_pct_json + """[context.dataIndex];
        }
      }
    }
  }
});

const legendaContainer = document.getElementById('legendaPilares');
const labels = """ + pilares_labels + """;
const colors = """ + pilares_colors + """;
const counts = """ + pilares_counts + """;
const total = counts.reduce((a, b) => a + b, 0);

labels.forEach((label, i) => {
  const pct = ((counts[i] / total) * 100).toFixed(1);
  const item = document.createElement('div');
  item.className = 'legenda-item';
  item.innerHTML = '<span class="legenda-cor" style="background:' + colors[i] + '"></span>' + label + ' (' + pct + '%)';
  legendaContainer.appendChild(item);
});
</script>
</body>
</html>"""
    return html

def main():
    print("=" * 70)
    print("Gerador de Dashboards de Análise de Conteúdo")
    print("=" * 70)

    if not os.path.exists(CSV_ORIGEM):
        print("\nERRO: " + CSV_ORIGEM + " não encontrado.")
        if sys.stdin.isatty():
            input("\nPressione ENTER para sair...")
        return

    posts = []
    datas_validas = []

    with open(CSV_ORIGEM, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            try:
                pilar = (row.get("Pilar_Tematico", "") or "").strip()
                titulo = (row.get("Titulo", "") or "").strip()
                if not pilar or not titulo:
                    continue

                dt = parse_data(row.get("Data", ""))
                if dt:
                    datas_validas.append(dt)

                posts.append(row)
            except Exception:
                continue

    print("\n" + str(len(posts)) + " posts válidos carregados.")

    if not posts:
        print("CSV vazio ou sem dados válidos!")
        if sys.stdin.isatty():
            input("\nPressione ENTER para sair...")
        return

    if datas_validas:
        data_min = min(datas_validas)
        data_max = max(datas_validas)
        periodo_str = data_min.strftime('%d/%m/%Y') + " a " + data_max.strftime('%d/%m/%Y')
        anos_cobertos = sorted(set(d.year for d in datas_validas))
        anos_str = ", ".join(str(a) for a in anos_cobertos)
    else:
        periodo_str = "Período não identificado"
        anos_str = "não identificado"

    total_posts = len(posts)
    contador_pilares = Counter()

    for p in posts:
        pilar = (p.get("Pilar_Tematico", "Sem classificação") or "Sem classificação").strip()
        contador_pilares[pilar] += 1

    pilares_labels = json.dumps([NOMES_CURTOS.get(k, k) for k in contador_pilares.keys()])
    pilares_counts = json.dumps(list(contador_pilares.values()))
    pilares_colors = json.dumps([CORES_PILARES.get(k, "#BDBDBD") for k in contador_pilares.keys()])

    pilares_pct = []
    for k in contador_pilares.keys():
        pct = (contador_pilares[k] / total_posts) * 100
        pilares_pct.append("{:.1f}%".format(pct))
    pilares_pct_json = json.dumps(pilares_pct)

    data_mais_recente = max(datas_validas) if datas_validas else None

    posts_com_pontuacao = []
    for p in posts:
        score_original = parse_int(p.get("Score", 0))
        data_post = parse_data(p.get("Data", ""))
        bonus_recencia = calcular_bonus_recencia(data_post, data_mais_recente)
        pontuacao_final = score_original + bonus_recencia

        posts_com_pontuacao.append({
            'post': p,
            'score_original': score_original,
            'bonus_recencia': bonus_recencia,
            'pontuacao_final': pontuacao_final
        })

    posts_ordenados = sorted(posts_com_pontuacao, key=lambda x: x['pontuacao_final'], reverse=True)
    top_10_relevancia = posts_ordenados[:10]

    posts_ordenados_data = sorted(
        posts,
        key=lambda x: parse_data(x.get("Data", "")) or datetime.min,
        reverse=True
    )
    top_10_recentes = posts_ordenados_data[:10]

    html_relevancia = gerar_html_relevancia(
        top_10_relevancia, contador_pilares, total_posts,
        periodo_str, anos_str,
        pilares_labels, pilares_counts, pilares_colors, pilares_pct_json
    )
    with open(HTML_SAIDA_RELEVANCIA, "w", encoding="utf-8") as f:
        f.write(html_relevancia)
    print("\nDashboard de Relevância gerado: " + HTML_SAIDA_RELEVANCIA)

    html_recentes = gerar_html_recentes(
        top_10_recentes, contador_pilares, total_posts,
        periodo_str, anos_str,
        pilares_labels, pilares_counts, pilares_colors, pilares_pct_json
    )
    with open(HTML_SAIDA_RECENTES, "w", encoding="utf-8") as f:
        f.write(html_recentes)
    print("Dashboard de Recentes gerado: " + HTML_SAIDA_RECENTES)

    print("\nPeríodo: " + periodo_str)
    print("Anos cobertos: " + anos_str)
    print("Total de posts analisados: " + str(total_posts))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nERRO: " + type(e).__name__ + ": " + str(e))
        import traceback
        traceback.print_exc()
        if sys.stdin.isatty():
            input("\nPressione ENTER para sair...")