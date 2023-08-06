import asyncio


class DoWork:
    def __init__(self, a: str) -> None:
        self.a = a

        print('First run!')
        self.khana_khane()


    def khana_khane(self) -> None:
        print(f"khana khane {self.a}")

    def mukh_dhune(self) -> None:
        print("mukh dhune")

    def uthne(self) -> None:
        print("avi gu uthyos")

    async def longggggggggg_method(self):
        print('LOLOOLOLOLOLOLOLOLOLOL')
        await asyncio.sleep(1)
        return "something"

    @classmethod
    def gu_khane(cls) -> None:
        print("gu khane")