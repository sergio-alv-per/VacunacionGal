import tweepy
import secretos
from gestion_datos import fecha_mas_reciente, marcar_informe_twiteado
from basedatos import extraer_datos

# Funciones que gestionan la interacción del programa con la API de twitter.

def generar_api():
    """Genera un objeto API de twitter con las claves secretas almacenadas"""
    CONSUMER_KEY = secretos.cons_key_twitter()
    CONSUMER_SECRET = secretos.cons_secret_twitter()
    KEY = secretos.api_key_twitter()
    SECRET = secretos.api_secret_twitter()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(KEY, SECRET)
    return tweepy.API(auth)


def generar_tweet():
    """Genera el string del tweet a publicar conteniendo los datos más recientes almacenados en la base de datos"""
    datos_recientes = extraer_datos(fecha_mas_reciente())
    formato_tweet = """El {completa:.2f}% (+{difcompleta:.2f}%) de la población gallega mayor de 12 años ha recibido la vacunación completa contra el COVID-19. El {monodosis:.2f}% (+{difmonodosis:.2f}%) ha recibido al menos una dosis de la vacuna.
  """

    return formato_tweet.format(completa=datos_recientes["pc"] * 100,
                                difcompleta=datos_recientes["difpc"] * 100,
                                monodosis=datos_recientes["1d"] * 100,
                                difmonodosis=datos_recientes["dif1d"] * 100)


def twitear(api, tweet):
    """Utiliza la api proporcionada para publicar el tweet dado como string"""
    api.update_status(tweet)
    marcar_informe_twiteado()
