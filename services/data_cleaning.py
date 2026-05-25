import pandas as pd


def limpar_eventos(df):

    # ==========================================
    # REMOVE DUPLICIDADE EXATA
    # ==========================================

    df = df.drop_duplicates()

    # ==========================================
    # ORDENA POR DATA
    # ==========================================

    df = df.sort_values(
        "DataHora"
    )

    # ==========================================
    # DIFERENÇA ENTRE EVENTOS
    # ==========================================

    df["Diferença Segundos"] = (
        df.groupby("Nome")[
            "DataHora"
        ]
        .diff()
        .dt.total_seconds()
    )

    # ==========================================
    # REMOVE ECO DE LEITURA
    # ==========================================

    df = df[
        ~(
            (df["Diferença Segundos"] <= 2)
            &
            (df["Porta"] ==
             df["Porta"].shift())
        )
    ]

    return df