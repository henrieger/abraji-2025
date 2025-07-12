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
@app.get("/busca")
async def busca(
    orgao: str | None = None,
    texto: str | None = None,
    login: None = Depends(auth.check_token),
):
    """Busca tramitações conforme filtros do usuário"""
    filter_df = df
    if orgao is not None:
        filter_df = filter_df[filter_df["orgao"] == orgao]
    if texto is not None:
        filter_df = filter_df[texto in filter_df["texto"]]
    return df.to_dict(orient="records")


@app.get("/orgaos")
async def orgaos():
    """Retorna todos os órgãos disponibilizados pela API"""
    return {"orgaos": set(df["orgao"])}


############################
# Endpoint de login da API #
############################
class LoginData(BaseModel):
    user: str
    password: str


@app.post("/login")
async def login(data: LoginData) -> dict:
    """Return a login token for authenticated users"""
    try:
        password = auth.login_df.loc[data.user]["password"]
    except KeyError:
        raise HTTPException(404, "Usuário não encontrado")

    if password != data.password:
        raise HTTPException(401, "Senha incorreta")

    return {"token": auth.generate_token(data.user, data.password)}
