import streamlit as st

# ==================================================
# COMPLIANCE
# ==================================================

def render_compliance(df):

    st.subheader("📋 Compliance Operacional")

    st.info("""
    Módulo responsável por:
    
    • acessos fora de horário;
    • análise de permanência;
    • duplicidade operacional;
    • validação de jornada;
    • comportamento operacional.
    """)

    st.dataframe(
        df.head(50),
        width="stretch",
        hide_index=True
    )