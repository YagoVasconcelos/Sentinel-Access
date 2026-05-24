# 🛡️ Sentinel Access

Plataforma Analítica Operacional para Controle de Acesso.

Desenvolvido por Yago Marinho.

---

# Sobre o Projeto

O Sentinel Access é uma plataforma desenvolvida para análise operacional de eventos de controle de acesso exportados do Genetec Security Desk.

O sistema permite:

- análise operacional;
- investigação de acessos;
- monitoramento de fluxo;
- análise comportamental;
- pesquisa inteligente;
- visualização analítica;
- gestão operacional de acessos.

---

# Objetivo

Centralizar e transformar dados de controle de acesso em informações estratégicas para:

- gestores;
- segurança patrimonial;
- compliance;
- operação industrial;
- inteligência operacional.

---

# Principais Funcionalidades

## 📥 Importação de CSV

Importação de arquivos exportados do:

- Genetec Security Desk 5.6

Os arquivos enviados são armazenados automaticamente em:

```text
data/uploads
```

---

## 🔍 Pesquisa Inteligente

Permite pesquisa por:

- nome;
- matrícula;
- porta;
- empresa;
- departamento;
- gestor;
- credencial.

---

## 📊 Dashboard Operacional

Visualização analítica dos eventos:

- total de acessos;
- funcionários ativos;
- portas monitoradas;
- indicadores operacionais;
- eventos registrados.

---

## 🏭 Aplicação

Projetado para:

- indústrias;
- centros operacionais;
- empresas multinacionais;
- controle de acesso corporativo;
- operações de segurança.

---

# Estrutura do Projeto

```text
Sentinel-Access/

├── app.py
├── README.md
│
├── assets/
│   ├── logo.png
│   └── styles.css
│
├── data/
│   └── uploads/
│
├── processed/
│
└── venv/
```

---

# Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- PySpark (em desenvolvimento)
- Plotly (em desenvolvimento)

---

# Funcionalidades Futuras

## Engine Analítica

- análise de turnos;
- detecção de duplicidade;
- análise 12x36;
- detecção de acessos antecipados;
- anomalias operacionais;
- análise comportamental.

---

## Recursos Corporativos

- autenticação;
- painel administrativo;
- exportação PDF;
- relatórios executivos;
- dashboards avançados;
- histórico operacional.

---

# Instalação 1

## Clonar repositório

```bash
git clone https://github.com/SEU_USUARIO/Sentinel-Access.git
```

---

## Criar ambiente virtual

```bash
python -m venv venv
```

---

## Ativar ambiente virtual

### Windows

```bash
venv\\Scripts\\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Instalação 2
.\instalar.ps1

---
# Executar o Sistema

```bash
streamlit run app.py
```

---

# Estrutura Esperada do CSV

| Campo | Descrição |
|---|---|
| Evento | Evento de acesso |
| Porta | Porta/catraca |
| Lado | Direção do leitor |
| Matricula | Matrícula |
| Nome | Nome |
| Sobrenome | Sobrenome |
| Empresa | Empresa |
| Credencial | Credencial |
| DataHora | Data e hora |
| Departamento | Departamento |
| Gestor | Gestor responsável |

---

# Direitos Autorais

© 2026 Sentinel Access

Desenvolvido por Yago Marinho.

Todos os direitos reservados.