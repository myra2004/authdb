from fastapi import FastAPI, Request
import datetime
from app.router.auth_router import router as auth_router
from app.router.book import router as book_router

app = FastAPI()


requests_in_this_minute= 0


@app.middleware("http")
async def simple_rate_limiter(request: Request,
                              call_next):
    global requests_dict
    request_time = time.time()
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)
app.include_router(book_router)

"""
from typing import Union
import time
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.router.auth import router as auth_router
from app.router.book import router as book_router

app = FastAPI()


requests_in_this_minute = 0

requests_dict = {}
# requests_dict = {"23-03-2023 12:00": 1, "23-03-2023 12:01": 2, "23-03-2023 12:02": 3}


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

@app.middleware("http")
async def simple_rate_limiter(request: Request, call_next):
    # global requests_in_this_minute
    # requests_in_this_minute += 1
    # if requests_in_this_minute > 10:
    #     return {"error": "Too many requests"}

    global requests_dict
    request_time = datetime.now()
    request_time = request_time.strftime("%d-%m-%Y %H:%M")
    if request_time not in requests_dict:
        requests_dict[request_time] = 1
    else:
        requests_dict[request_time] += 1

    print(">>>", requests_dict)

    if requests_dict[request_time] > 10:
        return JSONResponse(
            content={"error": "Rate limit exceeded. Please try again later."},
            status_code=429,
            media_type="application/json"
        )

    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth_router)
app.include_router(book_router)


"""