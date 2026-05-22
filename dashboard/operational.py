import streamlit as st

# ==================================================
# TABELA OPERACIONAL
# ==================================================

def render_operational_table(df):

    st.subheader("📡 Eventos Operacionais")

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        height=500
    )