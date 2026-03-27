import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from decouple import config
# %%
USER = config("mysql_user")
PASSWORD = config("mysql_password")
HOST = config("mysql_host")
PORT = config("mysql_port")
DATABASE = config("nombres_argentina")

# %%
#Conexion con mysql
db = mysql.connector.connect(
  host= HOST,
  user= USER,
  password= PASSWORD,
  port= PORT
)

#Crear objeto cursor
cursor = db.cursor()


#Crear base de datos
cursor.execute("CREATE DATABASE IF NOT EXISTS nombres_argentina")

print("base de datos creada")

cursor.close()
db.close()
# %%

db = mysql.connector.connect(
  host= HOST,
  user= USER,
  password= PASSWORD,
  port= PORT,
  database = "nombres_argentina"
)

#Crear tablas
tabla_nombres = """ CREATE TABLE `nombres_argentina`.`nombres` (
                    `anio` INT NOT NULL,
                    `nombre` VARCHAR(100) NOT NULL,
                    `cantidad` INT NOT NULL,
                    PRIMARY KEY (`anio`, `nombre`))
                    ENGINE = InnoDB
                    DEFAULT CHARACTER SET = utf8mb4
                    COLLATE = utf8mb4_spanish_ci;"""
                    
tabla_nacimientos = """ CREATE TABLE `nombres_argentina`.`total_nacimientos` (
                        `anio` INT NOT NULL,
                        `cant_nacimientos` INT NOT NULL,
                        PRIMARY KEY (`anio`))"""
# %%
cursor = db.cursor()
# %%
cursor.execute(tabla_nombres)
print("tabla nombres creada en base de datos")
# %%
cursor.execute(tabla_nacimientos)
print("tabla nacimientos creada en base de datos")
# %%
cursor.close()
# %%
#Cargar datos en las tablas (voy a usar sqlAlchemy para esto)
url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(USER, PASSWORD, HOST, PORT, DATABASE)
engine = create_engine(url)
# %%
#Cargar datos en nombres
nombres = pd.read_csv("../data/nombres_argentina.csv", keep_default_na=False, na_values = [""]) 
# %%
#Agrego keep_default_na = False para que no asuma el nombre NA (nombre oriental) como nulo 
nombres.to_sql('nombres', con=engine, if_exists='append', index=False)
print("¡Datos nombres cargados con éxito!")

# %%
#Cargar datos en nacimientos
nacimientos = pd.read_csv("../data/nacimientos_completos.csv")

nacimientos.to_sql('total_nacimientos', con=engine, if_exists='append', index=False)
print("¡Datos nacimientos cargados con éxito!")

# %%
#Eliminar manualmente algunos datos erroneos

def eliminar(nombre):
    cursor = db.cursor()
    query="""DELETE FROM nombres_argentina.nombres
             WHERE nombre = %s"""
    cursor.execute(query, (nombre,))
    db.commit()
    cursor.close()
    print("nombre eliminado")
# %%
eliminar("NOMBRE")
# %%
eliminar("UNICO")
# %%
if db.is_connected():
    cursor.close()
    db.close()
    print("Conexión MySQL cerrada")
