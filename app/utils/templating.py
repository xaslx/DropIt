from fastapi.templating import Jinja2Templates
from functools import lru_cache


@lru_cache()
def get_template() -> Jinja2Templates:
    templates: Jinja2Templates = Jinja2Templates(directory="app/static/templates")
    return templates