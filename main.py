from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

import requests, dotenv, os
from starlette.middleware.sessions import SessionMiddleware

from app.forms.forms import CreateTransitNetworkForm, ModifyTransitNetworkForm
from app.objects.api_obj import ApiResponseObj
from app.services.api_service import get_apis_service, create_api_service, get_api_by_id_service, modify_api_service

dotenv.load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


@app.get("/")
async def index(request: Request, page: int = 1, limit: int = 25):
    response = await get_apis_service(0, limit)
    if response.status_code == 200:
        data = response.json().get("data", {}).get("getRegistredApis", [])
        return templates.TemplateResponse("index.jinja", {"request": request, "data": data, "messages": request.session.pop('flash_messages', [])})
    return templates.TemplateResponse("index.jinja", {"request": request, "messages": request.session.pop('flash_messages', []), "data": {"items": [], "total": 0, "totalPages": 0, "page": page}})

@app.get("/api/create")
@app.post("/api/create")
async def api_create(request: Request):
    form = CreateTransitNetworkForm()
    request.session.setdefault('flash_messages', [])
    if request.method == "POST":
        form_data = await request.form()
        form = CreateTransitNetworkForm(formdata=form_data)
        if form.validate():
            response = await create_api_service(form)
            if response.status_code == 200:
                print("Données envoyées avec succès au gateway.")
                request.session['flash_messages'].append(("API enregistrée.", "success"))
                return RedirectResponse(url='/', status_code=303)
 
            request.session['flash_messages'].append(("Erreur lors de l'enregistrement de l'API.", "error"))
        else:
            request.session['flash_messages'].append(("Données de formulaire invalides.", "error"))

    return templates.TemplateResponse("add_transit_network.jinja", {"request": request, "form" : form, "messages": request.session.pop('flash_messages', [])})


@app.get("/api/{api_id}")
@app.post("/api/{api_id}")
async def api_details(request: Request, api_id: str):
    request.session.setdefault('flash_messages', [])
    api_infos_response = await get_api_by_id_service(api_id)
    data = api_infos_response.json().get("data", {}).get("getApiById", {})
    form = ModifyTransitNetworkForm(obj=ApiResponseObj(**data))
    if request.method == "POST":
        form_data = await request.form()
        new_data_form = ModifyTransitNetworkForm(form_data)
        if new_data_form.validate():
            old_datas = {
                cle: valeur
                for cle, valeur in form.data.items()
                if cle not in ['submit', 'csrf_token']
            }
            new_datas = {
                cle: valeur
                for cle, valeur in form_data.items()
                if cle not in ['submit', 'csrf_token']
            }
            if old_datas == new_datas:
                return RedirectResponse(url='/', status_code=303)
            response = await modify_api_service(new_data_form, int(api_id))
            if response.status_code == 200:
                print("Données envoyées avec succès au gateway.")
                request.session['flash_messages'].append(("API enregistrée.", "success"))
                return RedirectResponse(url='/', status_code=303)

            request.session['flash_messages'].append(("Erreur lors de l'enregistrement de l'API.", "error"))
        else:
            request.session['flash_messages'].append(("Données de formulaire invalides.", "error"))
    return templates.TemplateResponse("api_details.jinja", {"request": request, "form": form, "api_infos": data, "messages": request.session.pop('flash_messages', [])})