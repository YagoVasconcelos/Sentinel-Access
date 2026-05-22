import streamlit as st
from PIL import Image
import pandas as pd
import os

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

if logo:
    st.sidebar.image(logo, width=260)

st.sidebar.divider()

# UPLOAD
uploaded_file = st.sidebar.file_uploader(
    "Importar CSV Genetec",
    type=["csv"]
)

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success("Arquivo salvo com sucesso!")

st.sidebar.divider()

# HISTÓRICO
arquivos_csv = [
    f for f in os.listdir(UPLOAD_FOLDER)
    if f.endswith(".csv")
]

arquivo_selecionado = st.sidebar.selectbox(
    "Histórico de arquivos",
    arquivos_csv if arquivos_csv else ["Nenhum arquivo"]
)

st.sidebar.divider()

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

if arquivo_selecionado and arquivo_selecionado != "Nenhum arquivo":

    file_path = os.path.join(
        UPLOAD_FOLDER,
        arquivo_selecionado
    )

    try:

        df = pd.read_csv(
            file_path,
            sep=",",
            encoding="utf-8",
            quotechar='"',
            skipinitialspace=True
        )

    except Exception as e:

        st.error(
            f"Erro ao carregar CSV: {e}"
        )

# ==================================================
# FILTROS SOC
# ==================================================

st.subheader("🔎 Filtros SOC")

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

# PESQUISA GLOBAL

# ==================================================
# FILTRO DATA/HORA
# ==================================================

if "Carimbo de tempo do evento" in df_filtrado.columns:

    coluna_data = "Carimbo de tempo do evento"

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
# DASHBOARD SOC
# ==================================================

st.subheader("📡 Eventos em Tempo Quase Real")

# Remove colunas totalmente vazias
df_filtrado = df_filtrado.dropna(
    axis=1,
    how="all"
)

if "Carimbo de tempo do evento" in df_filtrado.columns:

    st.dataframe(
        df_filtrado.sort_values(
            "Carimbo de tempo do evento",
            ascending=False
        ),
        width="stretch",
        hide_index=True,
        height=500
    )

else:

    st.dataframe(
        df_filtrado,
        width="stretch",
        hide_index=True,
        height=500
    )

# ==================================================
# RESUMO
# ==================================================

st.subheader("Resumo Operacional")

st.info("""
Sentinel Access monitora eventos operacionais
exportados do Genetec Security Desk.
""")


# ==================================================
# RODAPÉ
# ==================================================

st.markdown("""
<div class="footer">
Sentinel Access © 2026 | Developed by Yago Marinho
</div>
""", unsafe_allow_html=True)