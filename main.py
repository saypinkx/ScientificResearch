from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
from dashboard import dash_app
import uvicorn
from fastapi import File, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import  List

app = FastAPI()
app.mount("/dashboard", WSGIMiddleware(dash_app.server))
templates = Jinja2Templates(directory="templates")
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=base_dir + '/templates')


@app.get('/')
def index():
    return "Hello"

def delete_excel_files():
    folder_path = base_dir+'/data'
    filenames = os.listdir(folder_path)
    for filename in filenames:
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)

@app.get("/trajectory")
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/trajectory", status_code=200)
def get_trajectory(file: List[UploadFile] = File(...)):
    delete_excel_files()
    files = file
    for file in files:
        with open(f'data/{file.filename}', 'wb') as f:
            content = file.file.read()
            f.write(content)
            f.close()
    return RedirectResponse(url="/dashboard", status_code=302)
# @app.post("/trajectory", status_code=200)
# def get_trajectory(request: Request):
#     files = request.files.getlist("files")
#     for file in files:
#         if file.filename != "":
#             file.save(os.path.join(f"{base_dir + '/data'}", file.filename))
#     return RedirectResponse(url="/dashboard", status_code=302)


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=7000, reload=True)
