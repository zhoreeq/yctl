# yctl
Control [Yggdrasil](https://yggdrasil-network.github.io/admin.html) node with Python.

## API
Yggdrasil's control commands translated from camelCase to pythonic snake\_case 
methods. For example, `getSelf` becomes `Control.get_self()`

Supports keepalive mode if instantiated with `keepalive=True`.

## Example
```python3
import asyncio
import yctl

async def main():
    ctl = yctl.Control(host="127.0.0.1", port=9001, keepalive=False)
    res = await ctl.get_self()

    for k, v in res["response"]["self"].items():
        res = await ctl.dht_ping(v["box_pub_key"], v["coords"])

        for k, v in res["response"]["nodes"].items():
            print(k, v)

asyncio.run(main())
```
