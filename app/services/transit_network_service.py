import os

import httpx

from app.core.config import properties, secrets
from app.forms.forms import CreateTransitNetworkForm, ModifyTransitNetworkForm


async def get_transit_network_service(offset: int, limit: int):
    query = """
        query GetTransitNetworks($offset: Int!, $limit: Int!){
            getRegistredTransitNetworks(offset: $offset, limit: $limit) {
                items{
                    externalId
                    name
                    description
                    endpointUrl
                }
                totalCount
                totalPages
                limit
                offset
            }
        }
    """
    variables = {"offset": offset, "limit": limit}
    async with httpx.AsyncClient() as client:
        res = await client.post(properties.URL_GATEWAY + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {secrets.GATEWAY_KEY}"})
        return res

async def get_transit_network_by_id_service(api_id):
    query = """
        query GetTransitNetwork($api_id: Int!){
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
        res = await client.post(properties.URL_GATEWAY + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {secrets.GATEWAY_KEY}"})
        return res

async def create_transit_network_service(form: CreateTransitNetworkForm):
    query = """
                    mutation CreateTN($name: String!, $external_id: String!, $fournisseur_id: String!, $description: String!, $country_code: String!, $city_or_region: String!) {
                        createTransitNetwork(data: {
                            name: $name,
                            externalId: $external_id,
                            fournisseurId: $fournisseur_id,
                            description: $description,
                            countryCode: $country_code,
                            cityOrRegion: $city_or_region
                        }) {
                            name,
                            externalId,
                            fournisseurId,
                            description,
                            countryCode,
                            cityOrRegion
                        }
                    }
                """

    variables = {
        "name" : form.title.data,
        "external_id" : form.external_id.data,
        "description" : form.description.data,
        "country_code" : form.country_code.data,
        "city_or_region" : form.city_or_region.data,
        "fournisseur_id" : "FR_TRANSPORT_GOUV"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(properties.URL_GATEWAY + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {secrets.GATEWAY_KEY}"})
        return res

async def modify_transit_network_service(form: ModifyTransitNetworkForm, api_id: int):
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
        res = await client.post(properties.URL_GATEWAY + "/graphql", json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {secrets.GATEWAY_KEY}"})
        return res