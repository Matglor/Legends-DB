# Legends DB Clone

## 1. Nombre del proyecto

**Legends DB Clone — Dragon Ball Legends Database**

## 2. Descripción

Legends DB Clone es una aplicación web que permite consultar y administrar un catálogo de personajes del videojuego Dragon Ball Legends.

El sistema cuenta con una interfaz gráfica que permite visualizar los personajes registrados, filtrar los resultados por elemento y rareza, añadir nuevos personajes y eliminar registros existentes.

La aplicación utiliza una API desarrollada con FastAPI para conectar la interfaz con la lógica del servidor y las operaciones de la base de datos.

### Funcionalidades principales

- Visualización del catálogo de personajes.
- Filtrado de personajes por elemento y rareza.
- Registro de nuevos personajes.
- Eliminación de personajes existentes.
- Administración de información como el ID, nombre, elemento, rareza y características especiales.
- Consulta de catálogos de elementos, rarezas y etiquetas mediante la API.

## 3. Tecnologías utilizadas

- **Python:** lenguaje de programación utilizado para el backend.
- **FastAPI:** framework para desarrollar la API y gestionar las rutas del servidor.
- **HTML5:** estructura de las páginas web.
- **CSS3:** estilos y diseño de la interfaz.
- **JavaScript:** interacción con la interfaz y comunicación con la API.
- **Bootstrap:** diseño adaptable y componentes visuales.
- **Font Awesome:** iconos utilizados en la interfaz.
- **Base de datos:** almacenamiento de los personajes y sus categorías mediante los módulos de acceso a datos del proyecto.

## 4. Instrucciones para instalar el proyecto

### Requisitos previos

- Python 3.10 o superior.
- pip, administrador de paquetes de Python.
- Los archivos del proyecto.
- Acceso a la base de datos configurada para la aplicación.

### Paso 1. Descargar el proyecto

Descarga o clona el repositorio y extrae los archivos, si corresponde.

### Paso 2. Abrir la carpeta del proyecto

Abre una terminal y sitúate en la carpeta principal, donde se encuentra `main.py`.

### Paso 3. Crear un entorno virtual (opcional, recomendado)

En Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

En Linux o macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 4. Instalar las dependencias

Si el proyecto incluye un archivo `requirements.txt`, ejecuta:

```bash
pip install -r requirements.txt
```

Si no existe ese archivo, instala como mínimo FastAPI y Uvicorn:

```bash
pip install fastapi uvicorn
```

Instala también cualquier otra dependencia que utilicen los módulos `crud.py` y `models.py` para acceder a la base de datos.

## 5. Instrucciones para ejecutar el proyecto

### Paso 1. Iniciar el servidor

Desde la carpeta principal del proyecto, ejecuta:

```bash
uvicorn main:app --reload
```

Este comando inicia el servidor de desarrollo de FastAPI y permite recargar la aplicación automáticamente cuando se realizan cambios en el código.

### Paso 2. Abrir la aplicación

Abre el navegador y visita:

- **Aplicación web:** http://127.0.0.1:8000/
- **Página para añadir personajes:** http://127.0.0.1:8000/add-character
- **Documentación interactiva de la API:** http://127.0.0.1:8000/docs

### Paso 3. Utilizar el sistema

Desde la interfaz principal se pueden consultar y filtrar los personajes, añadir nuevos registros y eliminar personajes existentes.

La página de registro permite introducir los datos del personaje y guardarlos mediante la API.

**Nota:** para que todas las funcionalidades estén disponibles, la conexión a la base de datos debe estar configurada correctamente y los archivos del frontend deben encontrarse en las ubicaciones esperadas por el servidor.

## 6. Estructura general del sistema

La estructura principal del proyecto es la siguiente:

```text
El_del_legends/
│
├── main.py
├── crud.py
├── models.py
├── index.html
├── add-character.html
├── README.md
│
└── static/
    ├── app.js
    ├── add-character.js
    └── styles.css
```

### Descripción de los archivos

- **`main.py`:** archivo principal del backend. Configura FastAPI, define las rutas de la aplicación y expone los endpoints para consultar, registrar y eliminar personajes.
- **`crud.py`:** contiene las operaciones para interactuar con la base de datos.
- **`models.py`:** define los modelos de datos y las validaciones utilizadas por la API.
- **`index.html`:** página principal que muestra el catálogo de personajes y sus filtros.
- **`add-character.html`:** página con el formulario para registrar nuevos personajes.
- **`static/app.js`:** gestiona la carga del catálogo, los filtros y las operaciones de los personajes desde la interfaz principal.
- **`static/add-character.js`:** gestiona el formulario de registro y envía los datos del nuevo personaje a la API.
- **`static/styles.css`:** contiene los estilos visuales de la aplicación.
- **`README.md`:** documento con la descripción del proyecto y las instrucciones de instalación y ejecución.

## 7. Endpoints principales de la API

| Método HTTP | Endpoint | Función |
|---|---|---|
| GET | `/api/characters` | Obtener todos los personajes. |
| PUT | `/api/characters` | Registrar o actualizar un personaje. |
| DELETE | `/api/characters/{character_id}` | Eliminar un personaje por su ID. |
| GET | `/api/types` | Obtener los elementos disponibles. |
| GET | `/api/rarities` | Obtener las rarezas disponibles. |
| GET | `/api/tags` | Obtener las etiquetas disponibles. |

## 8. Autor

Proyecto académico desarrollado como una aplicación web para la administración de un catálogo de personajes de Dragon Ball Legends.