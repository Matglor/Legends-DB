
let todosLosPersonajes = [];
let filtroType = 'TODOS';
let filtroRarity = 'TODOS';

const mapeoColores = {
    'RED': 'var(--color-red)',
    'BLU': 'var(--color-blu)',
    'GRN': 'var(--color-grn)',
    'YEL': 'var(--color-yel)',
    'PUR': 'var(--color-pur)',
    'LGT': 'var(--color-lgt)',
    'DRK': 'var(--color-drk)'
};

// Iconos de atributos de color
const mapeoIconosElementos = {
    'RED': 'https://dblegends.net/assets/element_icons/HUD_ChaIco_AttributeRED1.webp',
    'BLU': 'https://dblegends.net/assets/element_icons/HUD_ChaIco_AttributeBLU1.webp',
    'GRN': 'https://dblegends.net/assets/element_icons/HUD_ChaIco_AttributeGRN1.webp',
    'YEL': 'https://dblegends.net/assets/element_icons/HUD_ChaIco_AttributeYEL1.webp',
    'PUR': 'https://dblegends.net/assets/element_icons/HUD_ChaIco_AttributePUR1.webp'
};

// Iconos de rareza
const mapeoIconosRarezas = {
    'LEGEND': 'https://dblegends.net/assets/rarity_icons/Gas_txtRarity_LEGEND.webp',
    'ULTRA': 'https://dblegends.net/assets/rarity_icons/Gas_txtRarity_ULTRA.webp'
};

window.addEventListener('DOMContentLoaded', () => {
    inicializarFiltros();
    cargarGrillaPersonajes();
});

async function inicializarFiltros() {
    try {
        const resRarity = await fetch('/api/rarities');
        const rarities = await resRarity.json();

        const rarityContainer = document.getElementById('rarityFilters');
        const selectRarity = document.getElementById('charRarity');

        selectRarity.innerHTML =
            '<option value="" disabled selected>Seleccione Rareza</option>';

        rarities.forEach(r => {
            rarityContainer.innerHTML += `
                <button class="btn btn-sm btn-rarity"
                    onclick="filtrarPorRarity('${r.nombre}', this)">
                    ${r.nombre}
                </button>`;

            selectRarity.innerHTML += `
                <option value="${r.id}">${r.nombre}</option>`;
        });

        const resType = await fetch('/api/types');
        const types = await resType.json();

        const typeContainer = document.getElementById('typeFilters');
        const selectType = document.getElementById('charType');

        selectType.innerHTML =
            '<option value="" disabled selected>Seleccione Elemento</option>';

        types.forEach(t => {
            typeContainer.innerHTML += `
                <button class="btn btn-sm btn-type btn-type-${t.nombre.toLowerCase()}"
                    onclick="filtrarPorType('${t.nombre}', this)">
                    ${t.nombre}
                </button>`;

            selectType.innerHTML += `
                <option value="${t.id}">${t.nombre}</option>`;
        });
    } catch (err) {
        console.error('Error al cargar catálogos iniciales:', err);
    }
}

async function cargarGrillaPersonajes() {
    try {
        const response = await fetch('/api/characters');
        todosLosPersonajes = await response.json();
        aplicarFiltrosYRenderizar();
    } catch (err) {
        console.error('Error al obtener los personajes:', err);
    }
}

