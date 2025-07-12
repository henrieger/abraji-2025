import pandas as pd
from itertools import starmap


# Manipulate and return data from LAI requests
def get_lai_data() -> pd.DataFrame:
    lai_df: pd.DataFrame = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vQs-bfRjUdT3_hJTbuhTXNw1bxipel68KBleztf9P4Wy03jubPSU8HM72Qdv9LP8JRPUVZM1xKAEIpn/pub?gid=1591698238&single=true&output=csv",
    ).rename(
        columns={
            "Texto da Pergunta": "texto",
            "Link": "link",
            "Resumo do Pedido": "resumo",
            "Órgão": "orgao",
            "Data": "data",
        }
    )
    lai_df["data"] = pd.to_datetime(lai_df["data"], format="%d/%m/%Y %H:%M:%S")

    return lai_df


# Manipulate and return data from Querido Diário
def get_qrd_data() -> pd.DataFrame:
    qrd_df: pd.DataFrame = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vSoBsSA2N9jhvCXwnoT6XwNvjJoWExi5G3hzpK7WToS7D58uXn_d8IG7bHaspZ82Z-cSktcNONUGsyZ/pub?gid=1237516333&single=true&output=csv",
    )
    qrd_df["data"] = pd.to_datetime(qrd_df["data"], format="%Y-%m-%d")
    qrd_df["orgao"] = list(
        starmap(
            lambda x, y: f"Diário Oficial de {x}-{y}",
            zip(qrd_df["municipio"], qrd_df["uf"]),
        )
    )
    del qrd_df["municipio"]
    del qrd_df["uf"]

    return qrd_df
