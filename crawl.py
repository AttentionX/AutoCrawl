from playwright.async_api import async_playwright

async def inner_text(url):
    text = ''
    async def extract_text(url):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            try:
                await page.goto(url)
            except Exception as e:
                print(e)
                await browser.close()
                return ''
            
            # Wait for the page to finish loading
            await page.wait_for_selector('body')
            # Extract the visible text on the page
            text = await page.evaluate("() => document.querySelector('body').innerText")
            await browser.close()
            return text

    return await extract_text(url)