import os
import ssl

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from models import Base

load_dotenv()


def criar_engine(tipo: str):
    if tipo == "sqlite":
        engine = create_engine("sqlite:///dados.db")
    elif tipo == "mysql":
        campos = ["MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST",
                  "MYSQL_PORT", "MYSQL_DATABASE"]
        faltando = [c for c in campos if not os.getenv(c)]
        if faltando:
            raise RuntimeError(f"Variáveis ausentes no .env: {', '.join(faltando)}")

        url = URL.create(
            "mysql+pymysql",
            username=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            database=os.getenv("MYSQL_DATABASE"),
        )
        # Aiven exige TLS
        ctx = ssl.create_default_context(cafile=os.getenv("MYSQL_SSL_CA") or None)
        if not os.getenv("MYSQL_SSL_CA"):
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        engine = create_engine(url, connect_args={"ssl": ctx}, pool_pre_ping=True)
    else:
        raise ValueError("Tipo de banco inválido")

    Base.metadata.create_all(engine)  # testa a conexão e cria as tabelas
    return engine


def abrir_sessao(engine) -> Session:
    return Session(engine)