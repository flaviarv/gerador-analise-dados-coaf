"""
Orquestrador central do Pipeline de Engenharia de Dados COAF.
"""
import logging
import time
from .extract import run_extract
from .transform import run_transform, join_raw_tables
from .load import run_load

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CoafPipeline")


class CoafPipeline:
    def __init__(self):
        self.logger = logger

    def run(self) -> dict:
        start_time = time.time()
        self.logger.info("Iniciando pipeline COAF...")

        # 1. Extract: Gera com Faker e salva tabelas relacionais em data/raw
        raw_clientes, raw_tempo, raw_transacoes = run_extract()

        # 2. Transform: Validação do Modelo Estrela e regra temporal 60/40
        proc_clientes, proc_tempo, proc_transacoes = run_transform(
            raw_clientes, raw_tempo, raw_transacoes
        )

        # 3. Join Dimensional: INNER JOIN a partir de data/raw
        df_consolidada = join_raw_tables()

        # 4. Load: Salva apenas o resultado do INNER JOIN em data/processed
        run_load(df_consolidada)

        elapsed = round(time.time() - start_time, 2)
        return {
            "status": "SUCCESS",
            "duracao_segundos": elapsed,
            "metricas": {
                "raw_dim_cliente": len(proc_clientes),
                "raw_dim_tempo": len(proc_tempo),
                "raw_fato_transacoes": len(proc_transacoes),
                "processed_transacoes_consolidadas": len(df_consolidada),
            }
        }