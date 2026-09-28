# gerar_dashboard.py — Dashboard HTML interativo
import os
import csv
import json
from datetime import datetime
from collections import Counter, defaultdict

# ===== Configurações (Caminhos Relativos) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_ORIGEM = os.path.join(BASE_DIR, "posts_com_pilares.csv")
HTML_SAIDA = os.path.join(BASE_DIR, "dashboard.html")

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

def main():
    print("=" * 70)
    print("🎨 Gerador de Dashboard HTML — Leitura Direta do CSV Classificado")
    print("=" * 70)

    if not os.path.exists(CSV_ORIGEM):
        print(f"\n❌ ERRO: {CSV_ORIGEM} não encontrado.")
        print(" Execute o classificar_pilares.py primeiro.")
        input("\nPressione ENTER para sair...")
        return

    posts = []
    linhas_puladas = 0
    
    with open(CSV_ORIGEM, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if not row.get("Pilar_Tematico") and not row.get("Titulo"):
                linhas_puladas += 1
                continue
            posts.append(row)

    print(f"\n {len(posts)} posts válidos carregados do CSV")
    if linhas_puladas > 0:
        print(f"⚠️ {linhas_puladas} linhas vazias/corrompidas do CSV foram ignoradas.")

    if not posts:
        print("💥 CSV vazio ou sem dados válidos!")
        input("\nPressione ENTER para sair...")
        return

    total_posts = len(posts)
    contador_pilares = Counter()
    metricas_pilar = defaultdict(lambda: {"reacoes": 0, "comentarios": 0, "impressoes": 0, "alcance": 0})

    for p in posts:
        pilar = (p.get("Pilar_Tematico", "Sem classificação") or "Sem classificação").strip()
        contador_pilares[pilar] += 1
        metricas_pilar[pilar]["reacoes"] += parse_int(p.get("Reacoes", 0))
        metricas_pilar[pilar]["comentarios"] += parse_int(p.get("Comentarios", 0))
        metricas_pilar[pilar]["impressoes"] += parse_int(p.get("Impressoes", 0))
        metricas_pilar[pilar]["alcance"] += parse_int(p.get("Alcance", 0))

    total_reacoes = sum(parse_int(p.get("Reacoes", 0)) for p in posts)
    total_comentarios = sum(parse_int(p.get("Comentarios", 0)) for p in posts)
    total_impressoes = sum(parse_int(p.get("Impressoes", 0)) for p in posts)
    total_alcance = sum(parse_int(p.get("Alcance", 0)) for p in posts)
    eng_medio = (total_reacoes + total_comentarios) / total_impressoes * 100 if total_impressoes > 0 else 0

    timeline = defaultdict(int)
    pilares_timeline = defaultdict(lambda: defaultdict(int))
    for p in posts:
        dt = parse_data(p.get("Data", ""))
        pilar = (p.get("Pilar_Tematico", "Sem classificação") or "Sem classificação").strip()
        if dt:
            chave = dt.strftime("%Y-%m")
            timeline[chave] += 1
            pilares_timeline[chave][pilar] += 1
    timeline_ordenada = sorted(timeline.items())

    top_posts = sorted(posts, key=lambda x: parse_int(x.get("Impressoes", 0)), reverse=True)[:10]

    pilares_labels = json.dumps([NOMES_CURTOS.get(k, k) for k in contador_pilares.keys()])
    pilares_counts = json.dumps(list(contador_pilares.values()))
    pilares_colors = json.dumps([CORES_PILARES.get(k, "#BDBDBD") for k in contador_pilares.keys()])

    tl_labels = json.dumps([t[0] for t in timeline_ordenada])
    tl_counts = json.dumps([t[1] for t in timeline_ordenada])

    top_json = json.dumps([{
        "titulo": (p.get("Titulo", "") or "Sem título")[:70],
        "pilar": NOMES_CURTOS.get((p.get("Pilar_Tematico", "") or "").strip(), p.get("Pilar_Tematico", "")),
        "cor": CORES_PILARES.get((p.get("Pilar_Tematico", "") or "").strip(), "#BDBDBD"),
        "imp": parse_int(p.get("Impressoes", 0)),
        "rea": parse_int(p.get("Reacoes", 0)),
        "com": parse_int(p.get("Comentarios", 0)),
        "data": p.get("Data", "")
    } for p in top_posts])

    todos_pilares = list(set((p.get("Pilar_Tematico", "Sem classificação") or "Sem classificação").strip() for p in posts))
    pt_datasets = json.dumps([{
        "label": NOMES_CURTOS.get(p, p),
        "data": [pilares_timeline[m].get(p, 0) for m, _ in timeline_ordenada],
        "borderColor": CORES_PILARES.get(p, "#BDBDBD"),
        "backgroundColor": CORES_PILARES.get(p, "#BDBDBD") + "33",
        "tension": 0.3, "fill": False, "pointRadius": 4
    } for p in todos_pilares])

    met_labels = json.dumps([NOMES_CURTOS.get(k, k) for k in metricas_pilar.keys()])
    met_imp = json.dumps([metricas_pilar[k]["impressoes"] for k in metricas_pilar.keys()])
    met_rea = json.dumps([metricas_pilar[k]["reacoes"] for k in metricas_pilar.keys()])
    met_com = json.dumps([metricas_pilar[k]["comentarios"] for k in metricas_pilar.keys()])
    met_cores = json.dumps([CORES_PILARES.get(k, "#BDBDBD") for k in metricas_pilar.keys()])

    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard - Gestão de Projetos no LinkedIn</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
body { background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf7 100%); min-height: 100vh; padding: 20px; color: #2c3e50; }
.container { max-width: 1400px; margin: 0 auto; }
.header { background: linear-gradient(135deg, #0077B5 0%, #00A0DC 100%); color: #fff; padding: 40px; border-radius: 16px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,119,181,.3); text-align: center; }
.header h1 { font-size: 2.5em; margin-bottom: 10px; font-weight: 700; }
.header p { font-size: 1.1em; opacity: .95; }
.header .sub { font-size: .9em; margin-top: 10px; opacity: .8; }
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }
.kpi { background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.08); text-align: center; border-left: 5px solid #0077B5; transition: transform .2s; }
.kpi:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,.12); }
.kpi .v { font-size: 2.2em; font-weight: 700; color: #0077B5; margin: 8px 0; }
.kpi .l { color: #7f8c8d; font-size: .95em; text-transform: uppercase; letter-spacing: 1px; }
.g2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
@media (max-width: 900px) { .g2 { grid-template-columns: 1fr; } }
.card { background: #fff; padding: 28px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.08); margin-bottom: 24px; }
.card h2 { color: #2c3e50; margin-bottom: 20px; font-size: 1.4em; border-bottom: 3px solid #0077B5; padding-bottom: 10px; display: inline-block; }
.cc { position: relative; height: 380px; }
.ccl { position: relative; height: 450px; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th { background: #0077B5; color: #fff; padding: 12px; text-align: left; font-weight: 600; }
td { padding: 12px; border-bottom: 1px solid #ecf0f1; }
tr:hover { background: #f8f9fa; }
.badge { display: inline-block; padding: 4px 10px; border-radius: 12px; color: #fff; font-size: .8em; font-weight: 600; }
.mn { font-weight: 700; color: #0077B5; }
.legenda { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; justify-content: center; }
.legenda-item { display: flex; align-items: center; gap: 6px; padding: 6px 12px; background: #f8f9fa; border-radius: 20px; font-size: .85em; }
.legenda-cor { width: 14px; height: 14px; border-radius: 50%; }
.footer { text-align: center; padding: 20px; color: #7f8c8d; font-size: .9em; }
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>📊 Gestão de Projetos no LinkedIn</h1>
<p>Dashboard Interativo — Análise de Conteúdo e Engajamento</p>
<div class="sub">Gerado em """ + datetime.now().strftime("%d/%m/%Y às %H:%M") + """ • """ + str(total_posts) + """ posts analisados</div>
</div>

<div class="kpis">
<div class="kpi"><div class="l">Total de Posts</div><div class="v">""" + str(total_posts) + """</div><div>publicações analisadas</div></div>
<div class="kpi" style="border-left-color:#43A047"><div class="l">Impressões</div><div class="v" style="color:#43A047">""" + f"{total_impressoes:,}" + """</div><div>visualizações acumuladas</div></div>
<div class="kpi" style="border-left-color:#FB8C00"><div class="l">Reações</div><div class="v" style="color:#FB8C00">""" + f"{total_reacoes:,}" + """</div><div>engajamento direto</div></div>
<div class="kpi" style="border-left-color:#8E24AA"><div class="l">Engajamento</div><div class="v" style="color:#8E24AA">""" + f"{eng_medio:.2f}" + """%</div><div>(reações+coment)/impressões</div></div>
</div>

<div class="g2">
<div class="card"><h2>🎯 Distribuição por Pilar Temático</h2><div class="cc"><canvas id="c1"></canvas></div></div>
<div class="card"><h2>📈 Linha do Tempo — Posts por Mês</h2><div class="cc"><canvas id="c2"></canvas></div></div>
</div>

<div class="card"><h2>🏆 Top 10 Posts por Impressões</h2>
<table><thead><tr><th>#</th><th>Título</th><th>Pilar</th><th>Data</th><th>Impressões</th><th>Reações</th><th>Comentários</th></tr></thead>
<tbody id="tb"></tbody></table></div>

<div class="card"><h2>📊 Métricas por Pilar Temático</h2><div class="ccl"><canvas id="c3"></canvas></div></div>

<div class="card"><h2>🌊 Evolução dos Pilares ao Longo do Tempo</h2><div class="ccl"><canvas id="c4"></canvas></div>
<div class="legenda" id="leg"></div></div>

<div class="footer">
<p>💼 Dashboard gerado automaticamente a partir de posts_com_pilares.csv</p>
<p>Classificação por palavras-chave ponderadas • """ + datetime.now().strftime("%d/%m/%Y") + """</p>
</div>

</div>

<script>
new Chart(document.getElementById('c1'), {
  type: 'doughnut',
  data: {
    labels: """ + pilares_labels + """,
    datasets: [{
      data: """ + pilares_counts + """,
      backgroundColor: """ + pilares_colors + """,
      borderWidth: 3,
      borderColor: '#fff'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'bottom', labels: { padding: 15, font: { size: 12 } } },
      tooltip: {
        callbacks: {
          label: function(c) {
            const t = c.dataset.data.reduce((a, b) => a + b, 0);
            return c.label + ': ' + c.parsed + ' (' + ((c.parsed / t) * 100).toFixed(1) + '%)';
          }
        }
      }
    }
  }
});

new Chart(document.getElementById('c2'), {
  type: 'line',
  data: {
    labels: """ + tl_labels + """,
    datasets: [{
      label: 'Posts/mês',
      data: """ + tl_counts + """,
      borderColor: '#0077B5',
      backgroundColor: 'rgba(0,119,181,.15)',
      borderWidth: 3,
      tension: .4,
      fill: true,
      pointRadius: 5,
      pointBackgroundColor: '#0077B5'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      y: { beginAtZero: true, ticks: { stepSize: 1 } },
      x: { ticks: { maxRotation: 45 } }
    }
  }
});

new Chart(document.getElementById('c3'), {
  type: 'bar',
  data: {
    labels: """ + met_labels + """,
    datasets: [
      {
        label: 'Impressões',
        data: """ + met_imp + """,
        backgroundColor: """ + met_cores + """.map(c => c + 'CC'),
        borderColor: """ + met_cores + """,
        borderWidth: 2
      },
      {
        label: 'Reações',
        data: """ + met_rea + """,
        backgroundColor: """ + met_cores + """.map(c => c + '66'),
        borderColor: """ + met_cores + """,
        borderWidth: 2,
        type: 'line',
        yAxisID: 'y1',
        tension: .3,
        pointRadius: 6,
        pointBackgroundColor: """ + met_cores + """
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top' } },
    scales: {
      y: { beginAtZero: true, position: 'left', title: { display: true, text: 'Impressões' } },
      y1: { beginAtZero: true, position: 'right', title: { display: true, text: 'Reações' }, grid: { drawOnChartArea: false } },
      x: { ticks: { maxRotation: 25 } }
    }
  }
});

new Chart(document.getElementById('c4'), {
  type: 'line',
  data: {
    labels: """ + tl_labels + """,
    datasets: """ + pt_datasets + """
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: { legend: { position: 'bottom' } },
    scales: {
      y: { beginAtZero: true, ticks: { stepSize: 1 } },
      x: { ticks: { maxRotation: 45 } }
    }
  }
});

const tb = document.getElementById('tb');
""" + top_json + """.forEach((p, i) => {
  const r = document.createElement('tr');
  r.innerHTML = '<td><strong>' + (i + 1) + '</strong></td><td>' + p.titulo + '</td><td><span class="badge" style="background:' + p.cor + '">' + p.pilar + '</span></td><td>' + p.data + '</td><td class="mn">' + p.imp.toLocaleString('pt-BR') + '</td><td class="mn">' + p.rea.toLocaleString('pt-BR') + '</td><td class="mn">' + p.com.toLocaleString('pt-BR') + '</td>';
  tb.appendChild(r);
});

const leg = document.getElementById('leg');
""" + pilares_labels + """.forEach((l, i) => {
  const d = document.createElement('div');
  d.className = 'legenda-item';
  d.innerHTML = '<span class="legenda-cor" style="background:' + """ + pilares_colors + """[i] + '"></span>' + l;
  leg.appendChild(d);
});
</script>
</body>
</html>"""

    with open(HTML_SAIDA, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n Dashboard gerado: {HTML_SAIDA}")
    print(f"\n📊 RESUMO:")
    print(f"   • {total_posts} posts (Total real do CSV)")
    print(f"   • {total_impressoes:,} impressões")
    print(f"   • {total_reacoes:,} reações")
    print(f"   • {total_comentarios:,} comentários")
    print(f"   • Engajamento médio: {eng_medio:.2f}%")
    print(f"\n📊 DISTRIBUIÇÃO POR PILAR:")
    for pilar, qtd in contador_pilares.most_common():
        pct = (qtd / total_posts) * 100
        print(f"   • {NOMES_CURTOS.get(pilar, pilar)}: {qtd} posts ({pct:.1f}%)")
    print(f"\n💡 Abra o arquivo no navegador (duplo clique)")
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n💥 ERRO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione ENTER para sair...")