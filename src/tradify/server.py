from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
import uvicorn
from .utils import seed_currencies
from contextlib import asynccontextmanager
from .db import engine

from tradify.transaction.routes import router as  tx_router
from tradify.user.routes import router as user_router
from tradify.wallet.routes import router as wallet_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_currencies(session)
    yield


app = FastAPI(lifespan=lifespan)



app.include_router(tx_router)
app.include_router(user_router)
app.include_router(wallet_router)



def start():
    uvicorn.run("tradify.server:app", host="127.0.0.1", port=8000, reload=True)