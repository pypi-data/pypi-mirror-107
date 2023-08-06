import asyncio

from test2 import DoWork


async def main() -> None:
    a = DoWork('avi gu')
    # print('Second Run!')
    # a.khana_khane
    b = list()
    for _ in range(10):
        b.append(a.longggggggggg_method())
    
    await asyncio.gather(*b)
    
    print('gaegaegaegaeg')
    print('gaegaegaegaeg')
    # await asyncio.gather(*b)

    a 

if __name__ == "__main__":
    asyncio.run(main())