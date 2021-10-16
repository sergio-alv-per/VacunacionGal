import os

# Funciones que gestionan el acceso del programa a variables secretas como 
# la URL de la base de datos y las claves de la API de Twitter.

def bdd_url():
    return os.environ['BDD_URL']

def cons_key_twitter():
    return os.environ['CONSUMER_KEY']

def cons_secret_twitter():
    return os.environ['CONSUMER_SECRET']

def api_key_twitter():
    return os.environ['KEY']

def api_secret_twitter():
    return os.environ['SECRET']
