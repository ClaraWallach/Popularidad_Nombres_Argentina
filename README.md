Popularidad de nombres en Argentina (1922-2025)



En este proyecto se puede ver la popularidad de un nombre en Argentina entre 1922 y 1925. Para hacerlo utilice datasets de datos.gob.ar  Los datos fueron procesados, limpiados y almacenados en una base de datos MySQL que es consultada a través de una API.



Para realizar la app use dos datasets con la información sobre los nombres; uno con datos entre 1922 y 2015 y otro con datos entre 2012 y 2024. Los archivos tienen algunas diferencias ya que el primero tiene los nombres cargados de forma completa (“Juan Martin”) y el segundo de manera individual (“Juan”, “Martin”). Por lo tanto dividí los nombres del primer conjunto de datos para que las búsquedas sean siempre por el nombre individual. Luego tuve que limpiar errores en la codificación de algunas letras, nombres repetidos o distintas inconsistencias.



Para realizar el gráfico utilice un dataset con la cantidad de nacimientos en argentina por año. De esta manera se puede calcular el porcentaje de nacidos por año con un determinado nombre y saber cual es la popularidad real ya que hay mucha diferencia entre la cantidad de nacimientos hoy y hace cincuenta años lo que genera ´problemas´ sí miramos las cantidades.


El gráfico es realizado con plotly.js para la pagina web aunque en el archivo funciones.py hay una función que lo realiza desde Python.


**Tecnologías utilizadas:** Python, MySQL, Fast Api, Plotly, Pandas


**Instalación y configuración:**


Clonar el repositorio



&#x09;git clone https://github.com/tu-usuario/nombres-argentina.git 

&#x09;cd nombres-argentina


Instalar dependencias (requirements.txt)



&#x09;pip install -r requirements.txt




En la carpeta data descargar los datasets: 



&#x09;nombres 1922- 2015 https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas 

&#x09;nombres 2012-2024 https://www.datos.gob.ar/dataset/renaper-nombres-propios-argentina
	nacimientos:  https://datos.salud.gob.ar/dataset/serie-historica-de-nacimientos-ocurridos-en-argentina-por-jurisdiccion/archivo/95cfbd36-d912-46a4-9dfa-213e4bdbdc53



Crear archivo .env con tus credenciales


Ejecutar archivo scripts/limpieza.py



&#x09;python data/limpieza.py


Ejecutar archivo scripts/setup\_db.py



&#x09;python data/setup\_db.py


Ejecutar la api que se encuentra en la carpeta backend



&#x09;uvicorn backend.main:app --reload


Realizar las consultas desde el front end

