"""
Etapa de Carga: persistência do resultado consolidado (INNER JOIN) na camada PROCESSED e no MySQL.
"""
from pathlib import Path
import pandas as pd
from src.config import PROCESSED_DATA_DIR

try:
    from utils.logger import get_logger
    logger = get_logger("LoadStep")
except ImportError:
    import logging
    logger = logging.getLogger("LoadStep")

try:
    from database.mysql import MySQLConnector
except ImportError:
    from database.mysql import MySQLConnector


def run_load(
    df_consolidada: pd.DataFrame,
    output_dir: Path = PROCESSED_DATA_DIR,
    sync_to_mysql: bool = True
) -> None:
    """
    Persiste os dados processados:
    1. Grava transacoes_consolidadas.csv em data/processed/
    2. Conecta no MySQL e sincroniza as transações na tabela transacoes_consolidadas
    """
    # 1. Persistência em arquivo CSV na camada processed
    logger.info(f"Persistindo dados processados (INNER JOIN) em '{output_dir}'...")
    output_dir.mkdir(parents=True, exist_ok=True)

    caminho_saida = output_dir / "transacoes_consolidadas.csv"
    df_consolidada.to_csv(caminho_saida, index=False, encoding="utf-8")

    logger.info(
        f"Arquivo '{caminho_saida.name}' salvo com sucesso ({len(df_consolidada):,} registros)."
    )

    # 2. Carga automática no Banco de Dados MySQL
    if sync_to_mysql:
        try:
            connector = MySQLConnector()
            if connector.test_connection():
                logger.info("Enviando tabela transacoes_consolidadas para o MySQL...")
                connector.insert_dataframe(
                    df=df_consolidada,
                    table_name="transacoes_consolidadas",
                    if_exists="replace",
                    chunksize=2000
                )
                logger.info("Dados carregados com sucesso no banco de dados MySQL!")
            else:
                logger.warning(
                    "Servidor MySQL não está acessível no momento. "
                    "O CSV foi salvo com sucesso em processed, mas a carga no MySQL foi postergada. "
                    "Para conectar, inicie o serviço do MySQL e confira as credenciais no arquivo .env."
                )
        except Exception as e:
            logger.warning(f"Aviso de sincronização MySQL: {e}. O arquivo CSV em processed continua intacto.")