function aplicarFiltrosYRenderizar() {
    const grid = document.getElementById('charactersGrid');
    grid.innerHTML = '';

    const filtrados = todosLosPersonajes.filter(char => {
        const cumpleType =
            filtroType === 'TODOS' || char.type_nombre === filtroType;

        const cumpleRarity =
            filtroRarity === 'TODOS' || char.rarity_nombre === filtroRarity;

        return cumpleType && cumpleRarity;
    });

    if (filtrados.length === 0) {
        grid.innerHTML = `
            <div class="col-12 text-center text-secondary py-5">
                <i class="fa-solid fa-box-open fa-2x mb-2"></i>
                <br>
                No se encontraron personajes con los filtros seleccionados.
            </div>`;
        return;
    }

    filtrados.forEach(char => {
        const colorHex = mapeoColores[char.type_nombre] || '#333';

        // Crear insignias
        let badges = '';

        // Icono del elemento
        if (mapeoIconosElementos[char.type_nombre]) {
            badges += `
                <img
                    src="${mapeoIconosElementos[char.type_nombre]}"
                    class="img-element-badge"
                    alt="${char.type_nombre}">
            `;
        }

        // Logo de rareza
        if (mapeoIconosRarezas[char.rarity_nombre]) {
            badges += `
                <img
                    src="${mapeoIconosRarezas[char.rarity_nombre]}"
                    class="img-rarity-badge"
                    alt="${char.rarity_nombre}">
            `;
        } else {
            badges += `
                <span class="badge-rarity-text">
                    ${char.rarity_nombre}
                </span>`;
        }

        // Insignias especiales
        if (char.es_zenkai === 1) {
            badges += '<span class="badge-special">ZENKAI</span>';
        }

        if (char.es_lf_ll === 1) {
            badges += '<span class="badge-special">LF/LL</span>';
        }

        // Tarjeta del personaje
        grid.innerHTML += `
            <div class="col">
                <div class="character-card d-flex h-100 shadow-sm">

                    <div
                        class="color-indicator"
                        style="background-color: ${colorHex};">
                    </div>

                    <div class="p-3 w-100 d-flex flex-column justify-content-between">

                        <div>
                            <div class="card-badge-container">
                                ${badges}
                            </div>

                            <h5
                                class="fw-bold mb-1"
                                style="font-size: 1.1rem; letter-spacing: 0.3px;">
                                ${char.nombre}
                            </h5>

                            <span class="character-id">
                                ${char.id}
                            </span>
                        </div>

                        <!-- ÚNICO BOTÓN: BORRAR -->
                        <div class="text-end mt-3 pt-2 border-top border-secondary">
                            <button
                                type="button"
                                class="btn btn-sm btn-outline-danger"
                                style="font-size: 0.8rem;"
                                onclick="eliminarPersonaje('${char.id}')"
                                title="Borrar personaje"
                                aria-label="Borrar personaje">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </div>

                    </div>
                </div>
            </div>`;
    });
}

function filtrarPorType(type, btn) {
    filtroType = type;

    document.querySelectorAll('#typeFilters .btn').forEach(b => {
        b.classList.remove('active');
    });

    if (btn) {
        btn.classList.add('active');
    }

    aplicarFiltrosYRenderizar();
}

function filtrarPorRarity(rarity, btn) {
    filtroRarity = rarity;

    document.querySelectorAll('#rarityFilters .btn').forEach(b => {
        b.classList.remove('active');
    });

    if (btn) {
        btn.classList.add('active');
    }

    aplicarFiltrosYRenderizar();
}

function abrirModalCrear() {
    document.getElementById('modalTitle').innerText =
        'Registrar Personaje';

    document.getElementById('characterForm').reset();
    document.getElementById('charId').disabled = false;
}

function abrirModalEditar(id) {
    const char = todosLosPersonajes.find(c => c.id === id);

    if (!char) return;

    document.getElementById('modalTitle').innerText =
        'Modificar Personaje';

    document.getElementById('charId').value = char.id;
    document.getElementById('charId').disabled = true;
    document.getElementById('charNombre').value = char.nombre;
    document.getElementById('charType').value = char.type_id;
    document.getElementById('charRarity').value = char.rarity_id;
    document.getElementById('charZenkai').checked = char.es_zenkai === 1;
    document.getElementById('charLfLl').checked = char.es_lf_ll === 1;

    const modalEl = document.getElementById('characterModal');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

    modal.show();
}

async function guardarPersonaje() {
    const id = document.getElementById('charId').value.trim();
    const nombre = document.getElementById('charNombre').value.trim();
    const rarity_id = parseInt(
        document.getElementById('charRarity').value
    );
    const type_id = parseInt(
        document.getElementById('charType').value
    );

    const es_zenkai =
        document.getElementById('charZenkai').checked ? 1 : 0;

    const es_lf_ll =
        document.getElementById('charLfLl').checked ? 1 : 0;

    if (!id || !nombre) {
        alert('Por favor rellene los campos obligatorios.');
        return;
    }

    const tags_ids = [];

    const payload = {
        id,
        nombre,
        rarity_id,
        type_id,
        es_zenkai,
        es_lf_ll,
        tags_ids
    };

    try {
        const res = await fetch('/api/characters', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            const modalEl = document.getElementById('characterModal');
            const modal = bootstrap.Modal.getInstance(modalEl);

            if (modal) {
                modal.hide();
            }

            cargarGrillaPersonajes();
        } else {
            alert('Ocurrió un error al intentar guardar el personaje.');
        }
    } catch (err) {
        console.error(err);
    }
}

async function eliminarPersonaje(id) {
    if (!confirm(
        `¿Está seguro de que desea eliminar permanentemente al personaje con ID ${id}?`
    )) {
        return;
    }

    try {
        const res = await fetch(`/api/characters/${id}`, {
            method: 'DELETE'
        });

        if (res.ok) {
            cargarGrillaPersonajes();
        } else {
            alert('Error al intentar eliminar el registro.');
        }
    } catch (err) {
        console.error(err);
    }
}
