"""
Etapa de Transformação e Validação: tipagem estrita, verificação de chaves e integridade.
"""
from pathlib import Path
import pandas as pd
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from utils.logger import get_logger

logger = get_logger("TransformStep")

def run_transform(
    df_cliente: pd.DataFrame,
    df_tempo: pd.DataFrame,
    df_transacoes: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    logger.info("Executando transformações, higienização e validações dimensionais...")

    # Cópia defensiva
    df_c = df_cliente.copy()
    df_t = df_tempo.copy()
    df_f = df_transacoes.copy()

    # 1. Validação de Clientes
    assert df_c["id_cliente"].is_unique, "Violação de PK: id_cliente duplicado!"
    df_c["id_cliente"] = df_c["id_cliente"].astype(int)
    df_c["patrimonio_declarado"] = df_c["patrimonio_declarado"].astype(float)
    df_c["renda_mensal_declarada"] = df_c["renda_mensal_declarada"].astype(float)

    # 2. Validação de Tempo
    assert df_t["id_tempo"].is_unique, "Violação de PK: id_tempo duplicado!"
    df_t["id_tempo"] = df_t["id_tempo"].astype(int)
    df_t["ano"] = df_t["ano"].astype(int)
    df_t["mes"] = df_t["mes"].astype(int)
    df_t["dia"] = df_t["dia"].astype(int)

    # 3. Validação de Transações e Integridade Referencial (FK)
    assert df_f["id_transacao"].is_unique, "Violação de PK: id_transacao duplicada!"
    assert df_f["id_cliente"].isin(df_c["id_cliente"]).all(), "Violação de FK: cliente não encontrado!"
    assert df_f["id_tempo"].isin(df_t["id_tempo"]).all(), "Violação de FK: data não encontrada em dim_tempo!"
    
    # 4. Validação da regra temporal (60% 2027 / 40% 2025)
    anos_transacoes = pd.to_datetime(df_f["data_transferencia"]).dt.year
    contagem_anos = anos_transacoes.value_counts(normalize=True)
    prop_2027 = contagem_anos.get(2027, 0.0)
    prop_2026 = contagem_anos.get(2026, 0.0)
    prop_2025 = contagem_anos.get(2025, 0.0)
    
    logger.info(f"Validação temporal: 2027 = {prop_2027:.1%} | 2026 = {prop_2026:.1%} | 2025 = {prop_2025:.1%}")
    assert round(prop_2027, 2) == 0.25, f"Distribuição incorreta para 2027: {prop_2027}"
    assert round(prop_2026, 2) == 0.35, f"Distribuição incorreta para 2026: {prop_2026}"
    assert round(prop_2025, 2) == 0.40, f"Distribuição incorreta para 2025: {prop_2025}"

    # Padronização de tipos
    df_f["valor_dolar"] = df_f["valor_dolar"].astype(float)
    df_f["tipo_transacao"] = df_f["tipo_transacao"].astype(bool)

    logger.info("Transformações e integridade relacional concluídas com 100% de conformidade.")
    return df_c, df_t, df_f


def join_raw_tables(
    raw_dir: Path = RAW_DATA_DIR,
    output_dir: Path = PROCESSED_DATA_DIR
) -> pd.DataFrame:
    """
    Executa INNER JOIN entre as tabelas brutas dim_cliente, dim_tempo e fato_transacoes
    e salva o resultado consolidado em data/processed/transacoes_consolidadas.csv.
    """
    logger.info(f"Iniciando INNER JOIN a partir de '{raw_dir}'...")

    caminho_cliente = raw_dir / "dim_cliente.csv"
    caminho_tempo = raw_dir / "dim_tempo.csv"
    caminho_transacoes = raw_dir / "fato_transacoes.csv"

    if not caminho_cliente.exists() or not caminho_tempo.exists() or not caminho_transacoes.exists():
        raise FileNotFoundError(
            f"Tabelas brutas não encontradas em '{raw_dir}'. Execute a etapa de extração primeiro."
        )

    df_cliente = pd.read_csv(caminho_cliente)
    df_tempo = pd.read_csv(caminho_tempo)
    df_transacoes = pd.read_csv(caminho_transacoes)

    # 1. INNER JOIN fato_transacoes com dim_cliente em id_cliente
    df_join1 = df_transacoes.merge(
        df_cliente,
        on="id_cliente",
        how="inner"
    )

    # 2. INNER JOIN com dim_tempo em id_tempo
    cols_tempo = [col for col in df_tempo.columns if col != "data"]
    df_consolidada = df_join1.merge(
        df_tempo[cols_tempo],
        on="id_tempo",
        how="inner"
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    arquivo_saida = output_dir / "transacoes_consolidadas.csv"
    df_consolidada.to_csv(arquivo_saida, index=False, encoding="utf-8")

    logger.info(
        f"INNER JOIN finalizado com sucesso! Arquivo salvo em '{arquivo_saida}' "
        f"({len(df_consolidada):,} registros e {len(df_consolidada.columns)} colunas)."
    )
    return df_consolidada