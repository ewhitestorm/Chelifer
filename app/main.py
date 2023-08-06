from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Union
from translation import City
from constructor import Constructor



class ItemIn(BaseModel):
    city: Union[str,None] = None
    global_city_id: Union[str,None] = Field(None, min_length=3)


app = FastAPI()


@app.get("/")
def root():
    return FileResponse("templates/index.html")


@app.get("/swagger")
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.post("/city")
async def form_city(request: Request):
    formdata = await request.form()
    data = ItemIn.model_validate(dict(formdata))
    city_name = City.translate_city(data.city)
    return RedirectResponse(url=f"city/{city_name}")


@app.post("/city/{city_id}")
async def post_form(city_id: str, request: Request):
    formdata = await request.form()
    data = ItemIn.model_validate(dict(formdata))
    item = ItemIn(city=data.city, global_city_id=city_id)
    item_dict = item.model_dump()
    return Constructor.info_about_city(item_dict['global_city_id'], item_dict['city'])


@app.get("/city/{city_id}")
async def get_link(city_id: str, city: str=None):
    item = ItemIn(global_city_id=city_id)
    item_dict = item.model_dump()
    return Constructor.info_about_city(item_dict['global_city_id'], city)