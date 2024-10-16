from datetime import datetime
import logging
import os
from fastapi import FastAPI, HTTPException, status
from src.database.db import engine
from fastapi.middleware.cors import CORSMiddleware

from src.models import models
from src.router.mala import app as mala_app
from src.router.user import app as users_app
from src.router.login import app as login_app

# Cria o banco de dados
models.Base.metadata.create_all(bind=engine)

def setup_logging():
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file = os.path.join(log_directory, f'{datetime.now().strftime("%Y-%m-%d")}.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

setup_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mala_app)
app.include_router(users_app)
app.include_router(login_app)



@app.get("/v1/status", tags=["status"])
def status():
    try:
        return {"Status": "Operational"}
    except Exception as e:
        logging.error("An error occurred during health check: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during health check")
