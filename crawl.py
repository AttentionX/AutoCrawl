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

def get_reviews_prompt(inner_text):
    few_shot_example = """
    떵어리64
    리뷰 57사진 83팔로워 3
    팔로우
    방문자리뷰
    방문자리뷰
    방문자리뷰
    고기국수 국물이 굉장히 진하고 고기양도 진짜 먹어도먹어도 계속 나오는데 이게 9천원이라니!!
    내용 더보기
    음식이 맛있어요+3
    개의 리뷰가 더 있습니다
    펼쳐보기
    최근 방문일
    5.5.금
    2023년 5월 5일 금요일
    1번째 방문영수증
    맛집탐방왕
    리뷰 299사진 844팔로워 191
    팔로우
    방문자리뷰
    방문자리뷰
    다음에 또 방문하고 싶은 고기국수 집입니다 :)
    개의 리뷰가 더 있습니다
    펼쳐보기
    최근 방문일
    5.17.수
    2023년 5월 17일 수요일
    1번째 방문카드결제`
    """

    few_shot_examples_results = """
    {"author":"떵어리64", "review":"고기국수 국물이 굉장히 진하고 고기양도 진짜 먹어도먹어도 계속 나오는데 이게 9천원이라니!!", "features": ["음식이 맛있어요"], "date":"2023년 5월 5일 금요일", "index":1}
    {"author":"맛집탐방왕", "review":"다음에 또 방문하고 싶은 고기국수 집입니다 :)", "features": [], "date":"2023년 5월 17일 수요일", "index":2}
    """

    instrcution = """
    Refer to the following examples and format the input data accordingly.
    """

    prompt = f"{instrcution}\n\nExample Input Data:\n{few_shot_example}\n\nExample Results:\n{few_shot_examples_results}\n\n\nInput Data:\n{inner_text}\n\n\nResults:\n"
    return prompt