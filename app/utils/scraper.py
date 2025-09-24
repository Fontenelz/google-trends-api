from requests_html import AsyncHTMLSession
from .data_formater import formatar_dados
from playwright.async_api import async_playwright

asession = AsyncHTMLSession()

async def fetch_trends():
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=BR"
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=30000)

        rows = await page.query_selector_all("tr[data-row-id]")
        for row in rows:
            cells = await row.query_selector_all("td")
            if cells:
                celulas_com_texto = [await cell.inner_text() for cell in cells]
                item_data = {
                    "index": celulas_com_texto[0],
                    "title": celulas_com_texto[1],
                    "data_volume": celulas_com_texto[2],
                    "duration": celulas_com_texto[3],
                    "keywords": [celulas_com_texto[4]],
                }
                data.append(formatar_dados(item_data))

        await browser.close()
    return data
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=BR"
    r = await asession.get(url)
    await r.html.arender(
        timeout=20,
        keep_page=True,
        scrolldown=0,
    )

    rows = r.html.find("tr[data-row-id]")
    data = []
    for row in rows:
        cells = row.find('td')
        if cells:
            celulas_com_texto = [cell.text for cell in cells]
            item_data = {
                "index": celulas_com_texto[0],
                "title": celulas_com_texto[1],
                "data_volume": celulas_com_texto[2],
                "duration": celulas_com_texto[3],
                "keywords": [celulas_com_texto[4]],
            }
            data.append(formatar_dados(item_data))
    return data
