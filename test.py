import asyncio
from datetime import datetime
import re

import natbot
import crawl
import openai_api

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
    # print(text)
    return text

def get_reviews_json(text):
    print("Getting reviews in json format")
    prompt = crawl.get_reviews_prompt(text)
    with open('prompts.txt', 'a') as file:
        # Write the response to the file
        file.write(f"\n\n\n{datetime.now()}\n")
        file.write(str(prompt))
    response = openai_api.chatGPT(prompt) #engine="gpt-4"
    print(response)
    with open('reviews.txt', 'a') as file:
        # Write the response to the file
        file.write(f"\n\n\n{datetime.now()}\n")
        file.write(str(response))

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
    text = asyncio.run(playwright_crawl(url))
    find_string = '정렬 안내'
    # occurrence = 3
    # inilist = [m.start() for m in re.finditer(find_string, text)]
    # cut_index = inilist[occurrence-1]
    cut_index = text.find(find_string)
    text = text[cut_index+len(find_string):]
    if len(text) > 1500:
        text = text[:1500]
    get_reviews_json(text)