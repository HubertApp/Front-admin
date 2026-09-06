from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

import requests, dotenv, os
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import properties
from app.forms.forms import CreateTransitNetworkForm, ModifyTransitNetworkForm
from app.objects.transit_network_obj import TransitNetworkResponseObj
from app.services.transit_network_service import get_transit_network_service, create_transit_network_service, get_transit_network_by_external_id_service, modify_transit_network_service, retrigger_aggregation_service

dotenv.load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

templates.env.globals['URL_GATEWAY'] = properties.URL_GATEWAY
@app.get("/")
async def index(request: Request, page: int = 1, limit: int = 25):
    response = await get_transit_network_service(0, limit)
    if response.status_code == 200:
        data = response.json().get("data", {}).get("getRegistredTransitNetworks", [])
        return templates.TemplateResponse("index.jinja", {"request": request, "data": data, "messages": request.session.pop('flash_messages', [])})
    return templates.TemplateResponse("index.jinja", {"request": request, "messages": request.session.pop('flash_messages', []), "data": {"items": [], "total": 0, "totalPages": 0, "page": page}})

@app.get("/transit-networks/create")
@app.post("/transit-networks/create")
async def transit_network_create(request: Request):
    form = CreateTransitNetworkForm()
    request.session.setdefault('flash_messages', [])
    if request.method == "POST":
        form_data = await request.form()
        form = CreateTransitNetworkForm(formdata=form_data)
        if form.validate():
            response = await create_transit_network_service(form)
            if response.status_code == 200:
                print("Données envoyées avec succès au gateway.")
                request.session['flash_messages'].append(("Réseau de transport enregistré.", "success"))
                return RedirectResponse(url='/', status_code=303)

            request.session['flash_messages'].append(("Erreur lors de l'enregistrement du réseau de transport.", "error"))
        else:
            request.session['flash_messages'].append(("Données de formulaire invalides.", "error"))

    return templates.TemplateResponse("add_transit_network.jinja", {"request": request, "form" : form, "messages": request.session.pop('flash_messages', [])})


@app.post("/transit-networks/{external_id}/retrigger")
async def transit_network_retrigger(request: Request, external_id: str):
    request.session.setdefault('flash_messages', [])
    response = await retrigger_aggregation_service(external_id)
    try:
        payload = response.json()
    except ValueError:
        payload = {}
    erreurs = payload.get("errors")
    donnees = (payload.get("data") or {}).get("retriggerAggregation")

    if donnees and not erreurs:
        request.session['flash_messages'].append(("Agrégation relancée.", "success"))
    else:
        motif = " ; ".join(e.get("message", "") for e in erreurs) if erreurs else f"réponse HTTP {response.status_code}"
        request.session['flash_messages'].append((f"Relance impossible : {motif}", "error"))

    return RedirectResponse(url=f'/transit-networks/{external_id}', status_code=303)


@app.get("/transit-networks/{external_id}")
@app.post("/transit-networks/{external_id}")
async def transit_network_details(request: Request, external_id: str):
    request.session.setdefault('flash_messages', [])
    transit_network_response = await get_transit_network_by_external_id_service(external_id)
    items = transit_network_response.json().get("data", {}).get("getRegistredTransitNetworks", {}).get("items") or []
    data = next((item for item in items if item.get("externalId") == external_id), {})
    data["resources"] = data.get("resources") or []
    form = ModifyTransitNetworkForm(obj=TransitNetworkResponseObj(**data))
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
            response = await modify_transit_network_service(new_data_form, external_id)
            if response.status_code == 200:
                print("Données envoyées avec succès au gateway.")
                request.session['flash_messages'].append(("Réseau de transport enregistré.", "success"))
                return RedirectResponse(url='/', status_code=303)

            request.session['flash_messages'].append(("Erreur lors de l'enregistrement du réseau de transport.", "error"))
        else:
            request.session['flash_messages'].append(("Données de formulaire invalides.", "error"))
    return templates.TemplateResponse("transit_network_details.jinja", {"request": request, "form": form, "transit_network_infos": data, "messages": request.session.pop('flash_messages', [])})
