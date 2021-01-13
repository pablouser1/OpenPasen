#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from openpasen import common
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
def req(method, url, body = None):
    try:
        if (method == "GET"):
            data = requests.get(url, headers=headers, cookies=jar, data=body, timeout=5, verify="cert/juntadeandalucia-es-chain.pem")
        if (method == "POST"):
            data = requests.post(url, headers=headerspost, cookies=jar, data=body, timeout=5, verify="cert/juntadeandalucia-es-chain.pem")
        # El encoding del servidor es ISO-8859-1
        data.encoding = 'ISO-8859-1'
        # Si el servidor devuelve un error hacer una exception
        if (data.json()['ESTADO']['CODIGO'] == "E"):
            raise Exception(data.json()['ESTADO']['DESCRIPCION'])
        return data
    
    # Timeout
    except requests.exceptions.RequestException as e:
        print(f'Error de conexión, {e}')
        quit(1)  # TODO, administrar mejor los errores

# Initial variables
headers = {
    "Content-Type": "application/json",
    "User-Agent": "OpenPasen"
}

headerspost = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "OpenPasen"
}

base_url = "https://seneca.juntadeandalucia.es/seneca/jsp/pasendroid/" # Este es el comienzo de todas las URLs de PASEN

def login(logininfo):
    # (logininfo): 0 = Username | 1 = Password | 2 = Remember me

    body = 'USUARIO=' + logininfo[0] + '&CLAVE=' + logininfo[1] + '&p={"version":"11.10.5"}'
    login = req("POST", base_url + "login", body)
    # Comprobando si se ha iniciado sesión correctamente
    if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
        print("Error al iniciar sesión")
        quit(1)

    jar.set('SenecaP', login.cookies['SenecaP'], domain='seneca.juntadeandalucia.es', path='/')
    jar.set('JSESSIONID', login.cookies['JSESSIONID'], domain='seneca.juntadeandalucia.es', path='/')
    # Guardar configuración de inicio de sesión si se ha marcado el botón de mantener sesión iniciada
    if (logininfo[2] == True):
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
    with open(common.config_path + "config.ini", 'w') as configfile:
        config.write(configfile)

def checksession():
    try:
        req("GET", base_url + "infoSesion").json()['RESULTADO'][0]['USUARIO']
        print("Sesión ok")
    except KeyError:
        print("Las cookies han expirado, generando nuevas...")
        body = 'USUARIO=' + config['Login']['Username'] + '&CLAVE=' + config['Login']['Password'] + '&p={"version":"11.10.5"}'
        login = req("POST", base_url + "login", body)
        if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
            print(f'Error al iniciar sesión,\n{login.text}')
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
        with open(common.config_path + "config.ini", 'w') as configfile:
            config.write(configfile)

def userinfo():
    main = req("GET", base_url + "infoSesion").json()
    global user
    if (main['RESULTADO'][0]["C_PERFIL"] == "ALU"):
        # Usuario es alumno
        user = {
            "nombre" : main['RESULTADO'][0]['USUARIO'],
            "curso" : main['RESULTADO'][0]['MATRICULAS'][0]['CURSO'],
            "unidad" : main['RESULTADO'][0]['MATRICULAS'][0]['UNIDAD'],
            "denominacion" : main['RESULTADO'][0]['MATRICULAS'][0]['DENOMINACION'],
            "tutor" : main['RESULTADO'][0]['MATRICULAS'][0]['TUTOR'],
            "matricula" : main['RESULTADO'][0]['MATRICULAS'][0]['X_MATRICULA'],
            "centro" : main['RESULTADO'][0]['MATRICULAS'][0]['X_CENTRO'],
            "tipo": main['RESULTADO'][0]["C_PERFIL"],
        }
    elif(main['RESULTADO'][0]["C_PERFIL"] == "TUT_LEGAL"):
        # Usuario es padre
        return {
            "nombre" : main['RESULTADO'][0]['USUARIO'],
            "hijos": main['RESULTADO'][0]['HIJOS'],
            "tipo": main['RESULTADO'][0]["C_PERFIL"],
        }
    
    foto_local = getpic(user["matricula"])
    
    user.update( {"foto" : foto_local} ) # Agregar foto al dict user
    return user

def getpic(matricula):
    try:
        foto_local = open(common.config_path + "imagen.png", 'rb')
        print("Imagen encontrada")
    except IOError:
        print("Foto no encontrada, descargando...")
        # Si no existe lo descarga
        bodyfoto = "X_MATRICULA=" + user["matricula"]
        foto_req = requests.post(base_url + "imageAlumno", headers=headerspost, cookies=jar, data=bodyfoto, stream=True, timeout=3, verify="cert/juntadeandalucia-es-chain.pem")
        # Guarda el archivo localmente
        foto_local = open(common.config_path + "imagen.png", 'wb')
        foto_req.raw.decode_content = True
        shutil.copyfileobj(foto_req.raw, foto_local)
    finally:
        return foto_local

def convcentro(evaluacion):
    bodyconv = "X_MATRICULA=" + user["matricula"]
    convocatorias = req("POST", base_url + "getConvocatorias", bodyconv)
    for i in range(0, len(convocatorias.json()['RESULTADO'])):
        if (convocatorias.json()['RESULTADO'][i]['D_CONVOCATORIA'] == evaluacion):
            return convocatorias.json()['RESULTADO'][i]['X_CONVCENTRO']

