import pandas as pd
# %%
## 1) CARGAR DATOS Y CREAR TABLA CON TODOS LOS AÑOS ###

#Link de los datos: 
# 1922-2015 : https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas
#2012 - 2024: https://www.datos.gob.ar/dataset/renaper-nombres-propios-argentina

# %%
n1= pd.read_csv("../data/datos originales/historico-nombres.csv") #1922-2015 

n2= pd.read_csv("../data/datos originales/nombres_propios_provincia_anio_2012_2024.csv") #2012-2024
# %%
n2 = n2.drop(["provincia_id", "nombre_provincia"], axis = 1)
# %%
n1=n1.dropna(axis=0)
n2= n2.dropna(axis=0)

# %%
n1= n1[n1["anio"]<2012]
# %%
#Junto las dos tablas en una única tabla 
nombres= pd.concat([n1,n2])
# %%

anios = nombres["anio"].unique()

# %%
### 2)LIMPIEZA DE LA TABLA ###
# %%
def reemplazos(nombre):
    #pasar todo a mayuscula y eliminar espacios al principio y final 
    nombre = nombre.upper().strip() 
    
    #reemplazar acentos y marcas conocidas
    reemplazos = {
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
        "À": "A", "È": "E", "Ì": "I", "Ò": "O", "Ù": "U",
        "Ü": "U", "Ï": "I", 
        ".": "", ",": "", #elimino puntos y comas
        #reemplazos de codificación CP850 (DOS)
        "\xa0": " ", "\x82": "E", "\xa4": "Ñ","\xa1": "I",
        "\xa2": "O", "\xa3": "U", "\x90": "E", "\xad": ""
        
    }
    for o, r in reemplazos.items():
        nombre = nombre.replace(o, r)

    return nombre 
# %%
nombres["nombre"]= nombres["nombre"].apply(reemplazos)
# %%
#eliminar las expresiones dentro de parantesis 
nombres["nombre"] = nombres["nombre"].str.replace("\\((.*?)\\)", " ", regex= True)

# %%
#eliminar los espacios alrededor de ' y - que despues separan nombres en lugares incorrectos 
nombres["nombre"] = nombres["nombre"].str.replace(r"\s*'\s*", "'", regex=True)
nombres["nombre"] = nombres["nombre"].str.replace(r"\s*-\s*", "'", regex=True)
# %%
#eliminar las nombres que tienen expresiones que NO son letras, espacios, guion o apostrofe (~ ^ doble negacion)
nombres= nombres[~nombres["nombre"].str.contains(r"[^A-ZÑ\s'\-]",na=False, regex=True)]

# %%
#eliminar filas unicamente con espacios
nombres= nombres[nombres["nombre"] != ""]
#eliminar espacios adelante y atras que hayan quedado despues de las transformaciones
nombres["nombre"] = nombres["nombre"].str.strip()
# %%
#eliminar filas con espacios vacios 
nombres.dropna(inplace = True)
# %%

### 3) DESCOMPONER LOS NOMBRES ###

#crear la columna lista nombres en la que se guarda una lista con cada palabra que conforma el nombre
nombres["lista_nombres"] = nombres["nombre"].str.split()

# %%
#eliminar la columna nombre que guarda el nombre compuesto
nombres.drop("nombre", axis=1, inplace=True)
# %%
#explode crea una fila para cada elemento de lista nombres. 
nombres_descompuestos = nombres.explode("lista_nombres")
# %%
nombres_descompuestos.rename(columns={"lista_nombres": "nombre"}, inplace= True)                                
# %%
nombres_descompuestos.reset_index(inplace= True)
# %%
#Crear tabla agrupando los que tengan igual nombre, posicion y anio. Sumo en cantidad 
nombres_argentina= nombres_descompuestos.groupby(["nombre","anio"])["cantidad"].sum().reset_index()

# %%
#eliminar filas unicamente con espacios
nombres_argentina= nombres_argentina[nombres_argentina["nombre"] != ""]
#eliminar espacios adelante y atras que hayan quedado despues de las transformaciones
nombres_argentina["nombre"] = nombres_argentina["nombre"].str.strip()
#eliminar filas con espacios vacios 
nombres_argentina.dropna(inplace = True)
# %%
nombres_argentina.to_csv("../data/nombres_argentina.csv", index=False)
# %%

# %%

### TABLA DE NACIMIENTOS POR AÑO ###
#datos de https://datos.salud.gob.ar/dataset/serie-historica-de-nacimientos-ocurridos-en-argentina-por-jurisdiccion/archivo/95cfbd36-d912-46a4-9dfa-213e4bdbdc53


nacimientos = pd.read_csv("datos originales/nacidos-vivos-jurisdiccion-2022-1914.csv")
# %%

nacimientos = nacimientos[["indice_tiempo", "total_argentina"]]
# %%

nacimientos.rename(columns={"indice_tiempo":"anio", "total_argentina": "cant_nacimientos"}, inplace = True)
# %%
#elimino dia y mes de la fecha 
nacimientos["anio"] = nacimientos["anio"].str[0:4]
# %%

nacimientos["anio"] = nacimientos["anio"].astype(int)

# %%
#selecciono los datos que tengo la tabla de nombres 
nacimientos = nacimientos[nacimientos["anio"] >= 1922]

# %%
vacios = nacimientos[nacimientos["cant_nacimientos"] == 0]
# %%
#eliminar filas con cantidad vacia que despues voy a agregar con los valores reales
nacimientos = nacimientos[nacimientos["cant_nacimientos"] != 0]
# %%
#info de datosmacro.com e indec
faltantes = [(1971, 564000), (1972, 557000), (1973, 583000), (1974, 604000), (2023, 485000), (2024, 470000)]

agregar = {"anio": [], "cant_nacimientos": []}

for i in faltantes:
    agregar["anio"].append(i[0])
    agregar["cant_nacimientos"].append(i[1])

# %%
anios_faltantes = pd.DataFrame(agregar)
# %%
nacimientos_completo = pd.concat([nacimientos, anios_faltantes], axis= 0, ignore_index=True).sort_values(by="anio")
# %%
nacimientos_completo.to_csv("../data/nacimientos_completos.csv", index=False)



