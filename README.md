BackendBagAirport 

Este é um projeto para o sistema de gerenciamento de aeroportos utilizando FastAPI e PostgreSQL.

Configuração do Ambiente

Usaremos o wsl linux dentro do vscode

Criar e Ativar o Ambiente Virtual

Copiar código:

python3 -m venv venv 
source venv/bin/activate

pip install -r requirements.txt

Criar um Arquivo .env 
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

STAGE=DEV 
DB_NAME=bagairport 
DB_USER=postgres 
DB_PASSWORD=postgres 
DB_HOST=172.17.32.1 # Mude de acordo com o IP da máquina (localhost) (comando ipconfig no cmd, aí veja o Ipv4 da máquina)
DB_PORT=5432

DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}


Atualizar o Banco de Dados 
Aplique as migrações para criar ou atualizar o esquema do banco de dados:
Copiar código:

alembic upgrade head

Executar o Servidor Inicie o servidor de desenvolvimento:
Copiar código:

uvicorn src.main:app --reload --port 5000

Acessar a Documentação da API Abra o navegador e acesse o link:
http://localhost:8000/docs

