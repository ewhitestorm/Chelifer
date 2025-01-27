import os
import asyncio
import secrets
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Union
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer
from logic.translation import City
from logic.constructor import Constructor
from logic.positioning import Data



class ItemIn(BaseModel):
    city: Union[str, None] = Field(None, min_length=1)
    location: Union[str, None] = None
    global_city_id: Union[str,None] = None

class ItemOut(BaseModel):
    location: str
    city: str
    rubric: str
    num: int


load_dotenv()
secret_key = os.environ.get("SECRET_KEY")

app = FastAPI()

app.session_cookie_name = "session"
app.add_middleware(SessionMiddleware, secret_key=secret_key)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

post_form_result = {}
counter = int()
error_displayed = bool() 


def generate_csrf_token(secret_key):
    serializer = URLSafeTimedSerializer(secret_key)
    token = secrets.token_urlsafe(32)
    main_csrf_token = serializer.dumps(token)
    return main_csrf_token


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    if "csrf_token":
        request.session["csrf_token"] = generate_csrf_token(secret_key)
        csrf_token = request.session["csrf_token"]
    return templates.TemplateResponse("index.html", {"request": request, "csrf_token": csrf_token})


@app.get("/swagger")
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.post("/realestate")
async def form_options(data: ItemIn, request: Request):
    csrf_token = request.headers.get("X-CSRFToken")
    
    if not csrf_token or csrf_token != request.session.get("csrf_token"):
        return RedirectResponse(url="/error_csrf", status_code=403)
    
    city_name = City.translate_city(data.city)
    return RedirectResponse(url=f"realestate/{city_name}")


@app.post("/realestate/{city_id}")
async def post_form(city_id: str, data: ItemIn, request: Request):
    global counter
    post_form_result = {}

    csrf_token = request.headers.get("X-CSRFToken")
    
    if not csrf_token or csrf_token != request.session.get("csrf_token"):
        return RedirectResponse(url="/error_csrf", status_code=403)
    
    item = ItemIn(city=data.city, global_city_id=city_id)
    item_dict = item.model_dump()
    post_form_result = Constructor.info_about_city(item_dict['global_city_id'], item_dict['city'])
    
    counter_res = await Data.func_counter()
    asyncio.create_task(Data.log_data(counter_res, post_form_result))
    
    request.session.clear()
    return post_form_result
    

@app.get("/error_page")
async def exem_error_page(request: Request):
    global error_displayed
    
    if error_displayed == True:
        error_displayed = False
        return templates.TemplateResponse("error_page.html", {"request": request})
    
    else:
        return templates.TemplateResponse("error_404.html", {"request": request})


@app.get("/errorCSRF")
async def exem_error_csrf(request: Request):
    global error_displayed

    if error_displayed == True:
        error_displayed = False
        return templates.TemplateResponse("error_csrf.html", {"request": request})
    
    else:
        return templates.TemplateResponse("error_404.html", {"request": request})


@app.get("/{error_type}")
async def error_handler(error_type: str, request: Request):
    global error_displayed

    if error_type == "error":
        if request.query_params.get("from_js") == "true":
            error_displayed = True
        return RedirectResponse(url="/error_page", status_code=302)
    
    elif error_type == "error_csrf":
        if request.query_params.get("from_js") == "true":
            error_displayed = True
        return RedirectResponse(url="/errorCSRF", status_code=302)
        
    else:
        return templates.TemplateResponse("error_404.html", {"request": request})
        

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def allowed_paths(request: Request):
    get_paths = ["/", "/docs", "/openapi.json", "/swagger"]
    post_paths = ["/realestate", "/realestate/{city_id}"]
    
    if request.method == "GET" and request.url.path not in get_paths:
        return templates.TemplateResponse("error_404.html", {"request": request})

    elif request.method == "POST" and request.url.path not in post_paths:
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
        