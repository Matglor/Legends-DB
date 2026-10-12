
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('currentYear').textContent =
        new Date().getFullYear();

    cargarCatalogos();

    document.getElementById('addCharacterForm')
        .addEventListener('submit', guardarNuevoPersonaje);
});

async function cargarCatalogos() {
    const typeSelect = document.getElementById('newCharType');
    const raritySelect = document.getElementById('newCharRarity');

    try {
        const [typesResponse, raritiesResponse] = await Promise.all([
            fetch('/api/types'),
            fetch('/api/rarities')
        ]);

        if (!typesResponse.ok || !raritiesResponse.ok) {
            throw new Error('No se pudieron cargar los catálogos.');
        }

        const [types, rarities] = await Promise.all([
            typesResponse.json(),
            raritiesResponse.json()
        ]);

        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            option.textContent = type.nombre;
            typeSelect.appendChild(option);
        });

        rarities.forEach(rarity => {
            const option = document.createElement('option');
            option.value = rarity.id;
            option.textContent = rarity.nombre;
            raritySelect.appendChild(option);
        });

    } catch (error) {
        mostrarMensaje(
            error.message || 'Error al cargar los datos.',
            'danger'
        );
    }
}

async function guardarNuevoPersonaje(event) {
    event.preventDefault();

    const button = document.getElementById('saveCharacterButton');

    const id = document.getElementById('newCharId')
        .value.trim().toUpperCase();

    const nombre = document.getElementById('newCharName')
        .value.trim();

    const type_id = Number(
        document.getElementById('newCharType').value
    );

    const rarity_id = Number(
        document.getElementById('newCharRarity').value
    );

    if (!id || !nombre || !type_id || !rarity_id) {
        mostrarMensaje(
            'Completa todos los campos obligatorios.',
            'danger'
        );
        return;
    }

    const payload = {
        id,
        nombre,
        type_id,
        rarity_id,
        es_zenkai: document.getElementById('newCharZenkai').checked ? 1 : 0,
        es_lf_ll: document.getElementById('newCharLfLl').checked ? 1 : 0,
        tags_ids: []
    };

    button.disabled = true;

    button.innerHTML = `
        <span
            class="spinner-border spinner-border-sm me-2"
            aria-hidden="true">
        </span>
        Guardando...
    `;

    try {
        const response = await fetch('/api/characters', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(
                result.detail ||
                'No se pudo guardar el personaje. Comprueba que el ID no esté repetido.'
            );
        }

        mostrarMensaje(
            '¡Personaje guardado correctamente! Volviendo al catálogo...',
            'success'
        );

        window.setTimeout(() => {
            window.location.href = '/';
        }, 900);

    } catch (error) {
        mostrarMensaje(
            error.message || 'Ocurrió un error al guardar el personaje.',
            'danger'
        );

        button.disabled = false;

        button.innerHTML = `
            <i class="fa-solid fa-floppy-disk me-2"></i>
            Guardar personaje
        `;
    }
}

function mostrarMensaje(mensaje, tipo) {
    const container = document.getElementById('formMessage');

    container.innerHTML = '';

    const alert = document.createElement('div');

    alert.className = `alert alert-${tipo} mb-0`;
    alert.textContent = mensaje;

    container.appendChild(alert);
}
