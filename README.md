# 📊 LinkedIn Posts Dashboard

Dashboard interativo e pipeline de análise de conteúdo para posts do LinkedIn exportados via Buffer. O projeto extrai posts, classifica-os automaticamente em pilares temáticos de Gestão de Projetos e gera um relatório HTML visual com métricas de engajamento.

## 🚀 Funcionalidades

- **Extração Automatizada:** Scraping de posts enviados via Buffer usando Selenium.
- **Classificação Inteligente:** Algoritmo de scoring por palavras-chave que categoriza posts em 4 pilares temáticos.
- **Dashboard Interativo:** Geração de um arquivo HTML standalone com gráficos (Chart.js) e KPIs.
- **Limpeza de Dados:** Remoção automática de ruído da interface do Buffer.

##  Estrutura do Projeto
linkedin-posts-dashboard/
├── buffer_export1.py # Script de extração (Selenium)
├── classificar_pilares.py # Classificador temático
├── gerar_dashboard.py # Gerador do HTML interativo
├── requirements.txt # Dependências Python
├── .gitignore # Arquivos ignorados pelo Git
└── README.md # Este arquivo


## ️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/linkedin-posts-dashboard.git
   cd linkedin-posts-dashboard

2. Crie um ambiente virtual (recomendado) e instale as dependências
bath
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt

🎯 Como Usar
O pipeline funciona em 3 etapas sequenciais:
Passo 1: Extrair posts do Buffer
bash

1
Nota: Requer que você faça login no Buffer e cole o link de confirmação no console na primeira execução. O arquivo posts_buffer_texto_data1.csv será gerado.
Passo 2: Classificar os posts
bash

1
Lê o CSV bruto, limpa o texto, extrai métricas e gera o arquivo posts_com_pilares.csv.
Passo 3: Gerar o Dashboard
bash

1
Lê o CSV classificado e gera o arquivo dashboard.html. Abra este arquivo em qualquer navegador para visualizar o relatório.
🎨 Pilares Temáticos
Os posts são classificados automaticamente em:
🔵 Riscos, Orçamento e Governança
🟢 Liderança, Fator Humano e Inteligência Política
Estratégia, Valor e Negócios
🟣 Metodologias, Inovação e Futuro
🛠️ Tecnologias
Python 3.10+
Selenium (Web Scraping)
Chart.js (Visualização de dados via CDN)
HTML5/CSS3 (Dashboard standalone)
