"""
MASTER ORCHESTRATOR - Pipeline Completo COAF
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Registra a raiz e o gerador no sys.path para os imports internos de 'src' funcionarem
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "gerador_dados_coaf"))

from src.pipelines.runner import CoafPipeline

def main():
    print("=" * 60)
    print("INICIANDO GERAÇÃO DE DADOS COAF")
    print("=" * 60)

    pipeline = CoafPipeline()
    metricas = pipeline.run()

    print("\n" + "=" * 60)
    print("CONCLUÍDO COM SUCESSO:")
    print(metricas)
    print("=" * 60)


if __name__ == "__main__":
    main()