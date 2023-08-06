import asyncio
from pprint import pprint

from nepse import Client


async def main():
    client = Client()
    data = await client.get_company(symbol="UPPER")
    pprint(data.security.trading_start_date)
    # pprint(type(data.security.trading_start_date))
    pprint(data)

    await client.close()

asyncio.run(main())