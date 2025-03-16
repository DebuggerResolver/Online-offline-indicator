from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import logging
import os
import dotenv
from utils.db_setup import Redis
from routes.create_users_routes import router as user_router
from routes.get_users_routes import router as get_users
from routes.update_users_routes import router as update_users
from routes.delete_user_routes import router as delete_users
dotenv.load_dotenv()

SERVICE=os.getenv('SERVICE')
PORT=os.getenv('PORT')
@asynccontextmanager
async def lifespan(app:FastAPI):
  conn=await Redis.connect()
  await conn.ping()
  yield
  await Redis.close()
  
app=FastAPI(
  title='Simple online/offline indicator',
  summary='Online offline indicator that can alos be used to detect failures in distributed systems',
  description='Project 1: Online offline indicator without using websockets',
  version='1.0.0',
  docs_url=f"/v1/api/{SERVICE}/docs",
  openapi_url=f"/v1/api/{SERVICE}/openapi.json",
  lifespan=lifespan
)

# Add middlewares

# Add routes
app.include_router(user_router)
app.include_router(get_users)
app.include_router(update_users)
app.include_router(delete_users)

# Handle global Exceptions


if __name__=="__main__":
  logging.basicConfig(level='DEBUG')
  uvicorn.run("main:app",host='0.0.0.0',port=int(PORT),reload=True)

# When a server or application binds to 0.0.0.0, it means "listen on all available network interfaces" on the machine.

# For example, a web server listening on 0.0.0.0:8000 will accept requests from any network interface, including:
# localhost (127.0.0.1)
# Local area network (LAN) IP (e.g., 192.168.x.x)
# Public IP address (if accessible from the internet)
