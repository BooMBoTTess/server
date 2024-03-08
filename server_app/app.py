import sys
sys.path.append(r'C:\pycharm\Async_dash_test')

import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from src.home.routes import router as home_router
from src.dashboard.routes import router as dashboard_router
from src.auth.routes import router as user_router
from src.staff.routes import router as staff_router
from src.get_kvk.routes import router as kvk_router

from config import IP_ADDRESS
"""Я РАндомная строка АРтёмап"""
app = FastAPI(
    title='Training application'

)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router)
app.include_router(home_router)
app.include_router(dashboard_router)
app.include_router(staff_router)
app.include_router(kvk_router)

@app.get('/')
def redirect_to_login(request: Request):
    if 'auth' in request.cookies:
        return RedirectResponse('/home')
    else:
        return RedirectResponse("/auth/login")


def run_fastapi_app():


    uvicorn.run('app:app', host=IP_ADDRESS, port=8000, log_level="info", reload=True)
    print(f'SERVER STARTED ON IP: {IP_ADDRESS}')

if __name__ == '__main__':
    run_fastapi_app()
