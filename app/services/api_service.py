import os

import httpx

from app.forms.forms import APIForm, CreateAPIForm, ModifyAPIForm


async def get_apis_service(page: int, limit: int):
    query = """
        query GetApis($page: Int!, $limit: Int!){
            getApis(page: $page, pageSize: $limit) {
                items{
                    id
                    title
                    type
                    endpointUrl
                }
                totalCount
                pageSize
                page
            }
        }
    """
    variables = {"page": page, "limit": limit}
    async with httpx.AsyncClient() as client:
        res = await client.post(os.getenv("URL_GATEWAY") + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {os.getenv('GATEWAY_KEY')}"})
        return res

async def get_api_by_id_service(api_id):
    query = """
        query GetApiById($api_id: Int!){
            getApiById(apiId: $api_id) {
                id
                title
                type
                endpointUrl
                apiKey
                description
            }
        }
    """
    variables = {"api_id": int(api_id)}
    async with httpx.AsyncClient() as client:
        res = await client.post(os.getenv("URL_GATEWAY") + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {os.getenv('GATEWAY_KEY')}"})
        return res

async def create_api_service(form: CreateAPIForm):
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
    async with httpx.AsyncClient() as client:
        res = await client.post(os.getenv("URL_GATEWAY") + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {os.getenv('GATEWAY_KEY')}"})
        return res

async def modify_api_service(form: ModifyAPIForm, api_id: int):
    query = """
        mutation ModifyApi($apiId: Int!, $title: String!, $type: String!, $apiKey: String!, $description: String!, $endpointUrl: String!) {
            modifyApiById(apiId: $apiId, input: {
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
        "apiId": api_id,
        "title": form.title.data,
        "type": form.type.data,
        "apiKey": form.api_key.data,
        "description": form.description.data,
        "endpointUrl": form.endpoint_url.data
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(os.getenv("URL_GATEWAY") + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {os.getenv('GATEWAY_KEY')}"})
        return res