const searchInput = document.getElementById('search-input');
const resultsList = document.getElementById('results-list');

// Les champs à pré-remplir
const fieldId = document.getElementById('external_id');
const fieldRegion = document.getElementById('city_or_region');
const fieldCountryCode = document.getElementById('country_code');
const fieldName = document.getElementById('title');
const resourcesContainer = document.getElementById('resources-container');


searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().replace(/\s+/g, "");

    if (query.length === 0) {
        resultsList.classList.add('hidden');
        clearFormFields();
        return;
    }

    const filtered = AOMDisponibles
        .filter(item => {
            const cleanName = item.name.toLowerCase().replace(/\s+/g, "");
            return cleanName.includes(query);
        })
        .slice(0, 5);

    if (filtered.length > 0) {
        renderResults(filtered);
        resultsList.classList.remove('hidden');
    } else {
        resultsList.innerHTML = '<li class="disabled"><a>Aucun résultat</a></li>';
        resultsList.classList.remove('hidden');
    }
});

function renderResults(results) {
    resultsList.innerHTML = '';

    results.forEach(item => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.textContent = item.name;

        a.addEventListener('click', () => {
            searchInput.value = item.name;

            resultsList.classList.add('hidden');

            fillFormFields(item);
        });

        li.appendChild(a);
        resultsList.appendChild(li);
    });
}

function fillFormFields(item) {
    console.log(AOMDisponibles)
    fieldId.value = item.externalId || 'N/A';
    fieldRegion.value = item.cityOrRegion || 'N/A';
    fieldName.value = item.name || 'N/A';
    fieldCountryCode.value = item.countryCode || 'N/A';
    fillResourcesFormFields(item.resources);
}

function fillResourcesFormFields(resources) {
    resourcesContainer.innerHTML = "";
    if (resources && resources.length > 0) {
        resources.forEach((resource, index) => {
            const resourceHTML = `
                <tr class="hover">
                    <td>
                        <input type="text" 
                               name="resources-${index}-title" 
                               value="${resource.title || ''}" 
                               class="input input-sm input-ghost w-full bg-base-200/50 cursor-default" 
                               readonly>
                    </td>
                    <td>
                        <input type="text" 
                               name="resources-${index}-format" 
                               value="${resource.format || ''}" 
                               class="input input-sm input-ghost w-full bg-base-200/50 cursor-default" 
                               readonly>
                    </td>
                    <td>
                        <input type="text" 
                               name="resources-${index}-endpointUrl" 
                               value="${resource.endpointUrl || ''}" 
                               class="input input-sm input-ghost w-full bg-base-200/50 cursor-default" 
                               readonly>
                    </td>
                </tr>
            `;
            resourcesContainer.insertAdjacentHTML('beforeend', resourceHTML);
        });
    } else {
        resourcesContainer.innerHTML = `
            <tr>
                <td colspan="2" class="text-center py-6 text-sm text-base-content/50 italic">
                    Aucune ressource pour ce réseau.
                </td>
            </tr>
        `;
    }
}

function clearFormFields() {
    fieldId.value = '';
    fieldRegion.value = '';
    resourcesContainer.innerHTML = "";
}
document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !resultsList.contains(e.target)) {
        resultsList.classList.add('hidden');
    }
});