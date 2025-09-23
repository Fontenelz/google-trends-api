import os

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from requests_html import AsyncHTMLSession

import asyncio
import re
import urllib.parse

app = Flask(__name__)
asession = AsyncHTMLSession()

trends_cache = []  # cache global pra evitar rodar o scraping em toda request

def formatar_dados(item: dict) -> dict:
    """
    Recebe um item no formato bruto e devolve um dicionário formatado.
    """
    # Extrai volume de buscas (ex: "50K+")
    volume_match = re.search(r"(\d+[KMB]?\+?)", item.get("data_volume", ""))
    volume = volume_match.group(1) if volume_match else None

    # Extrai porcentagem de variação (ex: "1,000%")
    perc_match = re.search(r"(\d{1,3}(?:,\d{3})*%|\d+%)", item.get("data_volume", ""))
    variation = perc_match.group(1) if perc_match else None

    # Extrai tempo (ex: "1 hour ago")
    time_match = re.search(r"(\d+\s\w+\sago)", item.get("duration", ""))
    duration = time_match.group(1) if time_match else None

    # Extrai palavras-chave (remove duplicações e "Search term", "Explore")
    keywords_raw = item.get("keywords", [])
    keywords = []
    for kw in keywords_raw:
        parts = [p.strip() for p in kw.split("\n") if p.strip()]
        for p in parts:
            if "Search term" not in p and "Explore" not in p and "query_stats" not in p:
                if p not in keywords:
                    keywords.append(p)

    # Extrai título (primeira linha antes de "·")
    title = item.get("title", "").split("\n")[0].strip()

    return {
        "title": title,
        "search_volume": volume,
        "variation": variation,
        "duration": duration,
        "keywords": keywords
    }


async def fetch_trends():
    """Scraping com renderização de JS via Pyppeteer"""
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=BR"
    r = await asession.get(url)
    await r.html.arender(timeout=20)
    # print(r.html.find("tr[data-row-id]"))
    rows = r.html.find("tr[data-row-id]")
    data = []
    for row in rows:
        cells = row.find('td')
        # print(cells.text)
        if cells:
            celulas_com_texto = [cell.text for cell in cells]
            item_data = {
                "index": celulas_com_texto[0],
                "title": celulas_com_texto[1],
                "data_volume": celulas_com_texto[2],
                "duration": celulas_com_texto[3],
                "keywords": [celulas_com_texto[4]],  # Coloca o 5º dado em uma lista para a chave 'keywords'
            }
            data.append(formatar_dados(item_data))

            # Exemplo de como usar a nova lista de textos            
            # title = cells[0].text
            # print(cell_texts)
    # print(data)
    titles = [ e.text for e in r.html.find("tr.enOdEe-wZVHld-xMbwt") ]
    return data


def update_trends():
    global trends_cache
    try:
        print("🔄 Atualizando tendências...")
        trends_cache = asession.run(fetch_trends)[0]  # <<< aqui
        # trends_cache = results[0]
        
        # print("✅ Tendências atualizadas:", trends_cache[:5])
    except Exception as e:
        print("⚠️ Erro no scraping:", e)


@app.route("/trends")
def get_trends():
    return jsonify({"trends": trends_cache})



def start_scheduler(app):
    """Inicia agendamento periódico"""
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(
        id="update_trends",
        func=update_trends,
        trigger="interval",
        minutes=10,  # roda a cada 10 min
    )
    # roda uma vez logo no início
    update_trends()


if __name__ == "__main__":
    start_scheduler(app)
    port = int(os.environ.get("PORT", 5000))   # usa PORT quando fornecido pelo ambiente
    app.run(host="0.0.0.0", port=port, debug=False)
