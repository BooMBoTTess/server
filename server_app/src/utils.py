from starlette.templating import Jinja2Templates

from server_app.database.user_manager import fastapi_users

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


templates = Jinja2Templates(directory="templates")