#####################################################
# Запускаем приложение fastapi для интеграции в нем
# приложений marimo
# 30.01.2025, 29.03.2025
#####################################################


from typing import Callable, Coroutine
from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import marimo
import os
import toml


app_dir = os.path.dirname(__file__) # каталог приложения

templates_dir = os.path.join(os.path.dirname(__file__), "templates") # шаблоны HTML
examples_dir = os.path.join(os.path.dirname(__file__), "") # примеры marimo

# подгружаем оглавление из файла toml
toc = toml.load("toc.toml")

# сервер приложений marimo
server = marimo.create_asgi_app()

# собираем примеры (ссылки на блокноты marimo)
items : list[str] = []
for i, item in enumerate(toc["Оглавление"].items()):
    it = item[1] # очередной элемент оглавления

    name = it["name"] if "name" in it else "Без имени"
    title = it["title"] if "title" in it else ""
    url = it["url"] if "url" in it else "/404"
    app_name = os.path.splitext(url)[0]
    app_path = os.path.join(examples_dir, url)
    # регистрируем имена приложений marimo    
    app_type = it["app_type"] if "app_type" in it else ""
    if app_type=="marimo":
        server = server.with_app(path=f"/{app_name}", root=app_path)
       
    prm = it["prm"] if "prm" in it else "" # передаваемые параметры
    url = app_name + "?"+prm if prm else app_name
    name = f"{i+1}. {name}"   
    items.append({"name":name, "title":title, "url":url})

# Вывод исходных кодов
source_code = "src.py"
app_path =  os.path.join(examples_dir, source_code)
server = server.with_app(path=f"/src", root=app_path)
         
# Приложение FastAPI 
app = FastAPI() # создаем приложение FastAPI 

# Создаем шаблоны Jinja 2
templates = Jinja2Templates(directory=templates_dir)
   
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(        
        "toc.html", {"request": request, "items": items}      
    )
    
# Делаем приложения marimo доступными из FastAPI
app.mount("/", server.build())

# Запускаем сервер
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)