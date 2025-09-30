# main.py
from fastapi import FastAPI, Depends, Request, Form
from db import getDB
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,RedirectResponse


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

from routes.upload import router as upload_router
from routes.dbQuery import router as db_router
# Include the router
app = FastAPI()
#prefix will be prepended before the route
app.include_router(upload_router, prefix="/api") 
app.include_router(db_router, prefix="/api")

@app.get("/")
async def root():
	#產生回應內容的程式

	#以json方式回傳頁面
	#return {"data":"Hello World"}

	#以html網頁方式回傳頁面
	return HTMLResponse(content=" World", status_code=200)

@app.get("/file/{p:path}")  #http://localhost/file/a/b/c/123.jpg
async def getPath(p: str):  #p  “a/b/c/123.jpg”
	return {"yourPath": p}

@app.get("/url/")  #http://localhost/url/?a=2&d=999
async def getParam(a: int, b:int=5, c:str | None=None): #注意有預設值與沒有的差異
	#a:必須要提供(不然報錯)
	#b:網址參數沒提供時，以預設值0帶入
	#c:可有可無，未提供時  None/null
	#d:忽略
	return {"Aa": a, "Bb":b , "Cc":c }

@app.get("/jump")
def redirect():
		return RedirectResponse(url="/", status_code=302)

@app.get("/temp/{name1}/{name2}")
def useTemplate(request:Request, name1:str, name2:str):
		return templates.TemplateResponse("temp.html", {"request":request,"realName": name1, "nickName": name2})



app.mount("/", StaticFiles(directory="www"))