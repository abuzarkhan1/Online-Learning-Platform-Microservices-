from fastapi import FastAPI, Request
from .config.logger import logger
from .config.database import Base, engine
from .routes import course_route, lesson_route
import time
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course_route.router)
app.include_router(lesson_route.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"{request.method} {request.url} completed_in={process_time:.2f}ms status={response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Unhandled error for {request.method} {request.url}: {str(e)}")
        raise
