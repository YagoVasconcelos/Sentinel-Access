import streamlit as st
import plotly.express as px
import pandas as pd

from services.site_presence import (
    consolidar_presenca
)

# ==================================================
# DASHBOARD EXECUTIVO
# ==================================================

def render_executive_dashboard(df):

    st.subheader(
        "📊 Dashboard Executivo"
    )

    # ==================================================
    # CONSOLIDAR
    # ==================================================

    presenca = consolidar_presenca(df)

    # ==================================================
    # METRICAS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    # EVENTOS
    col1.metric(
        "Eventos",
        len(df)
    )

    # COLABORADORES
    total_colaboradores = 0
    if not presenca.empty:
        total_colaboradores = (
            presenca["Matrícula"]
            .nunique()
        )

    col2.metric(
        "Colaboradores",
        total_colaboradores
    )

    # EMPRESAS
    total_empresas = 0
    if not presenca.empty:
        total_empresas = (
            presenca["Empresa"]
            .nunique()
        )

    col3.metric(
        "Empresas",
        total_empresas
    )

    # PORTARIAS
    total_portarias = 0
    if "Porta" in df.columns:
        total_portarias = (
            df["Porta"]
            .nunique()
        )

    col4.metric(
        "Portarias",
        total_portarias
    )

    st.markdown("---")

    # ==================================================
    # GRAFICO EMPRESAS
    # ==================================================

    if not presenca.empty:

        # ==================================================
        # NORMALIZAR EMPRESAS
        # ==================================================
        def normalizar_empresa(nome):
            if pd.isna(nome):
                return "Não Informado"

            nome = str(nome).upper().strip()

            if "NATURA" in nome:
                return "NATURA"
            if "GPS" in nome:
                return "GPS"
            if "GRSA" in nome:
                return "GRSA"
            if "SODEXO" in nome:
                return "SODEXO"

            return nome

        # Aplica a normalização na base consolidada antes de agrupar
        presenca["Empresa"] = presenca["Empresa"].apply(normalizar_empresa)

        # ==================================================
        # AGRUPAR E CONTAR COLABORADORES ÚNICOS
        # ==================================================
        empresa_count = (
            presenca.groupby("Empresa")["Matrícula"]
            .nunique()
            .reset_index()
        )
        empresa_count.columns = ["Empresa", "Colaboradores"]

        # Ordenar do maior para o menor (garante que as barras maiores fiquem no topo)
        empresa_count = empresa_count.sort_values("Colaboradores", ascending=True)

        # ==================================================
        # LAYOUT DO TITULO + TOTAL GERAL DO GRÁFICO
        # ==================================================
        col_tit, col_met = st.columns([3, 1])
        with col_tit:
            st.subheader("🏭 Colaboradores por Empresa")
        with col_met:
            # Mostra o indicador de Total Geral destacado logo acima do gráfico
            st.metric(label="Total Geral", value=f"{total_colaboradores} un.")

        # ==================================================
        # CONFIGURAÇÃO VISUAL DO PLOTLY
        # ==================================================
        fig = px.bar(
            empresa_count,
            x="Colaboradores",
            y="Empresa",
            orientation="h",
            text="Colaboradores",
            color="Empresa"
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False  # Impede que o número final da barra fique cortado
        )

        fig.update_layout(
            height=500,  # Reduzido de 900 para 500 para evitar barras esticadas demais
            paper_bgcolor="rgba(0,0,0,0)",  # Transparência dark mode
            plot_bgcolor="rgba(255,255,255,0.02)",
            showlegend=False,  # Ocultado legenda lateral porque o eixo Y já tem os nomes das empresas
            
            font=dict(
                family="Source Sans Pro, sans-serif",
                size=12,
                color="#E0E0E0"
            ),
            
            xaxis=dict(
                title="Quantidade de Colaboradores Únicos",
                gridcolor="rgba(255,255,255,0.05)"
            ),
            
            yaxis=dict(
                title=None,
                categoryorder="total ascending"  # Ordenação visual correta de leitura
            ),
            
            margin=dict(l=20, r=40, t=20, b=20)
        )

        st.plotly_chart(
            fig,
            width="stretch",
            key="grafico_empresas"
        )

        st.markdown("---")

        # ==================================================
        # TABELA CONSOLIDADA
        # ==================================================

        st.subheader(
            "👥 Colaboradores que Acessaram o Site"
        )

        colunas_exibir = [
            "Data",
            "Matrícula",
            "Nome",
            "Sobrenome",
            "Empresa",
            "Primeira Entrada",
            "Última Saída",
            "Eventos"
        ]

        st.dataframe(
            presenca[colunas_exibir],
            width="stretch",
            hide_index=True,
            height=500
        )

    else:

        st.warning(
            "Nenhum dado consolidado encontrado."
        )