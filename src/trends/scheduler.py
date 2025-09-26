# src/trends/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .trends import update_trends

# trends_cache = []  # cache global

# async def update_trends():
#     """Função assíncrona que faz o scraping"""
#     print("🔄 Atualizando tendências...")
#     await asyncio.sleep(1)  # simula trabalho
#     return [{"title": "Exemplo", "search_volume": "50K+"}]

# def start_scheduler(app=None):
#     """Inicia o agendador"""
#     scheduler = BackgroundScheduler()

#     def job():
#         loop = asyncio.get_event_loop()
#         trends = loop.run_until_complete(update_trends())
#         global trends_cache
#         trends_cache = trends
#         print("✅ Tendências atualizadas:", trends_cache)

#     scheduler.add_job(job, IntervalTrigger(minutes=10))
#     scheduler.start()

#     # roda logo ao iniciar
#     job()

scheduler = AsyncIOScheduler()

def start_scheduler():
    # roda a cada 10 minutos
    scheduler.add_job(update_trends, "interval", minutes=10, id="update_trends")
    scheduler.start()