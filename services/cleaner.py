import pandas as pd

# ==================================================
# REMOVER EVENTOS DUPLICADOS
# ==================================================

def limpar_duplicados(df):

    if "Carimbo de tempo do evento" not in df.columns:
        return df

    # CONVERTER DATA

    df["Carimbo de tempo do evento"] = pd.to_datetime(
        df["Carimbo de tempo do evento"],
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce"
    )

    # ORDENAR

    df = df.sort_values(
        by="Carimbo de tempo do evento"
    )

    # CRIAR CHAVE

    df["Chave_Evento"] = (
        df["Nome"].astype(str) +
        df["Porta"].astype(str) +
        df["Evento"].astype(str)
    )

    # DIFERENÇA ENTRE EVENTOS

    df["Dif_Segundos"] = (
        df.groupby("Chave_Evento")[
            "Carimbo de tempo do evento"
        ]
        .diff()
        .dt.total_seconds()
    )

    # REMOVER DUPLICADOS

    df_limpo = df[
        (
            df["Dif_Segundos"].isna()
        ) |
        (
            df["Dif_Segundos"] > 5
        )
    ]

    # REMOVER COLUNAS AUXILIARES

    df_limpo = df_limpo.drop(
        columns=[
            "Chave_Evento",
            "Dif_Segundos"
        ],
        errors="ignore"
    )

    return df_limpo