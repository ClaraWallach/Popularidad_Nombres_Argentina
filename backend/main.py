import funciones

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
from decouple import config
# %%
app = FastAPI()

# Definimos quién tiene permiso para entrar (en este caso defino todos)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"], 
    allow_headers=["*"], # Permite todos los encabezados
)


# %%
def conexion():
    try:
    #Obtenemos los valores de las variables de entorno
        db_host = config("mysql_host")
        db_user = config("mysql_user")
        db_pass = config("mysql_password")
        db_name = config("mysql_database")
        db_port = config("mysql_port", default="3306")

    #Preparamos la configuración base (igual para local y web)
        conf = {
            "user": db_user,
            "password": db_pass,
            "database": db_name
        }
    #Si el host empieza con /cloudsql/ lo estoy desplegando entonces necesito usar unix_socket
        if "/cloudsql/" in db_host:
            socket_path = db_host 
            conf["unix_socket"] = socket_path


    #Para conectar con la bd de manera local 
        else: 
            #agrego al diccionario host y port que solo hay que mandar si se esta usando local
            conf["host"] = db_host
            conf["port"] = db_port


        #Conectamos usando el diccionario desempaquetado
        connection = mysql.connector.connect(**conf)
        return connection

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
# %%
@app.get("/nombre/{busqueda}")

async def nombre(busqueda: str):
    try:
        con= conexion()
        if con is None:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        #Crear cursor (objeto mysql cursor) que es el objeto a traves del cual se realizan las consultas
        cursor = con.cursor(dictionary = True)
        datos = funciones.datos(busqueda, cursor)
    
        return datos
    
    finally:
        cursor.close()
        con.close()
  
