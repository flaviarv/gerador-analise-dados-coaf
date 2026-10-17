# Gerador de Análise de Dados COAF

Aplicação em Python projetada para processamento e análise de dados relacionados a relatórios de conformidade e operações financeiras (COAF). O projeto é totalmente conteinerizado com Docker para garantir reprodução idêntica do ambiente de execução e facilitar a execução de rotinas de teste.

---

## 🚀 Quick Start

### Pré-requisitos

Para rodar esta aplicação, você precisa apenas de:
* [Docker](https://docs.docker.com/get-docker/) instalado na máquina (Windows, macOS ou Linux).

---

### 1. Clonar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/SEU_USUARIO/gerador-analise-dados-coaf-docker.git
cd gerador-analise-dados-coaf-docker
```

---

### 2. Configurar variáveis de ambiente

Copie o arquivo de exemplo para criar a sua configuração local:

```bash
cp .env.example .env
```

Abra o arquivo `.env` e preencha as variáveis de banco de dados e credenciais conforme o seu ambiente de teste:

```ini
MYSQL_HOST=host.docker.internal
MYSQL_PORT=3306 #Porta padrão mySQL
MYSQL_USER=root #Login padrão mySQL
MYSQL_PASSWORD=root #Senha padrão mySQL
MYSQL_DATABASE=nome-seu-banco-de-dados # Escolha um nome para o seu banco de dados
MYSQL_CHARSET=utf8mb4 
```

---

### 3. Executar com Docker (Recomendado)

Construa a imagem Docker e inicie a aplicação apontando para o seu `.env`:

```bash
# 1. Construir a imagem da aplicação
docker build -t gerador-dados-pld-ft .

# 2. Executar o container em modo interativo
docker run --rm -it --env-file .env gerador-coaf # ótimo execução em termos de cibersegurança 
```

---

## 🛠️ Execução local (Sem Docker - Opcional)

Caso prefira rodar diretamente no seu ambiente Python local ou via WSL:

1. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   
   # No Linux/WSL/macOS:
   source .venv/bin/activate
   
   # No Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   ```

2. **Instale as dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Inicie o script principal:**
   ```bash
   python main.py
   ```

---

## 📁 Estrutura do Projeto

```text
├── data/              # #########
├── database/          # Módulos de conexão e operações com banco de dados
├── src/               # Gerador de dados sintéticos e pipeline de ETL
├── docs/              # Diagramas de arquitetura 
├── utils/             # Funções utilitárias e helpers
├── Dockerfile         # Definição do container de execução
├── requirements.txt   # Dependências do ecossistema Python
├── .dockerignore      # Exclusões para otimização de build da imagem
├── .gitignore         # Exclusões de arquivos de tracking do Git
├── main.py            # Ponto de entrada da aplicação
└── README.md          # Guia de documentação e início rápido
```

---

## 🔒 Segurança e Boas Práticas

* **Credenciais:** O arquivo `.env` nunca deve ser versionado no Git. Utilize sempre `.env.example` para documentar novas variáveis necessárias.
* **Dados Sensíveis:** Pastas contendo arquivos reais de dados ou logs (`data/`, `docs/`, `queries/`, `*.log`) DEVEM SER IGNORADAS pelo `.gitignore` e `.dockerignore` para proteger os dados e mantê-los em conformidade regulatória (LGPD, COAF)