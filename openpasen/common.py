#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import requests
from openpasen import api
from os import mkdir as mkdir
import platform
from pathlib import Path
def init():
    # Variables globales, se usarán a lo largo de todo el programa
    global jar
    jar = requests.cookies.RequestsCookieJar()
    global config
    config = configparser.ConfigParser()
    homepath = str(Path.home())
    global config_path
    if platform.system() in "Linux":
        config_path = homepath + "/.config/openpasen/" # Localización en linux
    
    elif platform.system() in "Windows":
        config_path = homepath + "/AppData/Roaming/OpenPasen/" # Localización en Windows
    
    elif platform.system() in "Darwin":
        config_path = homepath + "/Library/OpenPasen" # Localización en Mac

def getsession():
    try:
        mkdir(config_path)
        print("Config no encontrada, creando...")
    except FileExistsError:
        print("Config encontrada")
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
