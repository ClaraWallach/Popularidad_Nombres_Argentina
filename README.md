#Popularidad de nombres en Argentina (1922-2024)
Visualización interactiva de la popularidad de un nombre propio en Argentina 

LINK DEL PROYECTO: https://popularidad-nombres-argentina.web.app

INDICE:
1. [Descripción general](#descripción-general)
2. [Proceso de realización](#proceso-de-realización)
3. [Tecnologías utilizadas](#tecnologías-utilizadas)
4. [Estructura de los archivos](#estructura-de-los-archivos)
5. [Instalación y configuración](#instalación-y-configuración)

## Descripción general
Este proyecto premite ver la popularidad de un nombre propio en Argentina entre 1922 y 1924. El usuario puedo consultar un nombre y obtener un grafico con el porcentaje sobre el total de nacimientos por año y la cantidad absoluta de nacimientos por año con el nombre buscado. 

Los datos utilizados son de datos.gob.ar  Los datos fueron procesados, limpiados y almacenados en una base de datos MySQL que es consultada a través de una API. Luego desplegue el proyecto en google cloud para que pueda ser consultado desde la web.

<img width="1789" height="686" alt="image" src="https://github.com/user-attachments/assets/d58c9beb-d506-47b4-9eec-183ae4eff207" />

## Proceso de realización
**Limpieza y normalizacion de datos**
Para realizar la app use dos datasets con la información sobre los nombres; uno con datos entre 1922 y 2015 y otro con datos entre 2012 y 2024. Los archivos tienen algunas diferencias ya que el primero tiene los nombres cargados de forma completa (“Juan Martin”) y el segundo de manera individual (“Juan”, “Martin”). Por lo tanto dividí los nombres del primer conjunto de datos para que las búsquedas sean siempre por el nombre individual. Luego tuve que limpiar errores en la codificación de algunas letras, nombres repetidos o distintas inconsistencias.

Para realizar el gráfico utilice un dataset con la cantidad de nacimientos en argentina por año. De esta manera se puede calcular el porcentaje de nacidos por año con un determinado nombre y saber cual es la popularidad real ya que hay mucha diferencia entre la cantidad de nacimientos hoy y hace cincuenta años lo que genera 'problemas' sí miramos las cantidades absolutas.

**API**
Utilizando fast api cree una api que se conecta con la base de datos y permite buscar un nombre. Devuelve un archivo json con la cantidad absoluta y el porcentaje de nacimientos que representa esa cantidad por año. 

**Front end**
En el front end el gráfico es realizado con plotly.js para la pagina web. En el archivo extras_backend hay una funcion que realiza el grafico desde python. 

## Tecnologías utilizadas 
- Lenguaje: Python (pandas para el procesamiento de datos)
- Backend: FASTAPI y Uvicorn
- Base de datos: MYSQL
- Frontend: HTML5, CSS3, JavaScript (Plotly.js para graficos interactivos)
- Infraestructura: Google Cloud Plataform (Cloud Run, Cloud SQL y Firebase Hosting)
- Contendores: Docker

## Estructura de los archivos 
├── backend/
│   ├── dockerfile          # Configuración del contenedor
│   ├── funciones.py        # Lógica de conexión y consultas
│   ├── main.py             # Endpoints de FastAPI
│   └── requirements.txt    # Dependencias del backend
├── data/
│   ├── nacimientos_completos.csv
│   ├── nombres_argentina.csv
│   └── datos originales/   # Datasets crudos de fuentes oficiales
├── frontend/
│   ├── 404.html
│   ├── index.html
│   ├── scripts.js          # Lógica de consumo de API y Plotly
│   └── style.css
├── scripts/
│   ├── limpieza.py         # Procesamiento de CSVs originales
│   └── setup_db.py         # Creación de tablas y carga de datos
├── extras_backend.py       # Utilidades adicionales y testeo de gráficos
├── requirements.txt        # Dependencias generales del proyecto
└── .envexample             # Plantilla para variables de entorno


## Instalación y configuración
La explicación de la instalación es para poder utilizarlo localmente, no se detalla el despliegue en la web 

1. Clonar y prepara entorno
```bash
git clone https://github.com/tu-usuario/nombres-argentina.git
cd nombres-argentina
pip install -r requirements.txt
```
2. Descargar datasets
Descargar y guardar en la carpeta data/ los datos originales:
&#x09;nombres: 1922- 2015 https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas 
&#x09;nombres: 2012-2024 https://www.datos.gob.ar/dataset/renaper-nombres-propios-argentina
&#x09;nacimientos:  https://datos.salud.gob.ar/dataset/serie-historica-de-nacimientos-ocurridos-en-argentina-por-jurisdiccion/archivo/95cfbd36-d912-46a4-9dfa-213e4bdbdc53
3. Variables de entorno
Crear un archivo .env basado en .envexample con credenciales de MYSQL
4. Incialización
```bash
python scripts/limpieza.py
python scripts/setup_db.py
```
5. Ejectura la API
```bash
cd backend
uvicorn main:app --reload
```
La API estara dispobible en http://localhost:8000 se puede consultar abriendo index.html del frontend 
