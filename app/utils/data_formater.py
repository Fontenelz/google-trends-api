import re

def formatar_dados(item: dict) -> dict:
    """
    Recebe um item no formato bruto e devolve um dicionário formatado.
    """
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
        "keywords": keywords
    }
