import gestion_datos
import twitter
import basedatos
import traceback

# Ejecución principla del programa

basedatos.generar_BD()

try:
    if not gestion_datos.hay_datos_hoy():
        print("Obteniendo informe...")
        dir_informes = "informes"
        informe = gestion_datos.descargar_informe(dir_informes)
    else:
        print("Ya hay datos de hoy")

    if gestion_datos.hay_informe_no_leido():
        print("Informe no leido, generando datos...")
        datos_hoy = gestion_datos.generar_datos(informe)
        gestion_datos.almacenar_datos(datos_hoy)
    else:
        print("Informe ya leido.")

    if gestion_datos.hay_informe_no_twiteado():
        print("Informe no tweeteado, generando tweet...")
        API = twitter.generar_api()
        tweet = twitter.generar_tweet()
        twitter.twitear(API, tweet)
    else:
        print("Informe ya tweeteado.")

    basedatos.cerrar_BD()
    print("Programa cerrado correctamente")
except Exception as e:
    traceback.print_exc()
    print("Programa cerrado inesperadamente.")
    basedatos.cerrar_BD()
    exit(1)
