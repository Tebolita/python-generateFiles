#Importo pandas para manipular los datos de una tabla 
import os 
import pandas as pd

#Lee los datos de un archivo dependiendo del formato
df = pd.read_csv("data_ids.csv")
#Filtro los datos por el id
data = df["id"]
#Hago una operacion para saber que cuantos elementos hay dentro y divir su contenido a la mitad
div = int(len(data) / 2)
#Selecciono todos los datos de la lista desde 0 hasta el resultado de div
df1 = data[0:div]
#Hago los mismo que antes pero ahora desde el resultado de div hasta el total de elementos que tiene la variable data
df2 = data[div:len(data)]

# Generar los archivos en formato csv
# df1.to_csv("PrimeraParte.csv", index=False)
# df2.to_csv("SegundaParte.csv", index=False)

########################################### SE CREA EL PRIMER ARHIVO SQL #################################################
#Se crea un archivo llamado primera.sql por si no hay uno y luego lo abro con la propiedad W para escribir 
fileWSql = open("./Primera.sql", "w")

#Escribo en el archivo
# fileWSql.write("""CREATE TABLE inventario(
# id INT NOT NULL,
# estado VARCHAR(100) NOT NULL
# )
# """)

#Cierro el archivo por seguridad
fileWSql.close()
#Abro el archivo para agregar al final de la siguente linea nuevo texto
fileASql = open("./Primera.sql", "a")

#Recoro la primera mitad de los datos y los voy escribiendo uno a uno en el archivo
for i in df1:
    fileASql.write("UPDATE inventario set estado = 'False' WHERE id = {a} \n".format(a=i))

########################################### SE CREA EL SEGUNDO ARHIVO SQL #################################################

fileWSql = open("./Sengudo.sql", "w")
#Escribo en el archivo
# fileWSql.write("""CREATE TABLE inventario(
# id INT NOT NULL,
# estado VARCHAR(100) NOT NULL
# )
# """)
#Cierro el archio por seguridad
fileWSql.close()
#Abro el archivo pero con la propiedad A para agregar al final de la siguente linea de texto
fileASql = open("./Sengudo.sql", "a")

#Recoro la primera mitad de los datos y los voy escribiendo uno a uno en el archivo
for i in df2:
    fileASql.write("UPDATE inventario set estado = 'False' WHERE id = {a} \n".format(a=i))



#Crear un lote pro cada 100 ids
directorio = "Lotes"

#Comprobar si ya existe la carpeta para evitar errores
if not os.path.isdir(directorio):
    os.mkdir(directorio)

# creo un indice para saber cuando llegue a un lote 
index = 0
# Creo un indice del nombre para saber que numero de lote se crea
IndexNombre = 0
# Recoro todos los ids
for i in data:
    # sumo +1 al index para ir controlando los lotes
    index += 1
    # cada vez que se inicie el index en 1 
    if index == 1:
        # Sumo 1 para diferenciar a los lotes
        IndexNombre += 1
        # Creo un archivo con el nombre lote y el numero
        fileWSql = open("./Lotes/Lote{a}.sql".format(a=IndexNombre), "w")
        fileWSql.write("UPDATE inventario set estado = 'False' where id in (")
    # si se cumple se escribe el id en el archivo
    if index < 100:
        fileWSql.write("{a},\n".format(a=i))
        
    # si index llega a 100 significa que ya tengo un lote por ello reinicio index para crear otro lote         
    if index == 100:
        # Termino la ultima linea agregando el ultimo id pero sin la , para evitar errores de syntaxis 
        fileWSql.write("{a}".format(a=i))
        fileWSql.write(")")
        index = 0
        fileWSql.close()