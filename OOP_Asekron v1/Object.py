import asyncio

class ObjectBase:
    def __init__(self,id = -1, update_interval=1.0):
        self.update_interval = update_interval
        self.running = True
        self.id = id

    async def run(self):
        await self.start()
        if hasattr(self, 'update'):
            while self.running:
                await self.update()
                await asyncio.sleep(self.update_interval)

    async def start(self):
        pass  # Subclasses can override this method

    async def stop(self):
        self.running = False
        print(f"Object stopped: {self.id}")
