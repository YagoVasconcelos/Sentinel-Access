import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ==================================================
# GRÁFICOS ANALÍTICOS
# ==================================================

def render_charts(df):
 
    # ==================================================
    # VALIDAR DATA
    # ==================================================

    if "DataHora" not in df.columns:

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

        st.subheader("🔥 Mapa de Calor Operacional")

        # Agrupamento estruturado
        heatmap_data = (
            df.groupby(["Porta", "Hora"])
            .size()
            .reset_index(name="Eventos")
        )

        heatmap_pivot = heatmap_data.pivot(
            index="Porta",
            columns="Hora",
            values="Eventos"
        ).fillna(0)

        # Garantir que todas as 24 horas apareçam no eixo X, mesmo se não houver acessos
        for h in range(24):
            if h not in heatmap_pivot.columns:
                heatmap_pivot[h] = 0.0
        
        heatmap_pivot = heatmap_pivot.reindex(columns=sorted(heatmap_pivot.columns))

        # Montagem do gráfico customizado
        fig_heatmap = go.Figure(
            data=go.Heatmap(
                z=heatmap_pivot.values,
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index,
                colorscale="YlOrRd",  # Escala térmica intuitiva
                xgap=2,               # Linhas sutis divisórias no eixo X
                ygap=2,               # Linhas sutis divisórias no eixo Y
                colorbar=dict(
                    title=dict(
                        text="Acessos",
                        side="top"    # <--- O 'side' agora fica aqui dentro do title
                    ),
                    thickness=15,
                    len=0.8
                ),
                hovertemplate="🚪 <b>Porta:</b> %{y}<br>⏰ <b>Hora:</b> %{x}:00h<br>📊 <b>Acessos:</b> %{z}<extra></extra>"
            )
        )

        fig_heatmap.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",  # Fundo transparente para casar com o Streamlit
            plot_bgcolor="rgba(0,0,0,0)",   # Área interna do gráfico limpa
            margin=dict(l=10, r=10, t=20, b=20),
            
            # Customização dos Textos e Eixos
            font=dict(
                family="Source Sans Pro, sans-serif",
                size=11,
                color="#E0E0E0"  # Texto claro legível no Dark Mode
            ),
            
            xaxis=dict(
                title="Horário do Dia",
                tickmode="array",
                tickvals=list(range(24)),
                ticktext=[f"{h}h" for h in range(24)],
                gridcolor="rgba(255,255,255,0.05)",
                fixedrange=True
            ),
            
            yaxis=dict(
                automargin=True,
                gridcolor="rgba(255,255,255,0.05)",
                fixedrange=True
            )
        )

        st.plotly_chart(
            fig_heatmap,
            width="stretch",
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

    fluxo_hora.columns = ["Hora", "Eventos"]

    st.markdown("---")

    st.subheader("⏱️ Fluxo por Hora")

    fig_hora = px.line(
        fluxo_hora,
        x="Hora",
        y="Eventos",
        markers=True
    )

    fig_hora.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        margin=dict(t=20, b=20),
        font=dict(color="#E0E0E0"),
        xaxis=dict(
            title="Hora", 
            tickmode="linear", 
            tick0=0, 
            dtick=1,
            gridcolor="rgba(255,255,255,0.05)"
        ),
        yaxis=dict(
            title="Quantidade de Eventos",
            gridcolor="rgba(255,255,255,0.05)"
        )
    )
    
    # Aplica uma cor moderna na linha do gráfico
    fig_hora.update_traces(line_color="#2E86C1", marker=dict(size=6, color="#5DADE2"))

    st.plotly_chart(
        fig_hora,
        width="stretch",
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

        fluxo_porta.columns = ["Porta", "Eventos"]

        st.markdown("---")

        st.subheader("🚪 Fluxo por Porta")

        fig_porta = px.bar(
            fluxo_porta,
            x="Porta",
            y="Eventos",
            text_auto=True
        )

        fig_porta.update_layout(
            height=450,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.02)",
            margin=dict(t=20, b=20),
            font=dict(color="#E0E0E0"),
            xaxis=dict(title=None),
            yaxis=dict(title="Eventos Total", gridcolor="rgba(255,255,255,0.05)")
        )
        
        fig_porta.update_traces(marker_color="#34495E")

        st.plotly_chart(
            fig_porta,
            width="stretch",
            key="grafico_fluxo_porta"
        )