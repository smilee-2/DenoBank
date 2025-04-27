from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import users_router, auth_router, admin_router, wallet_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(wallet_router)


@app.get('/', tags=['Main'])
async def main():
    return {'msg': 'main'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='0.0.0.0')
