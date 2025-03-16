from fastapi import APIRouter,Response,Request,Depends,Header,Body,Query,Path,status
import uuid
from utils.db_setup import Redis
from datetime import timedelta
from fastapi.responses import ORJSONResponse
import asyncio
import os

SERVICE=os.getenv('SERVICE')
router=APIRouter(prefix=f"/v1/api/{SERVICE}")

@router.post("/")
async def create_users(user_id:str=Query(...)):
  # user_id=uuid.uuid4()
  # key=str(user_id)
  conn=await Redis.connect()
  await conn.setex(name=user_id,time=timedelta(minutes=5),value="")
  return ORJSONResponse(content=None,status_code=status.HTTP_201_CREATED)
  
