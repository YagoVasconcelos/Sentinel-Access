import pandas as pd
from services.company_normalizer import (normalizar_empresa)

# ==================================================
# PORTARIAS PRINCIPAIS
# ==================================================

PORTARIAS_PRINCIPAIS = [

    "portaria 1",
    "portaria 2"

]

# ==================================================
# VALIDAR PORTARIA
# ==================================================

def eh_portaria_principal(porta):

    if pd.isna(porta):
        return False

    porta = str(porta).lower()

    return any(
        p in porta
        for p in PORTARIAS_PRINCIPAIS
    )

# ==================================================
# ENTRADA
# ==================================================

def eh_entrada(porta):

    if pd.isna(porta):
        return False

    porta = str(porta).lower()

    return "entrada" in porta

# ==================================================
# SAÍDA
# ==================================================

def eh_saida(porta):

    if pd.isna(porta):
        return False

    porta = str(porta).lower()

    return (
        "saida" in porta
        or "saída" in porta
    )

# ==================================================
# CONSOLIDAR PRESENÇA
# ==================================================

def consolidar_presenca(df):

    colunas_necessarias = [

        "Nome",
        "Sobrenome",
        "Matrícula",
        "Porta",
        "DataHora"

    ]

    for coluna in colunas_necessarias:

        if coluna not in df.columns:
            return pd.DataFrame()

    # ==================================================
    # CÓPIA
    # ==================================================

    df = df.copy()

    # ==================================================
    # DATETIME
    # ==================================================

    df["DataHora"] = pd.to_datetime(
        df["DataHora"],
        errors="coerce"
    )

    # ==================================================
    # REMOVER NULOS
    # ==================================================

    df = df.dropna(
        subset=[
            "Nome",
            "Porta",
            "DataHora"
        ]
    )

    # ==================================================
    # FILTRAR PORTARIAS
    # ==================================================

    df = df[
        df["Porta"].apply(
            eh_portaria_principal
        )
    ]

    # ==================================================
    # DATA
    # ==================================================

    df["Data"] = df[
        "DataHora"
    ].dt.date

    # ==================================================
    # RESULTADO
    # ==================================================

    resultado = []

    # ==================================================
    # AGRUPAR
    # ==================================================

    grupos = df.groupby([

        "Matrícula",
        "Data"

    ])

    # ==================================================
    # LOOP
    # ==================================================

    for (matricula, data), grupo in grupos:

        grupo = grupo.sort_values(
            "DataHora"
        )

        nome = grupo["Nome"].iloc[0]

        sobrenome = grupo[
            "Sobrenome"
        ].iloc[0]

        empresa = "-"

        if "Empresa" in grupo.columns:

            empresa = normalizar_empresa(grupo["Empresa"].iloc[0])

        # ==================================================
        # ENTRADAS
        # ==================================================

        entradas = grupo[
            grupo["Porta"].apply(
                eh_entrada
            )
        ]

        # ==================================================
        # SAÍDAS
        # ==================================================

        saidas = grupo[
            grupo["Porta"].apply(
                eh_saida
            )
        ]

        # ==================================================
        # PRIMEIRA ENTRADA
        # ==================================================

        primeira_entrada = "-"

        if not entradas.empty:

            primeira_entrada = (
                entradas["DataHora"]
                .min()
                .strftime("%H:%M:%S")
            )

        # ==================================================
        # ÚLTIMA SAÍDA
        # ==================================================

        ultima_saida = "-"

        if not saidas.empty:

            ultima_saida = (
                saidas["DataHora"]
                .max()
                .strftime("%H:%M:%S")
            )

        # ==================================================
        # TOTAL EVENTOS
        # ==================================================

        total_eventos = len(grupo)

        # ==================================================
        # RESULTADO
        # ==================================================

        resultado.append({

            "Data":
                data,

            "Matrícula":
                matricula,

            "Nome":
                nome,

            "Sobrenome":
                sobrenome,

            "Empresa":
                empresa,

            "Primeira Entrada":
                primeira_entrada,

            "Última Saída":
                ultima_saida,

            "Eventos":
                total_eventos

        })

    # ==================================================
    # DATAFRAME FINAL
    # ==================================================

    presenca = pd.DataFrame(
        resultado
    )

    if not presenca.empty:

        presenca = presenca.sort_values(
            [
                "Data",
                "Nome"
            ]
        )

    return presenca