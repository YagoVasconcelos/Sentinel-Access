import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ==================================================
# GRÁFICOS ANALÍTICOS
# ==================================================

def render_charts(df):

    st.subheader("📈 Analytics Operacional")

    # ==================================================
    # VALIDAR DATA
    # ==================================================

    if "Carimbo de tempo do evento" not in df.columns:

        st.warning(
            "Coluna de data não encontrada."
        )

        return
    
    # ==================================================
    # HEATMAP OPERACIONAL
    # ==================================================

    if (
        "Hora" in df.columns and
        "Porta" in df.columns
    ):

        st.markdown("---")

        st.subheader("🔥 Heatmap Operacional")

        heatmap_data = (
            df.groupby(
                ["Porta", "Hora"]
            )
            .size()
            .reset_index(name="Eventos")
        )

        heatmap_pivot = heatmap_data.pivot(
            index="Porta",
            columns="Hora",
            values="Eventos"
        ).fillna(0)

        fig_heatmap = go.Figure(
            data=go.Heatmap(
                z=heatmap_pivot.values,
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index
            )
        )

        fig_heatmap.update_layout(

            height=320,

            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),

            xaxis_title=None,
            yaxis_title=None,

            font=dict(
                size=10
            ),

            yaxis=dict(
                automargin=True
            )
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True,
            key="heatmap_operacional"
        )

    # ==================================================
    # FLUXO POR HORA
    # ==================================================

    fluxo_hora = (
        df["Hora"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    fluxo_hora.columns = [
        "Hora",
        "Eventos"
    ]

    st.markdown("---")

    st.subheader("⏱️ Fluxo por Hora")

    fig_hora = px.line(
        fluxo_hora,
        x="Hora",
        y="Eventos",
        markers=True
    )

    fig_hora.update_layout(
        height=500,
        xaxis_title="Hora",
        yaxis_title="Quantidade de Eventos"
    )

    st.plotly_chart(
        fig_hora,
        use_container_width=True,
        key="grafico_fluxo_hora"
    )

    # ==================================================
    # FLUXO POR PORTA
    # ==================================================

    if "Porta" in df.columns:

        fluxo_porta = (
            df["Porta"]
            .value_counts()
            .reset_index()
        )

        fluxo_porta.columns = [
            "Porta",
            "Eventos"
        ]

        st.markdown("---")

        st.subheader("🚪 Fluxo por Porta")

        fig_porta = px.bar(
            fluxo_porta,
            x="Porta",
            y="Eventos",
            text_auto=True
        )

        fig_porta.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_porta,
            use_container_width=True,
            key="grafico_fluxo_porta"
        )