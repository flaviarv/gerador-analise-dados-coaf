"""
Módulo de Conexão e Operações com Banco de Dados MySQL.
Padrão de Engenharia de Dados: Conexão resiliente via SQLAlchemy e PyMySQL com pooling.
"""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import pandas as pd

# Tentativa de carregar dotenv se instalado
try:
    from dotenv import load_dotenv
    # Carrega .env da raiz do projeto
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

try:
    from utils.logger import get_logger
    logger = get_logger("MySQLDatabase")
except ImportError:
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger("MySQLDatabase")


@dataclass
class MySQLConfig:
    """Configurações de conexão extraídas de variáveis de ambiente com defaults seguros."""
    host: str = os.getenv("MYSQL_HOST")
    port: int = int(os.getenv("MYSQL_PORT"))
    user: str = os.getenv("MYSQL_USER")
    password: str = os.getenv("MYSQL_PASSWORD")
    database: str = os.getenv("MYSQL_DATABASE")
    charset: str = os.getenv("MYSQL_CHARSET")

    @property
    def connection_url(self) -> str:
        """Monta a URL de conexão padrão SQLAlchemy (mysql+pymysql)."""
        auth = self.user
        if self.password:
            auth += f":{self.password}"
        return f"mysql+pymysql://{auth}@{self.host}:{self.port}/{self.database}?charset={self.charset}"


class MySQLConnector:
    """
    Gerenciador de conexão com o MySQL para o Pipeline de Dados COAF.
    Permite teste de conectividade, execução de scripts DDL e carga de DataFrames.
    """

    def __init__(self, config: Optional[MySQLConfig] = None):
        self.config = config or MySQLConfig()
        self._engine = None

    def get_engine(self):
        """Retorna a engine SQLAlchemy com Connection Pooling ativado."""
        if self._engine is None:
            try:
                from sqlalchemy import create_engine
                self._engine = create_engine(
                    self.config.connection_url,
                    pool_pre_ping=True,      # Valida a conexão antes de usar (evita conexões mortas)
                    pool_recycle=3600,       # Recicla conexões a cada 1 hora
                    pool_size=5,             # Tamanho do pool
                    max_overflow=10          # Conexões extras permitidas em pico
                )
                logger.info(f"Engine MySQL inicializada com sucesso ({self.config.host}:{self.config.port}/{self.config.database}).")
            except ImportError as e:
                logger.error("Pacote 'sqlalchemy' ou 'pymysql' não encontrado. Instale com: pip install sqlalchemy pymysql")
                raise e
        return self._engine

    def test_connection(self) -> bool:
        """Testa se a conexão com o banco está ativa e respondendo."""
        try:
            from sqlalchemy import text
            engine = self.get_engine()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).scalar()
                if result == 1:
                    logger.info("Conexão com o banco MySQL estabelecida com sucesso! (Ping: OK)")
                    return True
        except Exception as e:
            logger.error(f"Falha ao conectar no MySQL ({self.config.host}:{self.config.port}/{self.config.database}): {e}")
            return False
        return False

    def execute_script(self, script_path: Path) -> None:
        """Executa um arquivo .sql no banco (ex: database/mysql.sql)."""
        if not script_path.exists():
            raise FileNotFoundError(f"Script SQL não encontrado: {script_path}")

        logger.info(f"Executando script SQL: {script_path.name}...")
        engine = self.get_engine()

        with open(script_path, "r", encoding="utf-8") as f:
            sql_content = f.read()

        # Divide comandos por ';' para execução sequencial
        commands = [cmd.strip() for cmd in sql_content.split(";") if cmd.strip()]

        from sqlalchemy import text
        with engine.begin() as conn:
            for cmd in commands:
                conn.execute(text(cmd))

        logger.info(f"Script {script_path.name} executado com sucesso.")

    def insert_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = "append", chunksize: int = 1000) -> int:
        """
        Insere um DataFrame do pandas diretamente em uma tabela do MySQL.
        Usa inserções em lote (chunks) para alta performance de escrita.
        """
        logger.info(f"Gravando {len(df):,} linhas na tabela '{table_name}' (if_exists='{if_exists}')...")
        engine = self.get_engine()
        with engine.begin() as conn:
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists=if_exists,
                index=False,
                chunksize=chunksize
            )
        logger.info(f"Gravação concluída na tabela '{table_name}'.")
        return len(df)

    def query_to_dataframe(self, sql_query: str) -> pd.DataFrame:
        """Executa uma consulta SELECT no MySQL e retorna como DataFrame do pandas."""
        logger.info("Executando consulta SQL e convertendo para DataFrame...")
        engine = self.get_engine()
        return pd.read_sql(sql_query, con=engine)


# Instância pronta para uso rápido
db_connector = MySQLConnector()

if __name__ == "__main__":
    print("Testando conexão com o banco MySQL...")
    connector = MySQLConnector()
    connector.test_connection()
