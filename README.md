# 📊 LinkedIn Posts Dashboard

Sistema automatizado para extração, classificação e visualização de publicações do LinkedIn via Buffer, com geração de dashboards interativos hospedados no GitHub Pages.

![Status](https://img.shields.io/badge/status-operacional-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 🎯 Visão Geral

Este projeto transforma publicações do LinkedIn em inteligência estratégica acessível publicamente. Ele extrai automaticamente os posts enviados via Buffer, classifica cada publicação em pilares temáticos usando um algoritmo de scoring baseado em palavras-chave, e gera dois dashboards HTML interativos atualizados semanalmente.

### 🌐 Dashboards Públicos

- **Dashboard de Relevância Temática** → [dashboard_conteudo.html](https://kaffazigservicos-mei.github.io/linkedin-posts-dashboard/dashboard_conteudo.html)
- **Dashboard de Publicações Recentes** → [dashboard_recentes.html](https://kaffazigservicos-mei.github.io/linkedin-posts-dashboard/dashboard_recentes.html)

---

## 📁 Estrutura do Projeto
linkedin-posts-dashboard/
├── pipeline_atualizacao.py # Orquestrador principal (6 passos)
├── buffer_export1.py # Extração via Selenium + Buffer
├── classificar_pilares.py # Classificação temática por scoring
├── gerar_dashboard_conteudo.py # Gerador dos dois dashboards HTML
├── rodar_buffer.bat # Script de execução Windows
── README.md # Este arquivo
├── .gitignore # Ignora CSVs grandes e backups
├── .nojekyll # Habilita GitHub Pages
│
├── posts_buffer_texto_data1.csv # Dados brutos extraídos
├── historico_posts.csv # Histórico acumulado
├── posts_com_pilares.csv # Dados classificados
│
├── dashboard_conteudo.html # Dashboard de Relevância
├── dashboard_recentes.html # Dashboard de Recentes
└── pipeline.log # Log de execuções


---

## 🚀 Funcionalidades

### ✅ Pipeline Automatizado (6 Passos)

1. **Backup de Segurança** → Cria cópias dos CSVs antes de qualquer alteração
2. **Extração do Buffer** → Selenium rola a página, expande "See more" e salva posts
3. **Deduplicação** → Compara com histórico e mantém apenas posts novos
4. **Consolidação** → Anexa posts novos ao histórico acumulado
5. **Classificação Temática** → Scoring por palavras-chave em 5 pilares
6. **Geração de Dashboards** → Cria dois HTMLs interativos

### 🎨 Dois Dashboards Interativos

#### 1. Dashboard de Relevância Temática
- **Critério:** Top 10 por pontuação combinada (Score + Recência)
- **Fórmula:** `Pontuação Final = Score Original + Bônus de Recência`
  - Posts do mês atual: +50 pontos
  - Últimos 3 meses: +40 pontos
  - Últimos 6 meses: +25 pontos
  - Último ano: +10 pontos
- **Conteúdo:** Gráfico de pizza, tabela de frameworks (PMBOK 8ª / IPMA ICB4), insights estratégicos

#### 2. Dashboard de Publicações Recentes
- **Critério:** Top 10 ordenados estritamente por data (mais recente → mais antigo)
- **Conteúdo:** Gráfico de pizza, tabela de frameworks, visualização cronológica

---

##  Pilares Temáticos

O sistema classifica automaticamente cada post em um dos 5 pilares estratégicos:

| Pilar | Cor | Foco Principal |
|-------|-----|----------------|
| **Riscos, Orçamento e Governança** | 🔵 Azul | Controle, Previsibilidade e Proteção do Valor |
| **Liderança, Fator Humano e Inteligência Política** | 🟢 Verde | Soft Skills, Segurança Psicológica e Engajamento |
| **Estratégia, Valor e Negócios** | 🟠 Laranja | Alinhamento Estratégico e ROI |
| **Metodologias, Inovação e Futuro** | 🟣 Roxo | Adaptação, IA e Melhoria Contínua |
| **Transversal / Reflexivo** | ⚫ Cinza | Reflexão, Ética e Pensamento Sistêmico |

---

## ⚙️ Pré-requisitos

### Software
- **Python 3.10+** (testado com Python 3.14)
- **Google Chrome** (versão compatível com ChromeDriver)
- **Git** (para versionamento e publicação)
- **Conta Buffer** conectada ao LinkedIn profissional
- **Conta GitHub** (para hospedagem pública)

### Bibliotecas Python
```bash
pip install selenium beautifulsoup4

Configurações do Windows
Agendador de Tarefas (para execução semanal automática)
Permissões de execução para scripts .bat
Variável de ambiente PYTHONIOENCODING=utf-8

📋 Instalação e Configuração
1. Clonar o Repositório
git clone https://github.com/kaffazigservicos-mei/linkedin-posts-dashboard.git
cd linkedin-posts-dashboard

2. Instalar Dependências
bash
pip install selenium beautifulsoup4

3. Configurar Caminhos
Edite os arquivos Python e ajuste BASE_FOLDER ou PASTA para seu diretório local:
python
1 BASE_FOLDER = r"C:\Users\seu-usuario\Documents\Linkedinposts"

4. Configurar GitHub Pages
Acesse: https://github.com/kaffazigservicos-mei/linkedin-posts-dashboard/settings/pages
Em Source, selecione:
Branch: main
Folder: / (root)
Clique em Save

🔄 Como Usar
Execução Manual
bash
# Executar pipeline completo
python pipeline_atualizacao.py

# Ou usar o script batch
rodar_buffer.bat

Agendamento Automático (Windows)
Abra o Agendador de Tarefas (taskschd.msc)
Crie nova tarefa básica
Configure:
Nome: "Atualização Semanal LinkedIn"
Disparador: Semanal (ex: segunda-feira, 08:00)
Ação: Iniciar programa
Programa: C:\Users\seu-usuario\AppData\Local\Programs\Python\Python314\python.exe
Argumentos: "C:\Users\seu-usuario\Documents\Linkedinposts\pipeline_atualizacao.py"
Iniciar em: C:\Users\seu-usuario\Documents\Linkedinposts
Marque "Executar apenas quando o usuário estiver conectado"


Publicação no GitHub
bash
git add .
git commit -m "Atualização automática dos dashboards"
git push

📊 Metodologia de Classificação
Algoritmo de Scoring
Cada post é analisado contra um dicionário de ~200 palavras-chave distribuídas entre os 4 pilares principais. Cada termo possui um peso (2 a 4 pontos) baseado em sua especificidade temática.
Exemplo:
"contingência" → 4 pontos (Riscos)
"segurança psicológica" → 4 pontos (Liderança)
"pmbok" → 4 pontos (Metodologias)
"equipe" → 2 pontos (Liderança)

Regras de Classificação
O post recebe o pilar com maior score acumulado
Posts com score total < 4 são classificados como "Transversal / Reflexivo"
Cada ocorrência de termo é contada até 3 vezes (para evitar viés de repetição)
Termos com e sem acento são tratados como equivalentes
Inferência de Ano
O Buffer não exibe o ano na listagem de posts enviados. O algoritmo infere o ano algoritmicamente com base na ordem cronológica decrescente dos posts extraídos, assumindo que posts mais antigos pertencem a anos anteriores quando há inversão de meses.

🛠️ Troubleshooting
Sessão do Buffer Expirada
O pipeline detecta automaticamente e continua com dados existentes. Para renovar:
bash
python buffer_export1.py
Dashboards não atualizam no GitHub Pages
Aguarde 2-3 minutos após o push
Pressione Ctrl + F5 no navegador para limpar cache
Verifique se o arquivo .nojekyll existe na raiz do repositório
Erro de Deadlock no Passo 5
Já corrigido na versão atual. O pipeline usa stdin=subprocess.DEVNULL para evitar travamentos.
CSV Aberto no Excel
Feche o Excel antes de rodar o pipeline. O Windows bloqueia escrita em arquivos CSV abertos.


Estatísticas Atuais
Total de posts analisados: ~600 publicações
Período coberto: 2022 a 2026
Pilar mais frequente: Metodologias, Inovação e Futuro (~41%)
Tempo médio de execução: 30-60 minutos (depende da sessão do Buffer)


🤝 Contribuindo
Este é um projeto pessoal de automação e análise de dados. Se você deseja adaptar para seu uso:
Faça um fork do repositório
Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade)
Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')
Push para a branch (git push origin feature/nova-funcionalidade)
Abra um Pull Request

📄 Licença
Este projeto é fornecido "como está", sem garantias. Use por sua conta e risco.
📚 Recursos Adicionais
Documentação Selenium Python
GitHub Pages Documentation
Buffer API Documentation
PMBOK 8th Edition - PMI
IPMA ICB4
📞 Contato
GitHub: kaffazigservicos-mei
LinkedIn: Dilma Balbi
Última atualização: Outubro 2026
Versão do sistema: 2.1
Status: ✅ Operacional e em produção


