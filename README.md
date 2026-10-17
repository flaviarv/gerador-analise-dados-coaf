# 📊 Ativar programa com Docker
docker run --rm -v "${PWD}:/app" gerador-analise-dados-coaf


# A opção 1 é mais segura do que a 2 em termos de cibersegurança
1. docker run --env-file .env coaf 
2. docker build -t coaf .

################################################################

## Como executar os testes com Docker

1. Clone o repositório:
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Crie o arquivo de ambiente:
   cp .env.example .env

3. Construa e execute a imagem:
   docker build -t meu-app .
   docker run --rm -it --env-file .env meu-app