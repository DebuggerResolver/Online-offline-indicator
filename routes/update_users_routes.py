from fastapi import APIRouter,Depends,Header,Request,Response,status,Path,Query,Body
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException
import logging
from datetime import datetime,timedelta
import asyncio
import os
from utils.db_setup import Redis

SERVICE=os.getenv('SERVICE')
router=APIRouter(prefix=f"/v1/api/{SERVICE}")

@router.put("/")
async def update_users(user_id:str=Body(...)):
  conn=await Redis.connect()
  await conn.expire(user_id,timedelta(minutes=5))
  return Response(status_code=status.HTTP_200_OK)

async def main():
  await update_users("rahul")
  

if __name__=="__main__":
  asyncio.run(main())