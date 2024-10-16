import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém os valores das variáveis de ambiente
SECRET_KEY = os.getenv("SECRET_KEY", "senha")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
