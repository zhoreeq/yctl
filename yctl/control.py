import asyncio
import json

class Control:

    def __init__(self, host="127.0.0.1", port=9001, keepalive=False):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port)

    async def disconnect(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def _request(self, request, args={}):
        if self.keepalive:
            assert self.writer != None, "Must call connect() in keepalive mode"
            args["keepalive"] = True

        args["request"] = request
        data = json.dumps(args).encode()

        if self.keepalive:
            self.writer.write(data)
            resp = await self.reader.read(1024*15)

        else:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            writer.write(data)
            resp = await reader.read()
            writer.close()
            await writer.wait_closed()

        return json.loads(resp)

    async def get_DHT(self):
        return await self._request("getDHT")

    async def get_peers(self):
        return await self._request("getPeers")

    async def add_peer(self, uri):
        return await self._request("addPeer", {"uri": uri})

    async def remove_peer(self, port):
        return await self._request("removePeer", {"port": port})

    async def get_switch_peers(self):
        return await self._request("getSwitchPeers")

    async def get_self(self):
        return await self._request("getSelf")

    async def get_sessions(self):
        return await self._request("getSessions")

    async def get_tun_tap(self):
        return await self._request("getTunTap")

    async def get_allowed_encryption_public_keys(self):
        return await self._request("getAllowedEncryptionPublicKeys")

    async def add_allowed_encryption_public_key(self, box_pub_key):
        return await self._request("addAllowedEncryptionPublicKey", {
            "box_pub_key": box_pub_key})

    async def remove_allowed_encryption_public_key(self, box_pub_key):
        return await self._request("removeAllowedEncryptionPublicKey", {
            "box_pub_key": box_pub_key})

    async def get_multicast_interfaces(self):
        return await self._request("getMulticastInterfaces")

    async def get_routes(self):
        return await self._request("getRoutes")

    async def add_route(self, subnet, box_pub_key):
        return await self._request("addRoute", 
                {"subnet": subnet, "box_pub_key": box_pub_key})

    async def remove_route(self, subnet, box_pub_key):
        return await self._request("removeRoute", 
                {"subnet": subnet, "box_pub_key": box_pub_key})

    async def get_source_subnets(self):
        return await self._request("getSourceSubnets")

    async def add_source_subnet(self, subnet):
        return await self._request("addSourceSubnet", {"subnet": subnet})

    async def remove_source_subnet(self, subnet):
        return await self._request("removeSourceSubnet", {"subnet": subnet})

    async def dht_ping(self, box_pub_key, coords, target=None):
        args = {"box_pub_key": box_pub_key, "coords": coords}
        if target: args["target"] = target
        return await self._request("dhtPing", args)

    async def get_node_info(self, box_pub_key, coords):
        return await self._request("getNodeInfo", 
                {"box_pub_key": box_pub_key, "coords": coords})

