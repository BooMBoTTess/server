from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from server_app.src.auth.model import User
from server_app.src.utils import current_active_user, templates

from config import IP_ADDRESS
router = APIRouter(
    prefix='/dashboard',
    tags=['dashboard'],
    dependencies=[Depends(current_active_user)]
)

def get_permition(post, dep):
    """
    :param post: post_id
    :param dep: dep_id
    :return:
    permition: int: от условий дает доступы к разным дашбордам
    1 - РУК. Все дашборды.
    2.0 - замрук нулевой. (ХЗ надо придумать как это сделать)
    3.0 - начальник 0 отдела.
    -1 - остальное
    """

    permition = -1
    if post == 0:
        permition = '0'
    elif post == 1:
        permition = '1.0' # TODO: второе число отдавать по замруку доделать
    elif post == 3:
        permition = f'3.{dep}'


    return permition

@router.get('/')
async def homepage(request: Request, user: User = Depends(current_active_user)):
    """
    по permition дает определенный дашборд
    """
    post = user.fk_post_id
    dep = user.fk_department_id
    permition = get_permition(post, dep)
    if permition == -1:
        return 403
    else:
        return templates.TemplateResponse("dashboard.html", {'request': request, 'permition': permition, 'IP_ADDRESS': IP_ADDRESS})

@router.get("/{permition}")
async def direct_dashboard(request: Request, id):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})