from base64 import b64encode, b64decode
from fastapi import Header, HTTPException
import pandas as pd
import binascii


"""DataFrame with user data. THIS IS A BAD PRACTICE!!!!!"""
login_df: pd.DataFrame = pd.read_csv(
    "https://raw.githubusercontent.com/henrieger/abraji-2025/refs/heads/main/logins.csv",
    index_col="user",
)


def generate_token(user: str, password: str) -> str:
    """Generate a token from user data"""
    return b64encode(f"token:{user}|{password}".encode()).decode()


def check_token(authentication: str = Header()) -> None:
    """Check if passed token is from valid user. Errors out in case of mismatch"""
    try:
        auth_data: str = b64decode(authentication.encode()).decode()
        user, password = auth_data.replace("token:", "").split("|", 3)
    except (ValueError, binascii.Error):
        raise HTTPException(422, "Header inválido")

    try:
        registered_password = login_df.loc[user]["password"]
    except KeyError:
        raise HTTPException(401, f"Token inválido - Usuário {user} não existe")

    if registered_password != password:
        raise HTTPException(401, "Token inválido - Senha incorreta")
