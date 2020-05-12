import os

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

import markdown2

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))


@router.get('/')
async def ws_docs(request: Request):
    rendered_html = markdown2.markdown_path(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'websocket-docs.md'),
    )
    return templates.TemplateResponse(
        'ws-docs.html',
        {
            "request": request,
            'docs': rendered_html,
        },
    )
