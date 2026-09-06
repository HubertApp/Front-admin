let AOMDisponibles = [];
async function fetchToutesLesAOMs(URL_GATEWAY) {
  searchInput.disabled = true;
  const placeholderInitial = searchInput.placeholder;
  searchInput.placeholder = "Chargement des réseaux en cours...";
  const query = `
    query ObtenirLesAOM($fournisseurId: String!) {
      searchTransitNetworksDatasets(fournisseurId: $fournisseurId) {
        externalId
        name
        cityOrRegion
        countryCode
        resources {
          title
          format
          endpointUrl
        }
      }
    }
  `;
  const GRAPHQL_ENDPOINT = URL_GATEWAY;
  const variables = {
    fournisseurId: "FR_TRANSPORT_GOUV"
  };

  try {
    const response = await fetch(GRAPHQL_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
      body: JSON.stringify({ query, variables })
    });
    const jsonResponse = await response.json();
    if (jsonResponse.errors) {
      console.error("Erreur renvoyée par GraphQL :", jsonResponse.errors);
      return;
    }
    AOMDisponibles = jsonResponse.data.searchTransitNetworksDatasets;

  } catch (error) {
    console.error("Erreur réseau ou serveur inaccessible :", error);
  } finally {
    searchInput.disabled = false;
    searchInput.placeholder = placeholderInitial;
  }
}