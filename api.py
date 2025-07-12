from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import auth
import data

################
# Configuração #
################
app = FastAPI()  # Configuração da API
lai_df = data.get_lai_data()  # Dados da LAI
qrd_df = data.get_qrd_data()  # Dados do Querido Diário

# Dados concatenados para uso na API
df: pd.DataFrame = pd.concat([lai_df, qrd_df], ignore_index=True).fillna("")


@app.get("/")
async def hello() -> dict:
    """Endpoint de teste da API"""
    return {"Hello": "World!"}


#############################
# Endpoints de busca da API #
#############################


############################
# Endpoint de login da API #
############################
