import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth, customers, dashboard, inventory, orders, products
from app.core.config import get_settings
from app.middleware.rate_limit import RateLimitMiddleware

settings = get_settings()
APP_DIR = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("inventory-api")

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-ready inventory and order management API with JWT auth, stock tracking, analytics, and Docker support.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.mount("/uploads", StaticFiles(directory=APP_DIR / "uploads"), name="uploads")


@app.middleware("http")
async def request_logger(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    return await call_next(request)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(inventory.router)
app.include_router(dashboard.router)
