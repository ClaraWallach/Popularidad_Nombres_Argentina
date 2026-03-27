import plotly.express as px
import pandas as pd
from decouple import config
import mysql.connector

# %%
def buscar_nombre(nombre:str, cursor):
    
    anios = list(range(1922, 2025))
    molde = {anio:[0, 0] for anio in anios}

    query = """
         SELECT nombres.anio, nombres.cantidad, (nombres.cantidad * 100/total_nacimientos.cant_nacimientos) AS porcentaje
         FROM nombres
         INNER JOIN total_nacimientos ON nombres.anio = total_nacimientos.anio
         WHERE nombre = %s
         
     """
    # %s se utiliza dentro de la consulta para pasarle una variable (nombre)
    # ejecutamos la consulta notar que hay que pasar la query como primer argumento y las variables en el segundo
    # si tengo mas de una variable (%s) hay que pasarlas en orden
    # las variables hay que pasarlas como tuplas por eso (n,) al ser una tupla de un solo elemento hay que agregar la , al final para que se interprete como tal 
    
    cursor.execute(query, (nombre,))
    
    
    #lee los datos y los devuelve en una lista de tuplas
    result = cursor.fetchall()
  
    for i in range(len(result)):
        molde[result[i]["anio"]] = [result[i]["cantidad"],result[i]["porcentaje"]]

    
    #creo el diccionario res donde guardo todos los valores listos para convertir en df
    res = {"anio": [], "cantidad": [], "porcentaje": []}
    molde = list(molde.items())
    for i in range(len(molde)):
        res["anio"].append(int(molde[i][0]))
        res["cantidad"].append(int(molde[i][1][0]))
        res["porcentaje"].append(float(molde[i][1][1]))
    
    return res

# %%

def graficar_popularidad(dict_nombre:dict, nombre:str):
    df_nombre = pd.DataFrame(dict_nombre).sort_values(by="anio")
    fig = px.bar(
        df_nombre,
        x="anio", y="porcentaje",
        title = f"Popularidad del nombre {nombre}",
        hover_data = {"cantidad": True}, #se guarda en la lista customdata a la que despues puedo acceder
        labels={'anio': 'Año', 'cantidad': 'Cantidad exacta de nacimientos', 'porcentaje': 'Porcentaje de nacimientos'},
        )

    #agregar etiquetas en el eje x cada cinco años y mostrar grilla
    fig.update_xaxes(
        tickmode = 'linear',
        tick0 = 1925,      
        dtick = 5,
        tickangle = -45, 
        showgrid=True, 
        gridwidth=1, 
        minor=dict(ticklen=4, dtick=1, showgrid=True, gridcolor='GhostWhite')
    )
    
    #para que al pasar el mouse sobre cualquier altura del grafico muestre la info (mas facil ver data de años con porcentaje muy bajo)
    fig.update_layout(
        hovermode='x', 
        hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial"
        )
    )
    
    fig.update_traces(
       hovertemplate=(
           "<b>" + nombre + " en " + "%{x}</b><br>" +
           "<b>%{customdata[0]:,d}</b> nacidos con este nombre<br>" +
           "%{y:.4f}% del total del año"   #{y:.4f} muestra eje y (porcentaje) con cuatro decimales 
       )
    )

    fig.write_html("popularidad_nombre.html")  
    print("grafico hecho")
# %%

def normalizar(nombre:str):
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
#Devuelve un diccionario {cantidad, anio}
def datos(nombre, cursor): 
    busqueda = normalizar(nombre)
    dict_busqueda= buscar_nombre(busqueda, cursor)
    return dict_busqueda


# %%

# %%
#Crea un archivo html con el grafico de la popularidad de un nombre
#No es usada en la api porque creo el grafico desde el front end
def grafico(nombre:str): 
    cursor = conection.cursor(dictionary = True)
    busqueda = normalizar(nombre)
    dict_busqueda= buscar_nombre(busqueda, cursor)
    graficar_popularidad(dict_busqueda, busqueda)
    cursor.close()
# %%

#Para usar la funcion grafico desde este archivo hay que cargar la conexion con la base de datos
conf = {
    "host": config("mysql_host"),
     "port": config("mysql_port"),
     "database": config("mysql_database"),
     "user": config("mysql_user"),
     "password": config("mysql_password")}
    
conection = mysql.connector.connect(**conf)
# %%
cursor = conection.cursor(dictionary = True)
#Llamar a la funcion

#Cerrar el conector
cursor.close()
