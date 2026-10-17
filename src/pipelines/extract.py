"""
Etapa de Extração / Geração: produz dados brutos e persiste em data/raw/.
"""
from pathlib import Path
import pandas as pd
from src.config import RAW_DATA_DIR
from src.generators.client_generator import generate_dim_cliente
from src.generators.transaction_generator import generate_fato_transacoes
from src.generators.time_generator import generate_dim_tempo
from utils.logger import get_logger

logger = get_logger("ExtractStep")

def run_extract(output_dir: Path = RAW_DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    logger.info("Iniciando extração e geração de dados com Faker...")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Clientes
    df_cliente = generate_dim_cliente()
    logger.info(f"dim_cliente gerada: {len(df_cliente)} registros.")

    # 2. Transações
    df_transacoes = generate_fato_transacoes()
    logger.info(f"fato_transacoes gerada: {len(df_transacoes)} registros.")

    # 3. Tempo
    datas_unicas = df_transacoes["data_transferencia"].unique().tolist()
    df_tempo = generate_dim_tempo(datas_unicas)
    logger.info(f"dim_tempo gerada: {len(df_tempo)} dias únicos catalogados.")

    # Persistência na camada RAW
    df_cliente.to_csv(output_dir / "dim_cliente.csv", index=False, encoding="utf-8")
    df_tempo.to_csv(output_dir / "dim_tempo.csv", index=False, encoding="utf-8")
    df_transacoes.to_csv(output_dir / "fato_transacoes.csv", index=False, encoding="utf-8")
    logger.info(f"Dados brutos armazenados com sucesso em '{output_dir}'.")

    return df_cliente, df_tempo, df_transacoes