"""
Instância base do Faker com suporte a dados brasileiros (pt_BR).
"""
from faker import Faker
from src.config import RANDOM_SEED

def get_faker_instance() -> Faker:
    fake = Faker("pt_BR")
    Faker.seed(RANDOM_SEED)
    return fake