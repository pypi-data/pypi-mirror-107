from abc import abstractmethod
from abc import ABC
import asyncio
from bergen.wards.base import GraphQLException, MainWard, TokenExpired
import aiohttp
import requests
from bergen.console import console
from bergen.wards.base import WardException
from bergen.query import  TypedGQL
from typing import TypeVar

T = TypeVar("T")


class BareMainWard(MainWard):

    def __init__(self, client, loop=None):
        super().__init__(client, loop=loop)
        self._graphql_endpoint = f"{self.protocol}://{self.host}:{self.port}/graphql"
        

    async def connect(self):
        self.async_session = aiohttp.ClientSession(headers=self._headers)

    async def pass_async(self, the_query: TypedGQL, variables: dict = {}, **kwargs):
        query_node = the_query.query
        try:
            async with self.async_session.post(self._graphql_endpoint, json={"query": query_node, "variables": variables}) as resp:

                if resp.status == 403:
                    raise TokenExpired("Token was Expired")
            
                result = await resp.json() 

                if "errors" in result:
                    raise GraphQLException(f"Ward {self._graphql_endpoint}:" + str(result["errors"]))

                return the_query.extract(result["data"])

        except:
            console.print_exception(show_locals=True)
            raise 
            
        
    async def disconnect(self):
        await self.async_session.close()


