"""
Gerador da dimensão dim_cliente (5.000 clientes).
"""
import numpy as np
import pandas as pd
from src.config import TOTAL_CLIENTS, RANDOM_SEED
from src.generators.base import get_faker_instance

def generate_dim_cliente() -> pd.DataFrame:
    fake = get_faker_instance()
    np.random.seed(RANDOM_SEED)

    client_records = []
    for client_id in range(1, TOTAL_CLIENTS + 1):
        # Distribuição realista de patrimônio e renda para análise COAF
        tier = np.random.choice(["retail", "affluent", "hnw"], p=[0.70, 0.25, 0.05])
        
        if tier == "retail":
            patrimonio = round(float(np.random.uniform(5_000.0, 150_000.0)), 2)
            renda = round(float(np.random.uniform(2_000.0, 12_000.0)), 2)
        elif tier == "affluent":
            patrimonio = round(float(np.random.uniform(150_000.0, 1_500_000.0)), 2)
            renda = round(float(np.random.uniform(12_000.0, 50_000.0)), 2)
        else:  # High Net Worth
            patrimonio = round(float(np.random.uniform(1_500_000.0, 25_000_000.0)), 2)
            renda = round(float(np.random.uniform(50_000.0, 350_000.0)), 2)

        endereco = fake.address().replace("\n", ", ")

        client_records.append({
            "id_cliente": client_id,
            "nome": fake.name(),
            "CPF": fake.cpf(),
            "endereco": endereco,
            "patrimonio_declarado": patrimonio,
            "renda_mensal_declarada": renda
        })

    return pd.DataFrame(client_records)