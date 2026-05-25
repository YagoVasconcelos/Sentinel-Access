import streamlit as st
import os

# ==================================================
# SIDEBAR
# ==================================================

def render_sidebar(logo, upload_folder):

    # 1. INJEÇÃO DIRETA ADAPTADA PARA AS DIVS NATIVAS DO STREAMLIT
    st.sidebar.markdown(
        """
        <style>
            /* Arranca o bloco invisível de padding superior que empurra os elementos */
            div[data-testid="stSidebarUserContent"] > div {
                padding-top: 0rem !important;
            }
            
            /* Cola o primeiro bloco (o container da logo) no teto real */
            div[data-testid="stSidebarUserContent"] [data-testid="element-container"]:first-child {
                margin-top: -50px !important;
                padding-left: 0rem !important;
                padding-right: 0rem !important;
            }
            
            /* Força a imagem a ignorar margens e se expandir pelas laterais */
            div[data-testid="stSidebarUserContent"] .stImage img {
                width: 100% !important;
                max-width: 100% !important;
                height: auto !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 2. RENDERIZAÇÃO DA LOGO COM A SINTAXE NOVA DO STREAMLIT
    st.sidebar.image(
        logo,
        width="stretch"
    )

    st.sidebar.divider()

    # ==================================================
    # UPLOAD CSV
    # ==================================================

    uploaded_file = st.sidebar.file_uploader(
        "Importar CSV Genetec",
        type=["csv"]
    )

    # ==================================================
    # SALVAR CSV
    # ==================================================

    if uploaded_file is not None:

        file_path = os.path.join(
            upload_folder,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(
                uploaded_file.getbuffer()
            )

        st.sidebar.success(
            "Arquivo importado com sucesso"
        )

    # ==================================================
    # HISTÓRICO
    # ==================================================

    arquivos_csv = [
        f for f in os.listdir(upload_folder)
        if f.endswith(".csv")
    ]

    arquivo_selecionado = st.sidebar.selectbox(
        "Histórico de Arquivos",
        arquivos_csv
    )

    # ==================================================
    # PESQUISA UNIFICADA COM CALENDÁRIO
    # ==================================================

    st.sidebar.markdown("### Pesquisar")

    # Criamos as colunas acopladas na sidebar de forma nativa
    busca_col1, busca_col2 = st.sidebar.columns([4, 1])

    with busca_col1:
        pesquisa = st.text_input(
            "Pesquisar",
            placeholder="Nome, matrícula, porta...",
            label_visibility="collapsed"  # Oculta a label redundante
        )

    with busca_col2:
        with st.popover("📅"):
            st.markdown("#### Filtrar Período")
            usar_data = st.checkbox("Usar Data", key="side_chk_data")

            if usar_data:
                filtro_data = st.date_input("Selecionar Data")
            else:
                filtro_data = None

            usar_hora = st.checkbox("Usar Hora", key="side_chk_hora")

            if usar_hora:
                filtro_hora = st.text_input("Hora", placeholder="Ex: 14:30")
            else:
                filtro_hora = None

            if st.button("Limpar Filtros", width="stretch"):
                st.rerun()

    # Retorna todas as variáveis coletadas para o app.py gerenciar os filtros globais
    return arquivo_selecionado, pesquisa, filtro_data, filtro_hora