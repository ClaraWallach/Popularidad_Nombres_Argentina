from backend import funciones

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
    allow_methods=["*"], # Permite GET, POST, etc.
    allow_headers=["*"], # Permite todos los encabezados
)


# %%
def conexion():
    try:
        conf = {
            "host": config("mysql_host"),
            "port": config("mysql_port"),
            "database": config("mysql_database"),
            "user": config("mysql_user"),
            "password": config("mysql_password")}
    
        conection = mysql.connector.connect(**conf)
        return conection 
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
  


