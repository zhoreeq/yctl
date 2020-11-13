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

    async def add_peer(self, uri: str) -> Dict:
        return await self._request("addPeer", {"uri": uri})

    async def remove_peer(self, port: int) -> Dict:
        return await self._request("removePeer", {"port": port})

    async def disconnect_peer(self, port: int) -> Dict:
        return await self._request("disconnectPeer", {"port": port})

    async def get_switch_peers(self) -> Dict:
        return await self._request("getSwitchPeers")

    async def get_self(self) -> Dict:
        return await self._request("getSelf")

    async def get_sessions(self) -> Dict:
        return await self._request("getSessions")

    async def get_tun_tap(self) -> Dict:
        return await self._request("getTunTap")

    async def get_allowed_encryption_public_keys(self) -> Dict:
        return await self._request("getAllowedEncryptionPublicKeys")

    async def add_allowed_encryption_public_key(self, box_pub_key: str) -> Dict:
        return await self._request("addAllowedEncryptionPublicKey", {
            "box_pub_key": box_pub_key})

    async def remove_allowed_encryption_public_key(self, box_pub_key: str) -> Dict:
        return await self._request("removeAllowedEncryptionPublicKey", {
            "box_pub_key": box_pub_key})

    async def get_multicast_interfaces(self) -> Dict:
        return await self._request("getMulticastInterfaces")

    async def get_routes(self) -> Dict:
        return await self._request("getRoutes")

    async def add_route(self, subnet: str, box_pub_key: str) -> Dict:
        return await self._request("addRoute", 
                {"subnet": subnet, "box_pub_key": box_pub_key})

    async def remove_route(self, subnet: str, box_pub_key: str) -> Dict:
        return await self._request("removeRoute", 
                {"subnet": subnet, "box_pub_key": box_pub_key})

    async def get_source_subnets(self) -> Dict:
        return await self._request("getSourceSubnets")

    async def add_source_subnet(self, subnet: str) -> Dict:
        return await self._request("addSourceSubnet", {"subnet": subnet})

    async def remove_source_subnet(self, subnet: str) -> Dict:
        return await self._request("removeSourceSubnet", {"subnet": subnet})

    async def dht_ping(self, box_pub_key: str, coords: str, target: str = "") -> Dict:
        args = {"box_pub_key": box_pub_key, "coords": coords}
        if target: args["target"] = target
        return await self._request("dhtPing", args)

    async def get_node_info(self, box_pub_key: str, coords: str) -> Dict:
        return await self._request("getNodeInfo", 
                {"box_pub_key": box_pub_key, "coords": coords})

