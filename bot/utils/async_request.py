from enum import Enum
from aiohttp import ClientSession
from loguru import logger


class Method(Enum):
      POST = "post"
      GET = "get"
      PUT = "put"
      DELETE = "delete"


async def request_provider(url, method: Method, headers: dict|None=None, body_or_params: dict|None=None, ):
    async with ClientSession() as session:
        query = None
        match method:
            case Method.POST:
                  query =  session.post(url, json=body_or_params)
            case Method.GET:
                  query =  session.get(url, params=body_or_params)
            case Method.PUT:
                  query =  session.put(url, json=body_or_params)
            case Method.DELETE:
                  query =  session.delete(url, params=body_or_params)
                
        async with query as resp:
            logger.info(f"{resp.status=}")
            logger.info(f"{await resp.text()=}")

            data = await resp.json()
            logger.info(f"{data=}")
            return data