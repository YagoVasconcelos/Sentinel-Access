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
        "Carimbo de tempo do evento"
    )

    # ==========================================
    # DIFERENÇA ENTRE EVENTOS
    # ==========================================

    df["Diferença Segundos"] = (
        df.groupby("Nome")[
            "Carimbo de tempo do evento"
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