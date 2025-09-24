from requests_html import AsyncHTMLSession
from .data_formater import formatar_dados

asession = AsyncHTMLSession()

async def fetch_trends():
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=BR"
    r = await asession.get(url)
    await r.html.arender(timeout=20)

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
