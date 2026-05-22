import pandas as pd
import os

# ==================================================
# CARREGAR CSV ROBUSTO
# ==================================================

def carregar_csv(upload_folder, arquivo):

    file_path = os.path.join(
        upload_folder,
        arquivo
    )

    # ==================================================
    # LEITURA ROBUSTA
    # ==================================================

    try:

        df = pd.read_csv(
            file_path,
            sep=",",
            encoding="utf-8",
            engine="python",
            on_bad_lines="skip"
        )

    except:

        try:

            df = pd.read_csv(
                file_path,
                sep=";",
                encoding="latin1",
                engine="python",
                on_bad_lines="skip"
            )

        except Exception as e:

            raise Exception(
                f"Erro ao ler CSV: {e}"
            )

    # ==================================================
    # REMOVER COLUNAS VAZIAS
    # ==================================================

    df = df.dropna(
        axis=1,
        how="all"
    )

    # ==================================================
    # REMOVER LINHAS TOTALMENTE VAZIAS
    # ==================================================

    df = df.dropna(
        how="all"
    )

    # ==================================================
    # LIMPAR NOMES DAS COLUNAS
    # ==================================================

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    # ==================================================
    # REMOVER DUPLICIDADE DE CABEÇALHO
    # ==================================================

    if len(df) > 0:

        primeira_linha = list(
            df.iloc[0].astype(str)
        )

        colunas = list(
            df.columns.astype(str)
        )

        if primeira_linha == colunas:

            df = df.iloc[1:]

    # ==================================================
    # RESET INDEX
    # ==================================================

    df = df.reset_index(drop=True)

    return df
