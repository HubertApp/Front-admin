const searchInput = document.getElementById('search-input');
const resultsList = document.getElementById('results-list');

// Les champs à pré-remplir
const fieldId = document.getElementById('external_id');
const fieldRegion = document.getElementById('city_or_region');
const fieldCountryCode = document.getElementById('country_code');
const fieldName = document.getElementById('title');

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
    console.log(item)
    fieldId.value = item.externalId || 'N/A';
    fieldRegion.value = item.cityOrRegion || 'N/A';
    fieldName.value = item.name || 'N/A';
    fieldCountryCode.value = item.countryCode || 'N/A';
}

function clearFormFields() {
    fieldId.value = '';
    fieldRegion.value = '';
}
document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !resultsList.contains(e.target)) {
        resultsList.classList.add('hidden');
    }
});