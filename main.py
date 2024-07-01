from fastapi import FastAPI, Request, Form
from fastapi.middleware.wsgi import WSGIMiddleware
from dashboards.manual import dash_app
from dashboards.j import dash_app as j_app
from dashboards.v import dash_app as v_app
import uvicorn
import os
from fastapi import File, UploadFile, Body
from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from fastapi.staticfiles import StaticFiles
from deleter import deleter
from handler import Handler

handler = Handler()
app = FastAPI()
app.mount("/dashboard/manual", WSGIMiddleware(dash_app.server))
app.mount("/dashboard/j", WSGIMiddleware(j_app.server))
app.mount("/dashboard/v", WSGIMiddleware(v_app.server))
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="./static"), name='static')

base_dir = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=base_dir + '/templates')


# @app.get('/')
# def index():
#     return "Hello"


@app.get("/manual")
async def get_manual(request: Request):
    return templates.TemplateResponse("manual.html", {"request": request})


@app.get("/j")
async def get_j(request: Request):
    return templates.TemplateResponse("j.html", {"request": request})

@app.get("/g")
async def get_g(request: Request):
    return templates.TemplateResponse("g.html", {"request": request})
@app.get("/v")
async def get_v(request: Request):
    return templates.TemplateResponse("v.html", {"request": request})


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("src.html", {"request": request})


@app.post("/manual", status_code=200)
def get_trajectory(file: List[UploadFile] = File(...)):
    deleter.delete_excel_data_files()
    files = file
    for file in files:
        with open(f'data/{file.filename}', 'wb') as f:
            content = file.file.read()
            f.write(content)
            f.close()
    return RedirectResponse(url="/dashboard/manual", status_code=302)


@app.post("/j", status_code=200)
def get_trajectory_j(md_vertical: float = Form(...), md_inclined: float = Form(...), x: float = Form(...),
                     y: float = Form(...), inclination: float = Form(...), azimuth: float = Form(...),
                     z: float = Form(...), md_angle: float = Form(...)):
    deleter.delete_excel_type_file(type='j')
    handler.dater.create_data_for_j(md_inclined=md_inclined, md_vertical=md_vertical, x=x, y=y, z=z, inclination=inclination, azimuth=azimuth, md_angle=md_angle)
    return RedirectResponse(url="/dashboard/j", status_code=302)


@app.post("/v", status_code=200)
def get_trajectory_v(md: float = Form(...), x: float = Form(...), y: float = Form(...), z: float = Form(...)):
    deleter.delete_excel_type_file(type='v')
    handler.dater.create_data_for_v(x, y, z, md)
    return RedirectResponse(url="/dashboard/v", status_code=302)


@app.post("/g", status_code=200)
def get_trajectory_g(md: float = Form(...), x: float = Form(...), y: float = Form(...), z: float = Form(...)):
    deleter.delete_excel_type_file(type='v')
    handler.dater.create_data_for_v(x, y, z, md)
    return RedirectResponse(url="/dashboard/v", status_code=302)


# @app.post("/trajectory", status_code=200)
# def get_trajectory(request: Request):
#     files = request.files.getlist("files")
#     for file in files:
#         if file.filename != "":
#             file.save(os.path.join(f"{base_dir + '/data'}", file.filename))
#     return RedirectResponse(url="/dashboard", status_code=302)


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=7000, reload=True)
