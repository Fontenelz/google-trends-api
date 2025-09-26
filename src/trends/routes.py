from fastapi import APIRouter
from .trends import trends_cache, fetch_trends

router = APIRouter()

@router.get("/")
async def main():
  return { "message": "hello world" }

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/trends")
async def get_trends():
    # TODO: lógica de scraping Google Trends
    if len(trends_cache) == 0:
      await fetch_trends();
    return {"trends": trends_cache}
