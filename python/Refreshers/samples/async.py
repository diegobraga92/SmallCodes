import asyncio

async def coro(n):
    await asyncio.sleep(0.1)
    return n*2

async def main():
    res = await asyncio.gather(*(coro(i) for i in range(5)))
    print(res)

asyncio.run(main())



import asyncio
import aiohttp

async def fetch_url(session, url):
    """Asynchronous URL fetching"""
    async with session.get(url) as response:
        return await response.text()


async def fetch_multiple_urls(urls):
    """Concurrent fetching"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

# Run async function
# asyncio.run(fetch_multiple_urls(['url1', 'url2']))


# simple async pattern with cancellation
import asyncio

async def waiter():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("cancelled")

async def main():
    t = asyncio.create_task(waiter())
    await asyncio.sleep(0.1)
    t.cancel()
    await asyncio.gather(t, return_exceptions=True)

asyncio.run(main())