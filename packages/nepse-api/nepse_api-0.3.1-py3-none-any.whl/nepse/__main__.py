import asyncio
from pprint import pprint

from nepse import Client


async def main():
    client = Client()
    data = await client.get_company(symbol="UPPER")
    pprint(data.security_daily_trade_dto.high_price)
    pprint(data)

    await client.close()

asyncio.run(main())