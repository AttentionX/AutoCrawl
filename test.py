import natbot
import crawl
import asyncio

url = 'https://pcmap.place.naver.com/restaurant/1660727152/review/visitor?entry=pll&from=map&fromNxList=true&fromPanelNum=1&ts=1684407266873'

def natbot_crawl(url):
    print('Starting natbot crawler')
    crawler = natbot.Crawler()
    crawler.go_to_page(url)

    browser_content = "\n".join(crawler.crawl())
    print(browser_content)

async def playwright_crawl(url):
    print("Start playwright inner text extraction")
    # Use the event loop to run the coroutine and get the result
    text = await crawl.inner_text(url)
    print(text)

def main():
    print('Starting natbot crawler')
    crawler = natbot.Crawler()
    crawler.go_to_page(url)

    browser_content = "\n".join(crawler.crawl())
    print(browser_content)

    print("Start playwright inner text extraction")
    # Use the event loop to run the coroutine and get the result
    text = crawl.inner_text(url)
    print(text)

if __name__ == "__main__":
    # natbot_crawl(url)
    asyncio.run(playwright_crawl(url))