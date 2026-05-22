from services.access_rules import (
    AREAS_CRITICAS
)

# ==================================================
# CLASSIFICAÇÃO DE RISCO
# ==================================================

def classificar_risco(row):

    evento = str(
        row.get("Evento", "")
    ).lower()

    porta = str(
        row.get("Porta", "")
    ).lower()

    hora = row.get("Hora", 0)

    # ==================================================
    # ÁREA CRÍTICA
    # ==================================================

    porta_critica = any(
        area in porta
        for area in AREAS_CRITICAS
    )

    # ==================================================
    # ACESSO NEGADO
    # ==================================================

    if "negado" in evento:

        return "Acesso Negado"

    # ==================================================
    # MADRUGADA + ÁREA CRÍTICA
    # ==================================================

    if porta_critica and (
        hora >= 0 and hora <= 5
    ):

        return "Movimentação Sensível"

    # ==================================================
    # ÁREA CRÍTICA
    # ==================================================

    if porta_critica:

        return "Área Crítica"

    # ==================================================
    # NORMAL
    # ==================================================

    return "Normal"