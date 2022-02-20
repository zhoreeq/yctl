import asyncio
import json
from typing import Dict, Optional

class Control:

    def __init__(self, host: str = "127.0.0.1", port: int = 9001,
                       keepalive: bool = False):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port)

    async def disconnect(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def _request(self, request: str, args: dict = {}) -> Dict:
        if self.keepalive:
            assert self.writer != None, "Must call connect() in keepalive mode"
            args["keepalive"] = True

        args["request"] = request
        data = json.dumps(args).encode()

        if self.keepalive and self.writer and self.reader:
            self.writer.write(data)
            resp = await self.reader.read(1024*15)

        else:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            writer.write(data)
            resp = await reader.read()
            writer.close()
            await writer.wait_closed()

        return json.loads(resp)

    async def get_DHT(self) -> Dict:
        return await self._request("getDHT")

    async def get_peers(self) -> Dict:
        return await self._request("getPeers")

    async def get_self(self) -> Dict:
        return await self._request("getSelf")

    async def get_sessions(self) -> Dict:
        return await self._request("getSessions")

    async def get_tun_tap(self) -> Dict:
        return await self._request("getTunTap")

    async def get_multicast_interfaces(self) -> Dict:
        return await self._request("getMulticastInterfaces")

    async def get_paths(self) -> Dict:
        return await self._request("getPaths")

    async def get_node_info(self, key: str) -> Dict:
        return await self._request("getNodeInfo", {"key": key})

    async def debug_remote_get_self(self, key: str) -> Dict:
        return await self._request("debug_remoteGetSelf", {"key": key})

    async def debug_remote_get_peers(self, key: str) -> Dict:
        return await self._request("debug_remoteGetPeers", {"key": key})

    async def debug_remote_get_dht(self, key: str) -> Dict:
        return await self._request("debug_remoteGetDHT", {"key": key})

