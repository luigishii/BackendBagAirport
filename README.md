# BackendBagAirport


#python3 -m venv venv
#source venv/bin/activate

#alembic upgrade head

#Criar um arquivo .env: 
STAGE=DEV
DB_NAME=bagairport
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=172.17.32.1 #muda de acordo com o ip da máquina(localhost)
DB_PORT=5432

DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

