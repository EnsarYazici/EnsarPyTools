import asyncio
from object1 import Object1
from object2 import Object2
import Workers
# async def main():
#     obj1 = Object1()
#     obj2 = Object2()

#     await asyncio.gather(
#         obj1.start(),
#         obj2.start()
#     )
async def main():
    Workers.CreateWorker(50)

    await asyncio.gather(*(obj.start() for obj in Workers.wrks))
if __name__ == "__main__":
    try:
     asyncio.run(main())
    except KeyboardInterrupt:
        print("Program sonlandirildi...")
