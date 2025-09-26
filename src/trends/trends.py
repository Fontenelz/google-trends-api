import re
import os

from playwright.async_api import async_playwright
from requests_html import AsyncHTMLSession

trends_cache = []  # cache global
asession = AsyncHTMLSession()

def formatar_dados(item: dict) -> dict:
    volume_match = re.search(r"(\d+[KMB]?\+?)", item.get("data_volume", ""))
    volume = volume_match.group(1) if volume_match else None

    perc_match = re.search(r"(\d{1,3}(?:,\d{3})*%|\d+%)", item.get("data_volume", ""))
    variation = perc_match.group(1) if perc_match else None

    time_match = re.search(r"(\d+\s\w+\sago)", item.get("duration", ""))
    duration = time_match.group(1) if time_match else None

    keywords_raw = item.get("keywords", [])
    keywords = []
    for kw in keywords_raw:
        parts = [p.strip() for p in kw.split("\n") if p.strip()]
        for p in parts:
            if "Search term" not in p and "Explore" not in p and "query_stats" not in p:
                if p not in keywords:
                    keywords.append(p)

    title = item.get("title", "").split("\n")[0].strip()

    return {
        "title": title,
        "search_volume": volume,
        "variation": variation,
        "duration": duration,
        "keywords": keywords,
    }


async def fetch_trends():
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=BR"
    data = []

    async with async_playwright() as p:
        try:
          # browser = await p.chromium.launch(headless=True)
          # browser = await p.chromium.connect(os.environ['BROWSER_PLAYWRIGHT_ENDPOINT'])
          browser = await p.chromium.connect("wss://browserless-production-7109.up.railway.app?token=Nlw5WXI7v1T11Gy5lbcZQ8selfiVHAa8V0Zbrl4MlZaLInA4")
          context = await browser.new_context()

          page = await context.new_page()
          await page.goto(url, timeout=30000)

          rows = await page.query_selector_all("tr[data-row-id]")
          print(rows)
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
          print("Busca finalizada")
          return data
        except Exception as e:
          # Catch any other unexpected exceptions
          print(f"An unexpected error occurred: {e}")

      
async def old_fetch_trends():
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


async def update_trends():
    global trends_cache
    try:
        print("🔄 Atualizando tendências...")
        trends_cache = await fetch_trends()
        print(f"✅ {len(trends_cache)} tendências atualizadas")
    except Exception as e:
        print("⚠️ Erro no scraping:", e)