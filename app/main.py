from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Union
from logic.translation import City
from logic.constructor import Constructor
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates


class ItemIn(BaseModel):
    city: Union[str,None] = Field(None, min_length=1)
    location: Union[str, None] = None
    global_city_id: Union[str,None] = None

class ItemOut(BaseModel):
    location: str
    city: str
    rubric: str
    num: int


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

post_form_result = {}


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/swagger")
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.get("/error")
async def error_page(request: Request):
    if request.headers.get("Referer", "").startswith(str(request.base_url)):
        return templates.TemplateResponse("error_page.html", {"request": request})
    else:
        return templates.TemplateResponse("error_404.html", {"request": request})


@app.post("/realestate")
async def form_options(data: ItemIn, request: Request):
    city_name = City.translate_city(data.city)
    return RedirectResponse(url=f"realestate/{city_name}")


@app.post("/realestate/{city_id}")
async def post_form(city_id: str, data: ItemIn):
    post_form_result = {}
    item = ItemIn(city=data.city, global_city_id=city_id)
    item_dict = item.model_dump()
    post_form_result = Constructor.info_about_city(item_dict['global_city_id'], item_dict['city'])
    return post_form_result


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def allowed_paths(request: Request, path: str):
    get_paths = ['/', '/docs', '/openapi.json', '/swagger']
    post_paths = ["/realestate", "/realestate/{city_id}"]
    
    if request.method == 'GET' and request.url.path not in get_paths:
        return templates.TemplateResponse("error_404.html", {"request": request})

    elif request.method == 'POST' and request.url.path not in post_paths:
        return templates.TemplateResponse("error_404.html", {"request": request})

    else:
        pass  


@app.get("/check_result")
async def check_result():
    try:
        data = jsonable_encoder(post_form_result)
        item = ItemOut(**data)
        return JSONResponse(content=item.model_dump())

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
        