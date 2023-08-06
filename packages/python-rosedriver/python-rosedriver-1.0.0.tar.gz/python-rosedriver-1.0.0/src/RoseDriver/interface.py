import asyncio
import random
import socket
import string
import json
from websockets import connect


class RoseDriverImpl:

    def __init__(self, url, port, auth):
        self.__url = f"ws://{url}:{port}"
        self.__auth = f"{auth}"
        self.ws = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.build())
        self.size = 24
        self.delay = 0.2

    async def build(self):
        try:
            print(f"Connecting to [{self.__url}]")
            self.ws = await connect(self.__url)
            print("Connected")
        except socket.gaierror:
            print("[Error]: Failed to parse the address. Perhaps there is a typo in the Websocket address?")
        except (ConnectionRefusedError, ConnectionError) as e:
            print(f"[Error]: {e} ")

    async def _get_impl(self, database, collection, identifier) -> dict:
        json_send = json.dumps({"authorization": self.__auth, "method": "get", "database": database,
                                "collection": collection, "identifier": identifier, "unique": self._id_generator()})
        await self.ws.send(json_send)
        data = await self._listener()
        return data

    async def _add_impl(self, database, collection, identifier, JSON) -> dict:
        json_send = json.dumps({"authorization": self.__auth, "method": "add", "database": database,
                                "collection": collection, "identifier": identifier, "value": JSON,
                                "unique": self._id_generator()})
        await self.ws.send(json_send)
        data = await self._listener()
        return data

    async def _remove_impl(self, database, collection, identifier, *key) -> dict:
        json_send = json.dumps({"authorization": self.__auth, "method": "delete", "database": database,
                                "collection": collection, "identifier": identifier, "key": key,
                                "unique": self._id_generator()})
        await self.ws.send(json_send)
        data = await self._listener()
        return data

    async def _remove_item_impl(self, database, collection, identifier) -> dict:
        json_send = json.dumps({"authorization": self.__auth, "method": "delete", "database": database,
                                "collection": collection, "identifier": identifier,
                                "unique": self._id_generator()})
        await self.ws.send(json_send)
        data = await self._listener()
        return data

    async def _remove_Collection_impl(self, database, collection) -> dict:
        json_send = json.dumps({"authorization": self.__auth, "method": "delete", "database": database,
                                "collection": collection,
                                "unique": self._id_generator()})
        await self.ws.send(json_send)
        data = await self._listener()
        return data

    async def _remove_Database_impl(self, database) -> dict:
        json_send = json.dumps({"authorization": self.__auth, "method": "delete", "database": database,
                                "unique": self._id_generator()})
        await self.ws.send(json_send)
        data = await self._listener()
        return data

    # simple method for closing the connection safely
    async def close(self):
        try:
            return await self.ws.close()
        except Exception as e:
            print(f"[Error]: {e}")

    # small "listener" function
    async def _listener(self) -> dict:
        while True:
            try:
                recv_data = await self.ws.recv()
                if "session" in recv_data:
                    await asyncio.sleep(self.delay)
                    continue
                else:
                    data = json.loads(recv_data)
                    return data["response"]
            except KeyError:
                print("[Error]: A delay in response caused the listener to not receive the response"
                      " before handing it over. It is advised to change the Drivers [delay] attribute higher.")
                continue

    # generates the unique string
    def _id_generator(self, chars=string.ascii_uppercase + string.digits) -> str:
        return ''.join(random.choice(chars) for _ in range(self.size))
