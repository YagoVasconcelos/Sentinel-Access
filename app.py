import streamlit as st
from PIL import Image
import pandas as pd
import os
from services.csv_loader import carregar_csv
from dashboard.sidebar import render_sidebar
from dashboard.executive import render_executive_dashboard
from dashboard.operational import render_operational_table
from dashboard.charts import render_charts
from dashboard.security import render_security
from dashboard.compliance import render_compliance
from services.shift_classifier import (classificar_turno, detectar_antecedencia)
from services.risk_engine import classificar_risco
from services.cleaner import limpar_duplicados
from services.data_cleaning import limpar_eventos



# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Sentinel Access",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CSS
# ==================================================

def load_css():
    if os.path.exists("assets/styles.css"):
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ==================================================
# LOGO
# ==================================================

logo_path = "assets/logo.png"
logo = Image.open(logo_path) if os.path.exists(logo_path) else None

# ==================================================
# PASTA UPLOAD
# ==================================================

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==================================================
# SIDEBAR
# ==================================================

arquivo_selecionado, pesquisa = render_sidebar(
    logo,
    UPLOAD_FOLDER
)

# ==================================================
# PESQUISA + FILTRO DATA/HORA
# ==================================================

busca_col1, busca_col2 = st.sidebar.columns([5, 1])

with busca_col1:

    pesquisa = st.text_input(
        "Pesquisar por",
        placeholder="Nome, matrícula, porta..."
    )

with busca_col2:

    st.markdown("<br>", unsafe_allow_html=True)

    with st.popover("📅"):

        usar_data = st.checkbox("Usar Data")

        if usar_data:

            filtro_data = st.date_input(
                "Selecionar Data"
            )

        else:
            filtro_data = None

        usar_hora = st.checkbox("Usar Hora")

        if usar_hora:

            filtro_hora = st.text_input(
                "Hora",
                placeholder="Ex: 02:18 ou 14:30"
            )

        else:
            filtro_hora = None

        # LIMPAR FILTROS

        if st.button("Limpar"):

            st.rerun()


# ==================================================
# LEITURA CSV
# ==================================================

df = pd.DataFrame()

if arquivo_selecionado:

    try:

        df = carregar_csv(
            UPLOAD_FOLDER,
            arquivo_selecionado
        )
        
        df = limpar_duplicados(df)

    except Exception as e:

        st.error(
            f"Erro ao carregar CSV: {e}"
        )

# ==================================================
# FILTROS SOC
# ==================================================

st.markdown("""
<div class="soc-header">

<span class="soc-icon">🔍</span>

<span class="soc-title">
FILTROS OPERACIONAIS
</span>

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    filtro_nome = st.text_input("Filtrar por Nome")

with col2:
    filtro_porta = st.text_input("Filtrar por Porta")

with col3:
    filtro_evento = st.selectbox(
        "Tipo de Evento",
        ["Todos", "Entrada", "Saída", "Negado"]
    )

# ==================================================
# APLICAR FILTROS
# ==================================================

df_filtrado = df.copy()

# ==================================================
# PROCESSAMENTO CENTRAL
# ==================================================

if "DataHora" in df_filtrado.columns:

    # CONVERTER DATA

    df_filtrado[
        "DataHora"
    ] = pd.to_datetime(
        df_filtrado[
            "DataHora"
        ],
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce"
    )

    # ==========================================
    # LIMPEZA INTELIGENTE
    # ==========================================

    df_filtrado = limpar_eventos(
        df_filtrado
    )

    # EXTRAIR HORA

    df_filtrado["Hora"] = df_filtrado[
        "DataHora"
    ].dt.hour

    # EXTRAIR DATA

    df_filtrado["Data"] = df_filtrado[
        "DataHora"
    ].dt.date


# ==================================================
# CLASSIFICAÇÃO OPERACIONAL
# ==================================================

if "DataHora" in df_filtrado.columns:

    df_filtrado[
        "DataHora"
    ] = pd.to_datetime(
        df_filtrado[
            "DataHora"
        ],
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce"
    )

    # EXTRAIR HORA

    df_filtrado["Hora"] = df_filtrado[
        "DataHora"
    ].dt.hour

    # CLASSIFICAR TURNO

    df_filtrado["Turno"] = df_filtrado[
        "Hora"
    ].apply(classificar_turno)

    # ==================================================
    # CLASSIFICAÇÃO DE RISCO
    # ==================================================

    df_filtrado["Risco"] = df_filtrado.apply(
        classificar_risco,
        axis=1
    )

    # ANTECEDÊNCIA

    df_filtrado["Antecedência"] = df_filtrado[
        "Hora"
    ].apply(detectar_antecedencia)

# PESQUISA GLOBAL

# ==================================================
# FILTRO DATA/HORA
# ==================================================

if "DataHora" in df_filtrado.columns:

    coluna_data = "DataHora"

# ==========================================
# LIMPEZA INTELIGENTE
# ==========================================

    df_filtrado = limpar_eventos(
        df_filtrado
    )

    # CONVERTER PARA DATETIME

    df_filtrado[coluna_data] = pd.to_datetime(
        df_filtrado[coluna_data],
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce"
    )

    # FILTRAR DATA

    if filtro_data is not None:

        df_filtrado = df_filtrado[
            df_filtrado[coluna_data].dt.date == filtro_data
        ]

    # FILTRAR HORA

    if filtro_hora:
        df_filtrado = df_filtrado[
            df_filtrado[coluna_data]
            .dt.strftime("%H:%M")
            .str.contains(filtro_hora, na=False)
        ]

if pesquisa:

    df_filtrado = df_filtrado[
        df_filtrado.astype(str).apply(
            lambda row: row.str.contains(
                pesquisa,
                case=False,
                na=False
            ).any(),
            axis=1
        )
    ]

if filtro_nome and "Nome" in df_filtrado.columns:
    df_filtrado = df_filtrado[
        df_filtrado["Nome"].str.contains(filtro_nome, case=False, na=False)
    ]

if filtro_porta and "Porta" in df_filtrado.columns:
    df_filtrado = df_filtrado[
        df_filtrado["Porta"].astype(str).str.contains(filtro_porta, na=False)
    ]

if filtro_evento != "Todos" and "Evento" in df_filtrado.columns:
    df_filtrado = df_filtrado[
        df_filtrado["Evento"].str.contains(filtro_evento, case=False, na=False)
    ]

# ==================================================
# ABAS ENTERPRISE
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executivo",
    "📡 Operacional",
    "🛡️ Segurança",
    "📋 Compliance",
    "📈 Analytics"
])

# ==================================================
# EXECUTIVO
# ==================================================

with tab1:

    render_executive_dashboard(df_filtrado)

# ==================================================
# OPERACIONAL
# ==================================================

with tab2:

    render_operational_table(df_filtrado)

# ==================================================
# SEGURANÇA
# ==================================================

with tab3:

    render_security(df_filtrado)

# ==================================================
# COMPLIANCE
# ==================================================

with tab4:

    render_compliance(df_filtrado)

# ==================================================
# ANALYTICS
# ==================================================

with tab5:

    render_charts(df_filtrado)


# ==================================================
# RODAPÉ
# ==================================================

st.markdown("""
<div class="footer">
Sentinel Access © 2026 | Developed by Yago Marinho
</div>
""", unsafe_allow_html=True)