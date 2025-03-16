from fastapi import APIRouter ,Depends,Header,Request,Response,status,Query,Body,Path
from fastapi.responses import ORJSONResponse
import logging
import asyncio
from utils.db_setup import Redis
import os

SERVICE=os.getenv('SERVICE')
router=APIRouter(prefix=f"/v1/api/{SERVICE}")

@router.delete("/")
async def delete_user(user_id:str=Query(...)):
  conn=await Redis.connect()
  await conn.delete(user_id)
  logging.debug(f'User deleted successfully : {user_id}')
  return Response(status_code=status.HTTP_204_NO_CONTENT)

async def main():
  await delete_user('rahul')

if __name__=="__main__":
  logging.basicConfig(level='DEBUG')
  asyncio.run(main())