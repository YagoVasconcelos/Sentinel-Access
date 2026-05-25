import pandas as pd

from services.access_rules import (
    LIMITE_ACESSO_RAPIDO,
    LIMITE_MULTIPLOS_ACESSOS
)

# ==================================================
# DETECTAR ACESSOS RÁPIDOS
# ==================================================

def detectar_acessos_rapidos(df):

    resultados = []

    if (
        "Nome" not in df.columns or
        "DataHora" not in df.columns
    ):
        return pd.DataFrame()

    for nome, grupo in df.groupby("Nome"):

        grupo = grupo.sort_values(
            "DataHora"
        )

        grupo["Diferença"] = grupo[
            "DataHora"
        ].diff().dt.total_seconds()

        suspeitos = grupo[
            grupo["Diferença"]
            < LIMITE_ACESSO_RAPIDO
        ]

        if not suspeitos.empty:

            resultados.append(
                suspeitos
            )

    if resultados:

        return pd.concat(resultados)

    return pd.DataFrame()

# ==================================================
# DETECTAR MÚLTIPLOS ACESSOS
# ==================================================

def detectar_multiplos_acessos(df):

    if "Nome" not in df.columns:

        return pd.DataFrame()

    contagem = (
        df["Nome"]
        .value_counts()
        .reset_index()
    )

    contagem.columns = [
        "Nome",
        "Quantidade"
    ]

    suspeitos = contagem[
        contagem["Quantidade"]
        >= LIMITE_MULTIPLOS_ACESSOS
    ]

    return suspeitos