import pandas as pd
from datetime import datetime
import requests
import os.path
import pytz
import basedatos

# Funciones que gestionan la obtención y procesamiento de los datos
# desde la página web del Ministerio de Sanidad.

def intentar_descarga(link):
    """Intenta descargar un archivo desde el link proporcionado."""

    r = requests.get(link)

    if r.ok:
        return r
    else:
        raise Exception("Error en la descarga de " + link)



def descargar_informe(dir_informe):
    """Descarga el informe de hoy desde la página web del Ministerio de Sanidad.
       Si el informe ya ha sido descargado, no lo vuelve a descargar.
       Marca el informe como no leido y no twiteado en la base de datos.
       Devuelve la ruta del fichero descargado.
    """

    fecha_link = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y%m%d")

    nombre_informe = "Informe_Comunicacion_" + fecha_link + ".ods"
    link_mcscbs = "https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/" + nombre_informe

    fichero_informe = nombre_informe

    if (not os.path.exists(fichero_informe)):
        r = intentar_descarga(link_mcscbs)
        with open(fichero_informe, "wb") as f:
            f.write(r.content)
        marcar_informe_no_leido()
        marcar_informe_no_twiteado()

    return fichero_informe


def cargar_fichero(fichero_informe):
    """Carga el fichero ods descargado de la página web del Ministerio de Sanidad.
       Devuelve dos dataframes, asociados a cada una de las hojas relevantes del documento"""

    df_1_dosis = pd.DataFrame()
    df_pauta_completa = pd.DataFrame()

    hoja_1_dosis = "Etarios_con_al_menos_1_dosis"
    hoja_pauta_completa = "Etarios_con_pauta_completa"

    df_1_dosis = pd.read_excel(fichero_informe, hoja_1_dosis, engine="odf")
    df_pauta_completa = pd.read_excel(fichero_informe, hoja_pauta_completa, engine="odf")

    return (df_1_dosis, df_pauta_completa)


def fecha_mas_reciente():
    """"Devuelve la fecha más reciente entre aquellas que tienen datos asociados en la base de datos"""
    return max(basedatos.listado_fechas())


def obtener_diferencias_dia_previo(hoy_1d, hoy_pc):
    """Calcula el incremento en porcentaje de vacuandos respecto a los datos del día anterior"""
    dif_1d = 0.0
    dif_pc = 0.0
    if (basedatos.listado_fechas()):
        datos_previos = basedatos.extraer_datos(fecha_mas_reciente())

        dif_1d = hoy_1d - datos_previos["1d"]
        dif_pc = hoy_pc - datos_previos["pc"]

        if dif_1d < 0 or dif_pc < 0:
            raise Exception("Error en el cálculo de la diferencia con el día previo: resultado negativo")

        if dif_1d > 10 or dif_pc > 10:
            raise Exception("Error en el cálculo de la diferencia con el día previo: resultado demasiado grande")

    return (dif_1d, dif_pc)


def generar_datos(fichero_informe):
    """Genera un diccionario con los datos sobre vacunación necesarios asociados a la fecha actual.
       Los campos del diccionario serán "1d", "pc", "dif1d", "difpc".
    """
    (df_1_dosis, df_pauta_completa) = cargar_fichero(fichero_informe)

    df_1_dosis = df_1_dosis.set_index("Unnamed: 0")
    df_pauta_completa = df_pauta_completa.set_index("Unnamed: 0")

    galicia_1_dosis = df_1_dosis.loc[
        "Galicia", "% Con al menos 1 dosis sobre Población a Vacunar INE"]
    galicia_pauta_completa = df_pauta_completa.loc[
        "Galicia", "% pauta completa sobre Población a Vacunar INE"]

    (dif_1d, dif_pc) = obtener_diferencias_dia_previo(galicia_1_dosis,
                                                      galicia_pauta_completa)
    return {
        "1d": galicia_1_dosis,
        "pc": galicia_pauta_completa,
        "dif1d": dif_1d,
        "difpc": dif_pc
    }


def almacenar_datos(datos):
    """Almacena los datos generados asociados a la fecha actual en la base de datos"""
    fecha_iso = datetime.now(
        pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d")
    basedatos.insertar_datos(fecha_iso, datos)
    marcar_informe_leido()


def marcar_informe_no_leido():
    """Marca que existe un informe no leido, es decir, un archivo informe que no se ha procesado y almacenado en la base de datos"""
    basedatos.actualizar_valor("informe_no_leido", True)


def marcar_informe_leido():
    """Marca que el último informe descargado ya se ha procesado y almacenado en la base de datos"""
    basedatos.actualizar_valor("informe_no_leido", False)


def hay_informe_no_leido():
    """Devuelve True si existe un informe descargado que no se ha procesado"""
    return basedatos.extraer_valor("informe_no_leido")


def marcar_informe_no_twiteado():
    """Marca que existe un informe no twiteado, es decir, unos datos de los cuales no se ha publicado un tweet"""
    basedatos.actualizar_valor("informe_no_twiteado", True)


def marcar_informe_twiteado():
    """Marca que el último informe descargado ya tiene su tweet asociado"""
    basedatos.actualizar_valor("informe_no_twiteado", False)


def hay_informe_no_twiteado():
    """Devuelve True si existe un informe descargado sobre el que no se ha escrito un tweet"""
    return basedatos.extraer_valor("informe_no_twiteado")

def hay_datos_hoy():
    """Devuelve True si existen datos asociados a la fecha de hoy en la base de datos"""
    fecha_iso = datetime.now(
        pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d")
    return basedatos.existen_datos_fecha(fecha_iso)
