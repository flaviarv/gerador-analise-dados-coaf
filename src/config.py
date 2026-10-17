"""
Configurações centrais do pipeline de dados COAF.
"""
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Volumes de Dados
TOTAL_CLIENTS = 5_000
TOTAL_TRANSACTIONS = 40_000

# Proporção Temporal das Transações
RATIO_2027 = 0.25  # 25% (10.000 transações)
RATIO_2026 = 0.35  # 35% (14.000 transações)
RATIO_2025 = 0.40  # 40% (16.000 transações)

# Semente de reprodutibilidade
RANDOM_SEED = 42

# Ativos Digitais Comuns em Monitoramento COAF
CRYPTO_ASSETS = ["USDT", "USDC", "BTC", "ETH", "SOL", "BNB", "MONERO", "HYPER", "LINK", "ADA"]
CRYPTO_ASSET_WEIGHTS = [0.42, 0.20, 0.15, 0.10, 0.05, 0.03, 0.02, 0.01, 0.01, 0.01]


