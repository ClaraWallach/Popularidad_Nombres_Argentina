from decouple import config
import plotly.express as px
import pandas as pd 
import mysql.connector


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



#Crea un archivo html con el grafico de la popularidad de un nombre
#No es usada en la api porque creo el grafico desde el front end pero la dejo por si se quiere usar desde python
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