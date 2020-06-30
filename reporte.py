#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common
import api
import os
from shutil import copyfile
reportError = False
path = os.path.dirname(os.path.realpath(__file__))
try:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(open("assets/html/template.html"), "html.parser")
except ImportError:
    reportError = True
    print("No tienes instalado BeautifulSoup")

reporte = {}
def generar(seleccion):
    if reportError is True:
        return "ImportError"
    # Empezar con información básica del curso
    basic()
    # Ahora conseguimos las notas que tenga el usuario
    notas(seleccion)
    # Generar html a partir de la plantilla
    out = html()
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

def html():
    soup.find(id='alumno').string.replace_with(reporte["basicinfo"]["nombre"])
    soup.find(id='curso_centro').string.replace_with(f'{reporte["basicinfo"]["unidad"]} / {reporte["basicinfo"]["centro"]}')
    soup.find(id='foto')["src"] = f'{common.config_path}imagen.png'
    # Tabla notas
    notas = soup.find(id='notas')
    for i in range(0, len(reporte["notas"]["asignaturas"])):
        new_tr = soup.new_tag('tr')
        new_td = soup.new_tag('td')
        new_td.append(reporte["notas"]["asignaturas"][i])
        new_tr.append(new_td)
        notas.append(new_tr)
    trs = soup.find(id="notas").select("tr")
    for i in range(0, len(reporte["notas"]["notas"])):
        new_td = soup.new_tag('td')
        new_td.append(reporte["notas"]["notas"][i])
        trs[i].append(new_td)
    nota_media = sum(int (i) for i in reporte["notas"]["notas"]) / len(reporte["notas"]["notas"])
    soup.find(id='nota_media').string.replace_with(f'Tu nota media es de {str(round(nota_media, 2))}')
    
    # Registrar sólo en NOMBRE
    nombre_split = reporte["basicinfo"]["nombre"].split(", ",1)[1]
    try:
        os.mkdir(f'{common.config_path}{nombre_split}')
    except FileExistsError:
        pass
    out = f'{common.config_path}{nombre_split}/reporte.html'
    copyfile('assets/img/qr-code.png', f'{common.config_path}{nombre_split}/qr-code.png')
    # Escribe el html
    with open(out, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))
    return out