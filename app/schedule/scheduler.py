from flask_apscheduler import APScheduler
from app.utils.scraper import asession, fetch_trends
from app.utils.data_formater import formatar_dados

trends_cache = []

def update_trends():
    global trends_cache
    try:
        print("🔄 Atualizando tendências...")
        trends_cache = asession.run(fetch_trends)[0]
    except Exception as e:
        print("⚠️ Erro no scraping:", e)

def start_scheduler(app):
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(
        id="update_trends",
        func=update_trends,
        trigger="interval",
        minutes=10,
    )
    update_trends()

def get_cache():
    return trends_cache
