#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common
import requests
import os
import shutil

def init():
    global jar
    jar = common.getjar()
    global config
    config = common.getconfig()
    print("Api init")

#Facilita las requests
def req(method, url, body = "null"):
    try:
        if (method == "GET"):
            if (body == "null"):
                data = requests.get(url, headers=headers, cookies=jar, timeout=3)
            else:
                data = requests.get(url, headers=headers, cookies=jar, data=body, timeout=3)
        if (method == "POST"):
            if (body == "null"):
                data = requests.post(url, headers=headerspost, cookies=jar, timeout=3)
            else:
                data = requests.post(url, headers=headerspost, cookies=jar, data=body, timeout=3)
        return data
    
    # Timeout
    except requests.exceptions.RequestException:
        print("Error de conexión")
        quit(1)

# Initial variables
headers = {
    "Content-Type": "application/json; charset=UTF-8"
}

headerspost = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

base_url = "https://seneca.juntadeandalucia.es/seneca/jsp/pasendroid/" # Este es el comienzo de todas las URLs de PASEN

def login(logininfo):
    # (logininfo): 0 = Username | 1 = Password | 2 = Remember me

    body = 'USUARIO=' + logininfo[0] + '&CLAVE=' + logininfo[1] + '&p={"version":"11.10.0"}'
    login = requests.post(base_url + "login", headers=headerspost, data=body)
    # Comprobando si se ha iniciado sesión correctamente
    if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
        print("Error al iniciar sesión")
        quit(1)

    jar.set('SenecaP', login.cookies['SenecaP'], domain='seneca.juntadeandalucia.es', path='/')
    jar.set('JSESSIONID', login.cookies['JSESSIONID'], domain='seneca.juntadeandalucia.es', path='/')
    # Guardar configuración de inicio de sesión si se ha marcado el botón de mantener sesión iniciada
    if (logininfo[2] == "True"):
        print("Guardando información de inicio de sesión...")
        config['Cookies'] = {
            'SenecaP': login.cookies['SenecaP'],
            'JSESSIONID': login.cookies['JSESSIONID']}
        config['Login'] = {
            'Username': logininfo[0],
            'Password': logininfo[1]}
        config['Config'] = {
            'LoginRemember': "Y"}
    else:
        config['Config'] = {
            'LoginRemember': "N"}
    with open('data/config.ini', 'w') as configfile:
        config.write(configfile)

def checksession():
    try:
        req("GET", base_url + "infoSesion").json()['RESULTADO'][0]['USUARIO']
        print("Sesión ok")
    except KeyError:
        print("Las cookies han expirado, generando nuevas...")
        body = 'USUARIO=' + config['Login']['Username'] + '&CLAVE=' + config['Login']['Password'] + '&p={"version":"11.10.0"}'
        login = req("POST", base_url + "login", body)
        if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
            print("Error al iniciar sesión")
            quit(1)
        # Algo ha tenido que cambiar en los servidores de la Junta, de momento esto funciona
        try:
            jar.set('JSESSIONID', login.cookies['JSESSIONID'], domain='seneca.juntadeandalucia.es', path='/')
            config.set('Cookies', 'JSESSIONID', login.cookies['JSESSIONID'])
        except KeyError:
            print("JSESSIONID no recibido")

        try:
            jar.set('SenecaP', login.cookies['SenecaP'], domain='seneca.juntadeandalucia.es', path='/')
            config.set('Cookies', 'SenecaP', login.cookies['SenecaP'])
        except KeyError:
            print("SenecaP no recibido")
        with open('data/config.ini', 'w') as configfile:
            config.write(configfile)

def userinfo():
    main = req("GET", base_url + "infoSesion").json()
    global user
    user = {
        "nombre" : main['RESULTADO'][0]['USUARIO'],
        "curso" : main['RESULTADO'][0]['MATRICULAS'][0]['CURSO'],
        "unidad" : main['RESULTADO'][0]['MATRICULAS'][0]['UNIDAD'],
        "denominacion" : main['RESULTADO'][0]['MATRICULAS'][0]['DENOMINACION'],
        "tutor" : main['RESULTADO'][0]['MATRICULAS'][0]['TUTOR'],
        "matricula" : main['RESULTADO'][0]['MATRICULAS'][0]['X_MATRICULA'],
        "centro" : main['RESULTADO'][0]['MATRICULAS'][0]['X_CENTRO'],
        }
    try:
        foto_local = open('data/imagen.png', 'rb')
        print("Imagen encontrada")
    except IOError:
        print("Foto no encontrada")
        # Si no existe lo descarga
        bodyfoto = "X_MATRICULA=" + user["matricula"]
        foto_req = requests.post(base_url + "imageAlumno", headers=headerspost, cookies=jar, data=bodyfoto, stream=True, timeout=3)
        # Guarda el archivo localmente
        foto_local = open('data/imagen.png', 'wb')
        foto_req.raw.decode_content = True
        shutil.copyfileobj(foto_req.raw, foto_local)
    
    user.update( {"foto" : foto_local} ) # Agregar foto al dict user
    return user

def convcentro(evaluacion):
    bodyconv = "X_MATRICULA=" + user["matricula"]
    convocatorias = req("POST", base_url + "getConvocatorias", bodyconv)
    cantidad_convocatorias = len(convocatorias.json()['RESULTADO'])
    for i in range(0, cantidad_convocatorias):
        if (convocatorias.json()['RESULTADO'][i]['D_CONVOCATORIA'] == evaluacion):
            user.update({"convcentro" : convocatorias.json()['RESULTADO'][i]['X_CONVCENTRO']})

def avisos():
    avisos = req("GET", base_url + "avisos")
    print(avisos.text)
    return avisos

def conductas():
    bodyconductas = "X_MATRICULA=" + user["matricula"]
    conductas = req("POST", base_url + "getConductasContrarias", bodyconductas)
    return conductas

def notas():
    bodynotas = "X_MATRICULA=" + user["matricula"] + "&X_CONVCENTRO=" + str(user["convcentro"])
    notas = req("POST", base_url + "getNotas", bodynotas)
    return notas

def observaciones():
    body_obs = "X_MATRICULA=" + user["matricula"]
    observaciones = req("POST", base_url + "getObservaciones", body_obs)
    return observaciones

def centro():
    body = "X_CENTRO=" + user["centro"]
    centro = req("POST", base_url + "datosCentro", body)
    return centro

def cerrarsesion():
    os.remove("data/imagen.png")
    if (config['Config']['loginremember'] == "N"):
        # Al no haber configuración escrita respecto al login, ignora esta parte
        pass
    else:
        config.remove_section('Cookies')
        config.remove_section('Login')
        with open("data/config.ini", "w") as configfile:
            config.write(configfile)
