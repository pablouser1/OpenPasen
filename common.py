#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import requests
import api
def init():
    global jar
    jar = requests.cookies.RequestsCookieJar()
    global config
    config = configparser.ConfigParser()

def getsession():
    config.read('data/config.ini')
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