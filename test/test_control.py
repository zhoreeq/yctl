import unittest
import asyncio

from yctl import Control

class TestControl(unittest.TestCase):

    def test_get_self(self):
        async def test():
            ctl = Control()
            res = await ctl.get_self()
            self.assertEqual(res["status"], "success")

            await ctl.disconnect()

        asyncio.run(test())
