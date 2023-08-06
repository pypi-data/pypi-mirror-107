from pprint import pprint
import trio

from rmcl import api

async def list_items():
    client = await api.get_client()
    await client.update_items()
    pprint(client.by_id)

trio.run(list_items)
