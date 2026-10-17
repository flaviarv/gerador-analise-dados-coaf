"""
Geração de endereços de carteiras autocustódia no padrão EVM (Ethereum Virtual Machine).
Formato: 0x seguido de 40 caracteres hexadecimais.
"""
import secrets

def generate_evm_wallet(seed: int = None) -> str:
    """Gera um endereço de carteira EVM válido (0x + 40 hex chars)."""
    random_bytes = secrets.token_bytes(20)
    return "0x" + random_bytes.hex()