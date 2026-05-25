import pandas as pd
import re

# ==================================================
# PALAVRAS LIXO
# ==================================================

PALAVRAS_REMOVER = [

    "S/A",
    "SA",
    "LTDA",
    "EIRELI",
    "ME",
    "EPP",
    "FILIAL",
    "UNIDADE",
    "&CO",
    "& CO",
    "DO BRASIL",
    "BRASIL",
    "INDUSTRIA",
    "INDÚSTRIA",
    "IND",
    "CIA",
    "COMPANY"

]

# ==================================================
# NORMALIZAR EMPRESA
# ==================================================

def normalizar_empresa(nome):

    if pd.isna(nome):

        return "NÃO INFORMADO"

    # ==================================================
    # STRING
    # ==================================================

    nome = str(nome).upper().strip()

    # ==================================================
    # REMOVER CARACTERES
    # ==================================================

    nome = re.sub(
        r"[^A-Z0-9\s]",
        "",
        nome
    )

    # ==================================================
    # REMOVER PALAVRAS LIXO
    # ==================================================

    for palavra in PALAVRAS_REMOVER:

        nome = nome.replace(
            palavra,
            ""
        )

    # ==================================================
    # REMOVER ESPAÇOS DUPLOS
    # ==================================================

    nome = " ".join(
        nome.split()
    )

    # ==================================================
    # PEGAR NÚCLEO PRINCIPAL
    # ==================================================

    partes = nome.split()

    if len(partes) >= 1:

        nome = partes[0]

    return nome