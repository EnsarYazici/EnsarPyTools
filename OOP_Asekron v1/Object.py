import asyncio

class ObjectBase:
    def __init__(self, update_interval=1.0):
        self.update_interval = update_interval
        self.running = True

    async def start(self):
        await self.on_start()
        if hasattr(self, 'update'):
            while self.running:
                await self.update()
                await asyncio.sleep(self.update_interval)

    async def on_start(self):
        pass  # Subclasses can override this method

    def stop(self)
        self.running = False
