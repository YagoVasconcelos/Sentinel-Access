import pandas as pd

# ==================================================
# CLASSIFICADOR DE TURNOS
# ==================================================

def classificar_turno(hora):

    if pd.isna(hora):
        return "Não identificado"

    # ==================================================
    # ADM
    # ==================================================

    if 6 <= hora < 17:
        return "ADM"

    # ==================================================
    # 1º TURNO
    # ==================================================

    elif 5 <= hora < 15:
        return "1º Turno"

    # ==================================================
    # 2º TURNO
    # ==================================================

    elif 13 <= hora < 23:
        return "2º Turno"

    # ==================================================
    # 3º TURNO
    # ==================================================

    else:
        return "3º Turno"


# ==================================================
# DETECÇÃO DE ACESSO ANTECIPADO
# ==================================================

def detectar_antecedencia(hora):

    if pd.isna(hora):
        return "Não identificado"

    # Vigilantes chegando muito cedo

    if 2 <= hora <= 5:
        return "Antecedência Elevada"

    elif 5 <= hora <= 6:
        return "Antecedência Normal"

    else:
        return "Dentro do Horário"
    