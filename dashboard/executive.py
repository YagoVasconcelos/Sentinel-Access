import streamlit as st

# ==================================================
# DASHBOARD EXECUTIVO
# ==================================================

def render_executive_dashboard(df):

    st.subheader("📊 Dashboard Executivo")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Eventos",
        len(df)
    )

    if "Nome" in df.columns:

        col2.metric(
            "Funcionários",
            df["Nome"].nunique()
        )

    if "Porta" in df.columns:

        col3.metric(
            "Portas",
            df["Porta"].nunique()
        )

    if "Empresa" in df.columns:

        col4.metric(
            "Empresas",
            df["Empresa"].nunique()
        )

    st.markdown("---")