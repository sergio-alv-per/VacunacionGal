import urllib.parse as up
import psycopg2
import secretos


# Funciones que gestionan la interacción del programa con la base de datos.

conexion = None

def generar_BD():
    """Genera una conexión a una base de datos PostgreSQL externa dada por su URL"""
    global conexion
    up.uses_netloc.append("postgres")
    url = up.urlparse(secretos.bdd_url())

    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port )

    conn.set_session(autocommit=True)

    conexion = conn

def cerrar_BD():
    """Cierra la conexión a la base de datos"""
    conexion.close()

def extraer_datos(fecha):
    """Dada una fecha en formato string obtiene los datos almacenados en la base de datos
       asociados. A continuación los introduce en un diccionario y los devuelve.
    """
    cur = conexion.cursor()
    cur.execute("SELECT * FROM datos_vacunacion WHERE fecha=%s", (fecha,))
    res = [col for col in cur.fetchall()[0]]
    cur.close()
    return {"fecha": str(res[0]), "1d": res[1], "pc": res[2], "dif1d": res[3], "difpc": res[4]}

def extraer_valor(clave):
    """Extrae el valor de una clave. El valor es booleano."""
    cur = conexion.cursor()
    cur.execute("SELECT valor FROM pares WHERE clave=%s", (clave,))
    res = cur.fetchone()[0]
    cur.close()
    return res

def existen_datos_fecha(fecha):
    """Devuelve un valor booleano.
       Verdadero si existe una fila en la tabla datos_vacunacion asociada a la fecha proporcionada.
    """
    cur = conexion.cursor()
    cur.execute("SELECT fecha FROM datos_vacunacion WHERE fecha = %s", (fecha,))
    numfilas = cur.rowcount
    cur.close()
    return numfilas > 0

def insertar_datos(fecha, datos):
    """Inserta los datos dados asociados a la fecha proporcionada en la base de datos.
       Los datos deben ser un diccionario con claves "1d", "pc", "dif1d", "difpc".
       """
    cur = conexion.cursor()
    datos["fecha"] = fecha
    cur.execute("INSERT INTO datos_vacunacion VALUES (%(fecha)s, %(1d)s, %(pc)s, %(dif1d)s, %(difpc)s)", datos)
    cur.close()

def actualizar_valor(clave, valor):
    """Actualiza el valor de la clave dada, asignándole el valor proporcionado (booleano)"""
    cur = conexion.cursor()
    cur.execute("UPDATE pares SET valor=%s WHERE  clave=%s", (valor, clave))
    cur.close()

def listado_fechas():
    """Devuelve un listado de todas las fechas de las que se tienen datos en la base de datos"""
    cur = conexion.cursor()
    cur.execute("SELECT fecha FROM datos_vacunacion")
    res = [str(v[0]) for v in cur.fetchall()]
    cur.close()
    return res