def getNotas(convcentro, notas_evaluacion):
    bodynotas = "X_MATRICULA=" + user["matricula"] + "&X_CONVCENTRO=" + str(convcentro)
    notas_req = req("POST", base_url + "getNotas", bodynotas).json()
    notas = {
        "asignaturas": [],
        "notas_num": []
    }
    for i in range(0,len(notas_req['RESULTADO'])):
        notas["asignaturas"].append(notas_req['RESULTADO'][i]['D_MATERIA'])
        notas["notas_num"].append(notas_req['RESULTADO'][i]['NOTA'])
    
    return notas

def getMateriasMatricula():
    bodymaterias = "X_MATRICULA=" + user["matricula"]
    matmatricula = req("POST", base_url + "getMateriasMatricula", bodymaterias)
    materias = []
    for i in range (0, len(matmatricula.json()['RESULTADO'])):
        materias.append(matmatricula.json()['RESULTADO'][i]['D_MATERIAC'])
    return materias

def actividadesevaluables(convcentro, asignatura):
    # Antes de empezar, necesitamos saber las asignaturas
    bodyevaluacones = "X_MATRICULA=" + user["matricula"] + "&X_CONVCENTRO=" + str(convcentro)
    acteval_req = req("POST", base_url + "getActividadesEvaluables", bodyevaluacones).json()
    acteval = {
        "tema": [],
        "nota": []
    }
    for i in range(0,len(acteval_req['RESULTADO'])):
        if (asignatura == "Todas"):
            acteval["tema"].append(acteval_req['RESULTADO'][i]['D_ACTEVA'])
            acteval["nota"].append(acteval_req['RESULTADO'][i]['N_NOTA'])
        elif (acteval_req['RESULTADO'][i]['D_MATERIAC'] == asignatura):
            acteval["tema"].append(acteval_req['RESULTADO'][i]['D_ACTEVA'])
            acteval["nota"].append(acteval_req['RESULTADO'][i]['N_NOTA'])

    return acteval

def avisos():
    avisos = req("GET", base_url + "avisos")
    print(avisos.text)
    return avisos

def comunicaciones():
    comunicaciones = req("GET", base_url + "getComunicaciones")
    return comunicaciones

def conductas():
    bodyconductas = "X_MATRICULA=" + user["matricula"]
    conductas = req("POST", base_url + "getConductasContrarias", bodyconductas)
    return conductas

def observaciones():
    body_obs = "X_MATRICULA=" + user["matricula"]
    observaciones = req("POST", base_url + "getObservaciones", body_obs)
    observaciones_dict = {
        "Asignaturas": [],
        "Mensajes": [],
        "Fechas": []
    }
    for i in range(0,len(observaciones.json()['RESULTADO'])):
        observaciones_dict["Asignaturas"].append(observaciones.json()['RESULTADO'][i]['D_MATERIAC'])
        observaciones_dict["Mensajes"].append(observaciones.json()['RESULTADO'][i]['T_OBSMATERIA'])
        observaciones_dict["Fechas"].append(observaciones.json()['RESULTADO'][i]['F_OBSMAT'])
    return observaciones_dict

def horario():
    body_horario = "X_MATRICULA=" + user["matricula"]
    horario = req("POST", base_url + "getHorario", body_horario)
    horario_dict = {
        "Lunes": [],
        "Martes": [],
        "Miercoles": [],
        "Jueves": [],
        "Viernes": [],
    }
    for i in range(0, len(horario.json()['RESULTADO'])):
        # Elimina todo lo que va después del paréntesis (para que quepa en la tabla)
        temp = horario.json()['RESULTADO'][i]['PROF'].split("(", 1)[0]
        final = temp.strip()
        dia = horario.json()['RESULTADO'][i]['DIA']
        horario_dict[dia].append(final)
    
    return horario_dict

def faltas():
    body_faltas = "X_MATRICULA=" + user["matricula"]
    faltas_req = req("POST", base_url + "getFaltas", body_faltas)
    faltas = {
        "Asignaturas": [],
        "Fechas y Horas": [],
        "Justificada": []
    }
    for i in range(0, len(faltas_req.json()['RESULTADO'])):
        faltas["Asignaturas"].append(faltas_req.json()['RESULTADO'][i]['D_MATERIAC'])
        faltas["Fechas y Horas"].append(f'{faltas_req.json()["RESULTADO"][i]["F_FALASI"]}, {faltas_req.json()["RESULTADO"][i]["TRAMO"]}')
        faltas["Justificada"].append(faltas_req.json()['RESULTADO'][i]['TIPFAL'])

    return faltas

def centro():
    body = "X_CENTRO=" + user["centro"]
    centro_req = req("POST", base_url + "datosCentro", body)
    centro = {}
    for info in centro_req.json()['RESULTADO']:
        centro[info["SECCION"]] = info["DATOS"]
    return centro

def cerrarsesion():
    os.remove(common.config_path + "imagen.png")
    if (config['Config']['loginremember'] == "N"):
        # Al no haber configuración escrita respecto al login, ignora esta parte
        pass
    else:
        config.remove_section('Cookies')
        config.remove_section('Login')
        with open(common.config_path + "config.ini", "w") as configfile:
            config.write(configfile)
