# async_rate_limited_client.py
import asyncio
import time
import random
from typing import Optional
import aiohttp

class TokenBucket:
    """Simple token bucket rate limiter."""
    def __init__(self, rate: float, capacity: float):
        """
        rate: tokens added per second
        capacity: max tokens in bucket
        """
        self.rate = float(rate)
        self.capacity = float(capacity)
        self._tokens = float(capacity)
        self._last = time.monotonic()
        self._lock = asyncio.Lock()

    async def consume(self, tokens: float = 1.0):
        """Wait until tokens are available, then consume them."""
        async with self._lock:
            while True:
                now = time.monotonic()
                elapsed = now - self._last
                if elapsed > 0:
                    self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
                    self._last = now
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                # compute time until next token available
                need = tokens - self._tokens
                wait = need / self.rate
                # small minimum sleep to allow other tasks to progress
                await asyncio.sleep(max(0.01, wait))

# backoff with full jitter
def backoff_sleep(attempt: int, base: float = 1.0, cap: float = 60.0):
    exp = min(cap, base * (2 ** attempt))
    sleep = random.uniform(0, exp)
    return sleep

async def fetch_with_retries(session: aiohttp.ClientSession, url: str,
                             token_bucket: TokenBucket,
                             concurrency_sem: asyncio.Semaphore,
                             max_retries: int = 6):
    attempt = 0
    while True:
        # wait for rate token and concurrency slot
        await token_bucket.consume(1.0)
        async with concurrency_sem:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    if resp.status == 429:
                        # Respect Retry-After header if present
                        ra = resp.headers.get("Retry-After")
                        if ra is not None:
                            try:
                                ra_delay = float(ra)
                            except ValueError:
                                # sometimes Retry-After is an HTTP-date; for brevity assume seconds
                                ra_delay = 5.0
                            # jitter that server told us specifically
                            await asyncio.sleep(ra_delay + random.uniform(0, 1.0))
                        else:
                            # use exponential backoff with jitter
                            if attempt >= max_retries:
                                raise aiohttp.ClientResponseError(
                                    resp.request_info, resp.history, status=resp.status,
                                    message="Too many 429s", headers=resp.headers)
                            sleep = backoff_sleep(attempt)
                            attempt += 1
                            await asyncio.sleep(sleep)
                        continue
                    # treat 5xx as retryable
                    if 500 <= resp.status < 600:
                        if attempt >= max_retries:
                            resp.raise_for_status()
                        sleep = backoff_sleep(attempt)
                        attempt += 1
                        await asyncio.sleep(sleep)
                        continue
                    # other statuses -> raise
                    resp.raise_for_status()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt >= max_retries:
                    raise
                sleep = backoff_sleep(attempt)
                attempt += 1
                await asyncio.sleep(sleep)
                continue

# usage example
async def main():
    rate_per_sec = 5.0  # allow 5 requests per second
    burst_capacity = 10.0
    token_bucket = TokenBucket(rate=rate_per_sec, capacity=burst_capacity)
    concurrency = 3  # max concurrent HTTP requests
    sem = asyncio.Semaphore(concurrency)

    urls = ["https://httpbin.org/get?i="+str(i) for i in range(50)]

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        tasks = [fetch_with_retries(session, u, token_bucket, sem) for u in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successes = [r for r in results if not isinstance(r, Exception)]
        print("successes:", len(successes))

if __name__ == "__main__":
    asyncio.run(main())
