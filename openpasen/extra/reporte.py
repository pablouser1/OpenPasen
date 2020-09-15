#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO, optimizar funciones
from openpasen import common, api
import os
from shutil import copyfile
def init():
    try:
        from bs4 import BeautifulSoup
        global soup
        soup = BeautifulSoup(open("assets/templates/reporte.html"), "html.parser")
        global reporte
        reporte = {}
        # Aquí se almacenarán los mensajes que se usarán en el apartado de logros del documento
        global logros_subtitles
        logros_subtitles = {}
        reportError = False
        return reportError
    except ImportError:
        print("No tienes instalado BeautifulSoup")
        reportError = True
        return reportError

def generar(seleccion):
    reportError = init()
    # Parar si el usuario no tiene bs4 instalado
    if reportError is True:
        return "ImportError"
    # Empezar con información básica del curso
    basic()
    # Ahora conseguimos las notas que tenga el usuario
    notas(seleccion)
    # Faltas
    faltas()
    # Observaciones
    observaciones()
    # Conductas contrarias
    conductas()
    # Generar html a partir de la plantilla
    html(seleccion)

    # Registrar nombre y apellidos
    nombre_final = reporte["basicinfo"]["nombre"]
    seleccion_final = seleccion.replace(" ", "") # Elimina los espacios de las evaluaciones (1ªEvaluación)
    # Crea el directorio en el que se va a guardar el informe si no existe
    try:
        os.mkdir(f'{common.config_path}{nombre_final}')
    except FileExistsError:
        pass
    out = f'{common.config_path}{nombre_final}/reporte_{seleccion_final}.html'
    copyfile('assets/img/qr-code.png', f'{common.config_path}{nombre_final}/qr-code.png')
    # Escribe el html
    with open(out, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))
    return out

def basic():
    basic = api.userinfo()
    reporte["basicinfo"] = {
        "nombre": basic["nombre"],
        "unidad": basic["unidad"],
        "centro": basic["denominacion"],
        "tutor": basic["tutor"],
        "foto": basic["foto"]
    }

def notas(seleccion):
    convcentro = api.convcentro(seleccion)
    notas = api.getNotas(convcentro, seleccion)
    reporte["notas"] = {
        "asignaturas": [],
        "notas": []
    }
    for i in range(0,len(notas["asignaturas"])):
        reporte["notas"]["asignaturas"].append(notas["asignaturas"][i])
        reporte["notas"]["notas"].append(notas["notas_num"][i])
    reporte["nota_media"] = sum(int (i) for i in reporte["notas"]["notas"]) / len(reporte["notas"]["notas"])
    # Logros
    if (reporte["nota_media"] >= 5):
        logros_subtitles["notas"] = f'🥳 Has aprobado con una nota media de {str(round(reporte["nota_media"], 2))}'

def observaciones():
    observaciones = api.observaciones()
    reporte["observaciones"] = {
        "Asignaturas": [],
        "Mensajes": [],
        "Fechas": []
    }
    for i in range(0,len(observaciones["Asignaturas"])):
        reporte["observaciones"]["Asignaturas"].append(observaciones["Asignaturas"][i])
        reporte["observaciones"]["Mensajes"].append(observaciones["Mensajes"][i])
        reporte["observaciones"]["Fechas"].append(observaciones["Fechas"][i])
def conductas():
    conductas = api.conductas()
    if (conductas.text == '{"ESTADO":{"CODIGO":"C"},"RESULTADO":[]}'):
        logros_subtitles["conductas"] = "Enhorabuena, no tienes conductas contrarias 👏"
    else:
        pass

def faltas():
    faltas = api.faltas()
    reporte["faltas"] = {
        "Asignaturas": [],
        "Fechas y Horas": [],
        "Justificada": []
    }
    for i in range(0, len(faltas["Asignaturas"])):
        reporte["faltas"]["Asignaturas"].append(faltas["Asignaturas"][i])
        reporte["faltas"]["Fechas y Horas"].append(faltas["Fechas y Horas"][i])
        reporte["faltas"]["Justificada"].append(faltas["Justificada"][i])
        if (reporte["faltas"]["Justificada"][i] == "Injustificada"):
            reporte["faltas"]["Injustificada"] = True
    # Logros
    try:
        if reporte["faltas"]["Injustificada"]:
            print("Tiene faltas injustificadas")
    except KeyError:
        logros_subtitles["faltas"] = "No tienes ninguna falta injustificada"
def html(seleccion):
    soup.find(id='alumno').string.replace_with(reporte["basicinfo"]["nombre"])
    soup.find(id='hero_sub').string.replace_with(f'{reporte["basicinfo"]["unidad"]} / {reporte["basicinfo"]["centro"]}. Tutor: {reporte["basicinfo"]["tutor"]}')
    soup.find(id='evaluacion').string.replace_with(seleccion)
    soup.find(id='foto')["src"] = f'{common.config_path}imagen.png'
    # -- Tabla notas -- #
    notas = soup.find(id='notas')
    for i in range(0, len(reporte["notas"]["asignaturas"])):
        fila = soup.new_tag('tr')
        asignatura = soup.new_tag('td')
        asignatura.append(reporte["notas"]["asignaturas"][i])
        fila.append(asignatura)
        notas.append(fila)
    filas = soup.find(id="notas").select("tr")
    for i in range(0, len(reporte["notas"]["notas"])):
        nota = soup.new_tag('td')
        nota.append(reporte["notas"]["notas"][i])
        filas[i].append(nota)
    soup.find(id='nota_media').string.replace_with(f'Tu nota media es de {str(round(reporte["nota_media"], 2))}')
    # -- Tabla faltas -- #
    faltas = soup.find(id='faltas')
    for i in range(0, len(reporte["faltas"]["Asignaturas"])):
        fila = soup.new_tag('tr')
        asignatura = soup.new_tag('td')
        asignatura.append(reporte["faltas"]["Asignaturas"][i])
        fila.append(asignatura)
        faltas.append(fila)
    filas = soup.find(id="faltas").select("tr")
    for i in range(0, len(reporte["faltas"]["Justificada"])):
        horayfecha = soup.new_tag('td')
        justificada = soup.new_tag('td')
        horayfecha.append(reporte["faltas"]["Fechas y Horas"][i])
        justificada.append(reporte["faltas"]["Justificada"][i])
        filas[i].append(horayfecha)
        filas[i].append(justificada)
    # -- Tabla observaciones -- #
    observaciones = soup.find(id='observaciones')
    for i in range(0, len(reporte["observaciones"]["Asignaturas"])):
        fila = soup.new_tag('tr')
        asignatura = soup.new_tag('td')
        asignatura.append(reporte["observaciones"]["Asignaturas"][i])
        fila.append(asignatura)
        observaciones.append(fila)
    filas = soup.find(id="observaciones").select("tr")
    for i in range(0, len(reporte["observaciones"]["Asignaturas"])):
        mensaje = soup.new_tag('td')
        fecha = soup.new_tag('td')
        mensaje.append(reporte["observaciones"]["Mensajes"][i])
        fecha.append(reporte["observaciones"]["Fechas"][i])
        filas[i].append(mensaje)
        filas[i].append(fecha)
    # -- Logros -- #
    # Eliminar section si no hay ningún logro
    if (logros_subtitles == {}):
        soup.find('section', id="logros_section").decompose()
    else:
        logros = soup.find(id='logros')
        for subtitle in logros_subtitles:
            tag = soup.new_tag('h2', **{'class':'subtitle'})
            tag.append(logros_subtitles.get(subtitle))
            logros.append(tag)
            