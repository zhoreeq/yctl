# yctl
Control [Yggdrasil](https://yggdrasil-network.github.io/) node with Python.

```
pip install yctl
```

## API
[Yggdrasil's control commands](https://yggdrasil-network.github.io/admin.html) 
translated from camelCase to pythonic snake\_case methods. For example, 
`getSelf` becomes `Control.get_self()`

Supports keepalive mode if instantiated with `keepalive=True`.

## Example
```python3
import asyncio
import yctl

async def main():
    ctl = yctl.Control(host="127.0.0.1", port=9001, keepalive=False)
    res = await ctl.get_peers()

    for k, v in res['response']['peers'].items():
        res = await ctl.debug_remote_get_self(v['key'])
        print(res)

asyncio.run(main())
```
