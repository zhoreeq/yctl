import unittest
import asyncio

from yctl import Control

class TestControl(unittest.TestCase):

    def test_get_self(self):
        async def test():
            ctl = Control()
            res = await ctl.get_self()
            self.assertEqual(res["status"], "success")

        asyncio.run(test())

    def test_get_self_keepalive(self):
        async def test():
            ctl = Control(keepalive=True)
            await ctl.connect()
            res = await ctl.get_self()
            await ctl.disconnect()
            self.assertEqual(res["status"], "success")

        asyncio.run(test())

    def test_get_self_keepalive_not_connected(self):
        async def test():
            ctl = Control(keepalive=True)
            with self.assertRaises(AssertionError):
                res = await ctl.get_self()

        asyncio.run(test())
