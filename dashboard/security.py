import streamlit as st
import pandas as pd

from services.anomaly_engine import (
    detectar_acessos_rapidos,
    detectar_multiplos_acessos
)

# ==================================================
# CENTRAL DE SEGURANÇA
# ==================================================

def render_security(df):

    st.markdown("""
    

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
    # MÚLTIPLOS ACESSOS (AGRUPADO COM CLASSIFICAÇÃO)
    # ==================================================

    st.subheader(
        "🚨 Múltiplos Acessos"
    )

    if not multiplos_acessos.empty:
        
        # Garante que temos as colunas necessárias para agrupar por Nome e Sobrenome
        if "Nome" in multiplos_acessos.columns and "Sobrenome" in multiplos_acessos.columns:
            
            # 1. Agrupa para obter a quantidade exata por pessoa
            df_agrupado = multiplos_acessos.groupby(['Nome', 'Sobrenome']).size().reset_index(name='Quantidade')
            
            # 2. Função interna para definir o tipo de quebra ou suspeita baseado no DataFrame original
            def mapear_comportamento(row):
                # Busca o histórico completo deste usuário específico no df original
                historico = df[(df['Nome'] == row['Nome']) & (df['Sobrenome'] == row['Sobrenome'])]
                
                # Regra 1: Verifica se o motor de risco marcou como Crítico/Alto
                if 'Risco' in historico.columns and historico['Risco'].isin(['Alto', 'Crítico', 'Critico']).any():
                    return "🚨 Atividade Suspeita"
                
                # Regra 2: Verifica se possui eventos de acesso negado
                if 'Evento' in historico.columns and historico['Evento'].str.contains('Negado', case=False, na=False).any():
                    return "🚷 Quebra de Acesso"
                
                # Regra 3: Caso possua uma quantidade muito alta de batidas agregadas
                if row['Quantidade'] > 15:
                    return "⚠️ Fluxo Anômalo"
                
                # Padrão
                return "ℹ️ Falha / Acesso Repetitivo"
            
            # Aplica a classificação na nova coluna
            df_agrupado['Classificação'] = df_agrupado.apply(mapear_comportamento, axis=1)
            
            # Ordena pelos usuários com maior volume de alertas
            df_exibicao = df_agrupado.sort_values(by='Quantidade', ascending=False)
            
            # Renderiza a tabela final estruturada com Nome, Sobrenome, Quantidade e Classificação
            st.dataframe(
                df_exibicao[['Nome', 'Sobrenome', 'Quantidade', 'Classificação']],
                width="stretch",
                hide_index=True,
                height=250
            )
            
        else:
            # Caso a estrutura de colunas do retorno seja diferente, exibe o dataframe padrão modificado
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