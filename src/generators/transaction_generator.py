"""
Gerador da tabela fato_transacoes (40.000 transações).
Regra: 60% gerado em 2027 (24.000) e 40% gerado em 2025 (16.000).
"""
from datetime import date, timedelta
import numpy as np
import pandas as pd
from src.config import (
    TOTAL_CLIENTS,
    TOTAL_TRANSACTIONS,
    RATIO_2027,
    RATIO_2026,
    RATIO_2025,
    RANDOM_SEED,
    CRYPTO_ASSETS,
    CRYPTO_ASSET_WEIGHTS,
)
from src.generators.base import get_faker_instance
try:
    from utils.evm_utils import generate_evm_wallet
except ImportError:
    from src.utils.evm_utils import generate_evm_wallet

def _random_date_in_year(year: int, n: int, fake) -> list:
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    total_days = (end_date - start_date).days

    random_days = np.random.randint(0, total_days + 1, size=n)
    dates = [start_date + timedelta(days=int(d)) for d in random_days]
    return dates

def generate_fato_transacoes() -> pd.DataFrame:
    fake = get_faker_instance()
    np.random.seed(RANDOM_SEED)

    count_2027 = int(TOTAL_TRANSACTIONS * RATIO_2027)  # 24.000
    count_2026 = int(TOTAL_TRANSACTIONS * RATIO_2026)  # 14.000
    count_2025 = TOTAL_TRANSACTIONS - count_2027 - count_2026  # 16.000

    # Geração das datas garantindo exatamente 25% em 2027, 35% em 2026 e 40% em 2025
    dates_2027 = _random_date_in_year(2027, count_2027, fake)
    dates_2026 = _random_date_in_year(2026, count_2026, fake)
    dates_2025 = _random_date_in_year(2025, count_2025, fake)
    all_dates = dates_2027 + dates_2026 + dates_2025

    # Embaralha mantendo a semente
    indices = np.random.permutation(TOTAL_TRANSACTIONS)
    shuffled_dates = [all_dates[i] for i in indices]

    # Normalização defensiva de probabilidades para evitar erros de arredondamento em float
    crypto_weights = np.array(CRYPTO_ASSET_WEIGHTS, dtype=float)
    crypto_weights = crypto_weights / crypto_weights.sum()

    transactions = []
    for idx, transfer_date in enumerate(shuffled_dates, start=1):
        # Hora no formato HH:MM:SS
        transfer_time = fake.time(pattern="%H:%M:%S")

        # Valor em dólar (com distribuição com cauda longa típica de transações financeiras)
        bracket = np.random.choice(["small", "medium", "large", "suspicious_coaf"], p=[0.60, 0.25, 0.12, 0.03])
        if bracket == "small":
            valor_dolar = round(float(np.random.uniform(10.0, 1_000.0)), 2)
        elif bracket == "medium":
            valor_dolar = round(float(np.random.uniform(1_000.0, 10_000.0)), 2)
        elif bracket == "large":
            valor_dolar = round(float(np.random.uniform(10_000.0, 50_000.0)), 2)
        else:
            # Transações de alto valor atípicas para alerta COAF
            valor_dolar = round(float(np.random.uniform(50_000.0, 1_500_000.0)), 2)

        # Ativo digital
        ativo = np.random.choice(CRYPTO_ASSETS, p=crypto_weights)

        # Tipo da transação (BOOL: True = Envio, False = Recebimento)
        tipo_transacao = bool(np.random.choice([True, False], p=[0.5, 0.5]))

        # Chave estrangeira para dim_cliente
        client_id = int(np.random.randint(1, TOTAL_CLIENTS + 1))

        # Carteira autocustódia EVM
        carteira_evm = generate_evm_wallet()

        # id_tempo para relacionamento estrela (YYYYMMDD)
        id_tempo = int(transfer_date.strftime("%Y%m%d"))

        transactions.append({
            "id_transacao": f"TRX-{idx:08d}",
            "id_cliente": client_id,
            "id_tempo": id_tempo,
            "data_transferencia": transfer_date.strftime("%Y-%m-%d"),
            "hora_transferencia": transfer_time,
            "valor_dolar": valor_dolar,
            "ativo_digital": ativo,
            "tipo_transacao": tipo_transacao,
            "carteira_autocustodia": carteira_evm
        })

    return pd.DataFrame(transactions)