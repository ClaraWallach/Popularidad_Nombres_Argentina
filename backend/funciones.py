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
