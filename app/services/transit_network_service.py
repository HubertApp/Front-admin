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
                    countryCode
                    cityOrRegion
                    fournisseurId
                    status
                    statusLabel
                    resources {
                        title
                        format
                        endpointUrl
                    }
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
        res = await client.post(properties.URL_GATEWAY, json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {secrets.GATEWAY_KEY}"})
        return res

async def get_transit_network_by_external_id_service(external_id: str):
    # MS-Admin n'expose pas de query dediee a la recuperation d'un seul reseau :
    # on recupere la liste et on filtre cote front. A remplacer par une vraie
    # query getTransitNetworkByExternalId si la liste devient trop grande.
    return await get_transit_network_service(0, 1000)

async def create_transit_network_service(form: CreateTransitNetworkForm):
    query = """
                mutation CreateTN($name: String!, $external_id: String!, $fournisseur_id: String!, $description: String!, $country_code: String!, $city_or_region: String!, $resources: [ResourceInput!]!) {
                    createTransitNetwork(data: {
                        name: $name,
                        externalId: $external_id,
                        fournisseurId: $fournisseur_id,
                        description: $description,
                        countryCode: $country_code,
                        cityOrRegion: $city_or_region,
                        resources: $resources
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
        "fournisseur_id" : "FR_TRANSPORT_GOUV",
        "resources" : form.resources.data
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(properties.URL_GATEWAY, json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {secrets.GATEWAY_KEY}"})
        return res

async def modify_transit_network_service(form: ModifyTransitNetworkForm, external_id: str):
    query = """
        mutation UpdateTransitNetwork($external_id: String!, $name: String!, $fournisseur_id: String!, $description: String!, $country_code: String!, $city_or_region: String!, $endpoint_url: String, $resources: [ResourceInput!]) {
            updateTransitNetwork(externalId: $external_id, data: {
                externalId: $external_id,
                name: $name,
                fournisseurId: $fournisseur_id,
                description: $description,
                countryCode: $country_code,
                cityOrRegion: $city_or_region,
                endpointUrl: $endpoint_url,
                resources: $resources
            }) {
                name
                externalId
                fournisseurId
                description
                countryCode
                cityOrRegion
            }
        }
    """
    variables = {
        "external_id": external_id,
        "name": form.title.data,
        "description": form.description.data,
        "country_code": form.country_code.data,
        "city_or_region": form.city_or_region.data,
        "fournisseur_id": "FR_TRANSPORT_GOUV",
        "endpoint_url": form.endpoint_url.data,
        "resources": form.resources.data
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(properties.URL_GATEWAY, json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {secrets.GATEWAY_KEY}"})
        return res

async def retrigger_aggregation_service(external_id: str):
    query = """
        mutation RetriggerAggregation($external_id: String!) {
            retriggerAggregation(externalId: $external_id) {
                externalId
                name
                status
                statusLabel
            }
        }
    """
    variables = {"external_id": external_id}
    async with httpx.AsyncClient() as client:
        res = await client.post(properties.URL_GATEWAY, json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {secrets.GATEWAY_KEY}"})
        return res
