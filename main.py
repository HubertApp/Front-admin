from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from app.forms.forms import APIForm
import requests, dotenv, os
from starlette.middleware.sessions import SessionMiddleware

dotenv.load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


@app.get("/")
async def index(request: Request):
    async with httpx.AsyncClient() as client:
        query = """
            query {
                getApis {
                    id
                    title
                    type
                    apiKey
                    description
                    endpointUrl
                }
            }
        """
        response = await client.post(os.getenv("URL_GATEWAY") + "/graphql", json={"query": query}, headers={"Authorization": f"Bearer {os.getenv('GATEWAY_KEY')}"})
    if response.status_code == 200:
        apis = response.json().get("data", {}).get("getApis", [])
        return templates.TemplateResponse("index.jinja", {"request": request, "apis": apis, "messages": request.session.pop('flash_messages', [])})
    return templates.TemplateResponse("index.jinja", {"request": request, "messages": request.session.pop('flash_messages', []), "apis": []})

@app.get("/api")
@app.post("/api")
async def api_list(request: Request):
    form = APIForm()
    request.session.setdefault('flash_messages', [])
    if request.method == "POST":
        form_data = await request.form()
        form = APIForm(formdata=form_data)
        if form.validate():
            query = """
                mutation CreateApi($title: String!, $type: String!, $apiKey: String!, $description: String!, $endpointUrl: String!) {
                    createApi(input: {
                        title: $title,
                        type: $type,
                        apiKey: $apiKey,
                        description: $description,
                        endpointUrl: $endpointUrl
                    }) {
                        id
                        title
                        type
                        apiKey
                        description
                        endpointUrl
                    }
                }
            """
            variables = {
                "title": form.title.data,
                "type": form.type.data,
                "apiKey": form.api_key.data,
                "description": form.description.data,
                "endpointUrl": form.endpoint_url.data
            }
            # Logique à changer quand le microservice sera directement connecté à la gateway
            async with httpx.AsyncClient() as client:
                response = await client.post(os.getenv("URL_GATEWAY") + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {os.getenv('GATEWAY_KEY')}"})
            if response.status_code == 200:
                print("Données envoyées avec succès au gateway.")
                request.session['flash_messages'].append(("API enregistrée.", "success"))
                return RedirectResponse(url='/', status_code=303)
 
            request.session['flash_messages'].append(("Erreur lors de l'enregistrement de l'API.", "error"))
        else:
            request.session['flash_messages'].append(("Données de formulaire invalides.", "error"))

    return templates.TemplateResponse("add_api.jinja", {"request": request, "form" : form, "messages": request.session.pop('flash_messages', [])})