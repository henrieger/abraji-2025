from fastapi import Depends, FastAPI, HTTPException, Header
from pydantic import BaseModel
from base64 import b64decode, b64decode, b64encode
import pandas as pd

app = FastAPI()


class LoginData(BaseModel):
    user: str
    password: str


def check_auth(authentication: str = Header()) -> None:
    auth_data = authentication.replace("token:", "")
    try:
        user, encoded_password = auth_data.split("|", 2)
    except ValueError:
        raise HTTPException(422, "Header inválido")

    logins = pd.read_csv("logins.csv", index_col="user")

    try:
        password = logins.loc[user]["password"]
    except KeyError:
        raise HTTPException(401, f"Token inválido - Usuário {user} não existe")

    if b64decode(encoded_password.encode()) != password.encode():
        raise HTTPException(401, "Token inválido - Senha incorreta")


@app.get("/")
def hello() -> dict:
    """Test endpoint for the API"""
    return {"Hello": "World!"}


def filter_df_by(df: pd.DataFrame, key: str, value: str | None) -> pd.DataFrame:
    if value is None:
        return df

    return df[df[key].map(str.lower) == value.lower()]


@app.get("/tramites")
def tramites(
    termo: str | None = None,
    orgao: str | None = None,
    autor: str | None = None,
    login: None = Depends(check_auth),
) -> dict:
    """Retorna todos os tramites que correspondem aos termos de busca fornecidos"""
    df: pd.DataFrame = pd.read_csv("data.csv")
    df = filter_df_by(df, "term", termo)
    df = filter_df_by(df, "agency", orgao)
    df = filter_df_by(df, "author", autor)
    return df.to_dict("index")


@app.get("/orgaos")
def orgaos() -> dict:
    """Retorna todos os orgaos presentes no CSV de origem"""
    df: pd.DataFrame = pd.read_csv("data.csv")
    orgaos: set = set(df["agency"])

    return {"orgaos": list(orgaos)}


@app.get("/autores")
def autores() -> dict:
    """Retorna todos os autores presentes no CSV de origem"""
    df: pd.DataFrame = pd.read_csv("data.csv")
    autores: set = set(df["authors"])

    return {"autores": list(autores)}


@app.get("/termos")
def termos() -> dict:
    """Retorna todos os termos presentes no CSV de origem, para os parâmetros de busca fornecidos"""
    df: pd.DataFrame = pd.read_csv("data.csv")
    termos: set = set(df["termos"])

    return {"termos": list(termos)}


def generate_token(user: str, password: str) -> str:
    return f"token:{user}|{b64encode(password.encode()).decode()}"


@app.post("/login")
def login(data: LoginData) -> dict:
    login_df: pd.DataFrame = pd.read_csv("logins.csv", index_col="user")

    try:
        password = login_df.loc[data.user]["password"]
    except KeyError:
        raise HTTPException(404, "Usuário não encontrado")

    if password != data.password:
        raise HTTPException(401, "Senha incorreta")

    return {"token": generate_token(data.user, data.password)}
