import asyncio
import itertools
import re
import sys
import aiohttp
from bs4 import BeautifulSoup


class AsyncFetcher:
    def __init__(self, lim, urls):
        self.sem = asyncio.Semaphore(lim)
        self.urls = urls
        self.count = 0

    async def session_handler(self, session, url):
        async with session.get(url) as resp:
            assert resp.status == 200
            self.count += 1
            return await resp.text()

    async def parse_url_async(self, url, sem, n_words=7):
        async with aiohttp.ClientSession() as self.session:
            async with sem:
                page = await self.session_handler(self.session, url)
                words = re.split(r"[ ·,\n.()-/]+", BeautifulSoup(page, "html.parser").get_text())
                dct = {}
                for word in words:
                    if word.lower() not in dct:
                        dct[word.lower()] = 0
                    dct[word.lower()] += 1
                try:
                    dct.pop("")
                except Exception:
                    pass
                sorted_tuples = sorted(dct.items(), key=lambda item: item[1], reverse=True)
                dct = {k: v for k, v in sorted_tuples}
                url = url.replace('\n', '')
                if len(dct) > n_words:
                    print(f"{url}{dict(itertools.islice(dct.items(), n_words))}")
                else:
                    print(f"{url}{dct}")

    async def fetch_batch(self, urls, sem):
        tasks = [
            asyncio.create_task(self.parse_url_async(url, sem))
            for url in urls
        ]
        await asyncio.gather(*tasks)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.fetch_batch(self.urls, self.sem))


if __name__ == "__main__":
    test_fetcher = AsyncFetcher(int(sys.argv[1]), open(sys.argv[2], "r", encoding="utf8"))
    test_fetcher.start()
