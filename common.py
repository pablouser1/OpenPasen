#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import requests
import api
import os
from pathlib import Path
def init():
    # Variables globales, se usarán a lo largo de todo el programa
    global jar
    jar = requests.cookies.RequestsCookieJar()
    global config
    config = configparser.ConfigParser()
    # TODO incluir Mac (darwin)
    global config_path
    if os.name in "posix":
        config_path = str(Path.home()) + "/.config/openpasen/" # Localización en linux
    
    elif os.name in "nt":
        config_path = str(Path.home()) + "/AppData/Roaming/OpenPasen/" # Localización en Windows

def getsession():
    try:
        os.mkdir(config_path)
        print("Configuración no encontrada, creando...")
    except FileExistsError:
        print("Configuración encontrada")
    config.read(config_path + "config.ini")
    try:
        config.items('Login')
        jar.set('SenecaP', config['Cookies']['SenecaP'], domain='seneca.juntadeandalucia.es', path='/')
        jar.set('JSESSIONID', config['Cookies']['JSESSIONID'], domain='seneca.juntadeandalucia.es', path='/')
        return "main_menu"
    except configparser.NoSectionError:
        return "login_menu"

def getconfig():
    print("Accedido a la config")
    return config

def getjar():
    print("Accedido al Jar")
    return jar
