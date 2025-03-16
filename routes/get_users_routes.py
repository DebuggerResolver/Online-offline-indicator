from fastapi import FastAPI,Response,Request,Depends,Header,status,Body,Path,Query,APIRouter
from utils.db_setup import Redis
from fastapi.responses import ORJSONResponse
import asyncio
import logging
import os

SERVICE=os.getenv('SERVICE')
router=APIRouter(prefix=f"/v1/api/{SERVICE}")
logging.basicConfig(level='DEBUG')
@router.get("/")
async def get_all_users():
    conn = await Redis.connect()
    cursor = b'0'
    keys = []
    batch_size = 100  # Control batch size for better performance
    while cursor != 0:
        cursor, partial_keys = await conn.scan(cursor=cursor, match="*", count=batch_size)
        keys.extend(partial_keys)

    logging.debug(f"Keys fetched: {len(keys)}")
    return ORJSONResponse(content=keys, status_code=status.HTTP_200_OK)


async def main():
  await get_all_users()

if __name__=="__main__":
  asyncio.run(main())