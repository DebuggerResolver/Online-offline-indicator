from redis import asyncio as redis
from redis.asyncio import BlockingConnectionPool
from dotenv import load_dotenv
import asyncio
import os
import logging

load_dotenv()
class Redis:
  __instance=None
  
  @staticmethod
  async def connect():
    host=os.getenv('HOST','localhost')
    port=int(os.getenv('REDIS_PORT',6379))
    username=os.getenv('username')
    password=os.getenv('password')
    async with asyncio.Lock():
      if Redis.__instance is None:
        try:
          pool = BlockingConnectionPool(host=host,port=port,username=username,password=password,db=0,max_connections=10,timeout=3 ,decode_responses=True)
          Redis.__instance=await redis.Redis(
            connection_pool=pool
            )
        except Exception as e:
          logging.error(f"An exception occured : {e}")
      return Redis.__instance
  @staticmethod
  async def close():
    async with asyncio.Lock():
      if Redis.__instance :
        await Redis.__instance.aclose()
        Redis.__instance=None
    
async def main():
  conn=await Redis.connect()
  logging.debug("Connection established")
  await conn.ping()
  await Redis.close()
  logging.debug("Connection closed")
  

if __name__=="__main__":
  logging.basicConfig(level='DEBUG')
  asyncio.run(main())

  
  