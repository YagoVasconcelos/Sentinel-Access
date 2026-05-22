import streamlit as st
import os

# ==================================================
# SIDEBAR
# ==================================================

def render_sidebar(logo, upload_folder):

    st.sidebar.image(
        logo,
        width=260
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
    # PESQUISA
    # ==================================================

    pesquisa = st.sidebar.text_input(
        "Pesquisar",
        placeholder="Nome, matrícula, porta..."
    )

    return arquivo_selecionado, pesquisa