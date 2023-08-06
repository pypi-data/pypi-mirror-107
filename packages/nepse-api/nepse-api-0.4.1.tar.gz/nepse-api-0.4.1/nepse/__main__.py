import asyncio

import httpx

from nepse import Client
from nepse.utils import ClientWrapperHTTPX


async def main():
    nepse_client = Client()

    data = await nepse_client.get_company(symbol="LOL")
    print(data.issued_capital)
    
    await nepse_client.close()

asyncio.run(main())