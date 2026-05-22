import streamlit as st

from services.anomaly_engine import (
    detectar_acessos_rapidos,
    detectar_multiplos_acessos
)

# ==================================================
# CENTRAL DE SEGURANÇA
# ==================================================

def render_security(df):

    st.markdown("""
    <div class="section-title">
    🛡️ Central de Segurança
    </div>
    """, unsafe_allow_html=True)

    # ==================================================
    # VALIDAR DADOS
    # ==================================================

    if df.empty:

        st.warning(
            "Nenhum dado carregado."
        )

        return

    # ==================================================
    # DETECÇÕES
    # ==================================================

    acessos_rapidos = detectar_acessos_rapidos(df)

    multiplos_acessos = detectar_multiplos_acessos(df)

    # ==================================================
    # KPIs
    # ==================================================

    col1, col2 = st.columns(2)

    col1.metric(
        "Acessos Rápidos",
        len(acessos_rapidos)
    )

    col2.metric(
        "Múltiplos Acessos",
        len(multiplos_acessos)
    )

    st.markdown("---")

    # ==================================================
    # ACESSOS RÁPIDOS
    # ==================================================

    st.subheader(
        "⚠️ Acessos Rápidos"
    )

    if not acessos_rapidos.empty:

        st.dataframe(
            acessos_rapidos,
            width="stretch",
            hide_index=True,
            height=250
        )

    else:

        st.success(
            "Nenhum acesso rápido detectado."
        )

    st.markdown("---")

    # ==================================================
    # MÚLTIPLOS ACESSOS
    # ==================================================

    st.subheader(
        "🚨 Múltiplos Acessos"
    )

    if not multiplos_acessos.empty:

        st.dataframe(
            multiplos_acessos,
            width="stretch",
            hide_index=True,
            height=250
        )

    else:

        st.success(
            "Nenhuma anomalia detectada."
        )