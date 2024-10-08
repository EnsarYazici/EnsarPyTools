from Object import ObjectBase
import asyncio

class Object1(ObjectBase):
    def __init__(self,id = -1,update_inerval = 1):
        super().__init__(update_inerval)
        self.id = id
        self.a = 0
    async def start(self):
        print(f"Object{self.id} start")

    async def update(self):
        print(f"Object{self.id} update")
        for i in range(5):
            print(f"Object{self.id} processing {i}")
            await asyncio.sleep(1)  # Simulate a long-running task
            self.a += 1
        if self.a >= 10:
          self.stop()
