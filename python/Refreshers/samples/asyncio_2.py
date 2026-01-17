import asyncio

counter = 0

async def inc_counter(name):
    global counter
    while counter < 10000:
        counter += 1
        print(f"Thread {name}: {counter}")
        sleep_time = 0.0001 + (counter % 5) * 0.0001
        await asyncio.sleep(sleep_time)

async def main():
    tasks = [asyncio.create_task(inc_counter(f"Thread-{i}")) for i in range(5)]

    await asyncio.gather(*tasks)

asyncio.run(main())