#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import configparser
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Initial variables
headers = {
    "Content-Type": "application/json; charset=UTF-8"
}

headerslogin = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

class userinfo:
    # Al conseguir iniciar sesión, establecer variables, se utilizan luego
    def __init__(self, main):
        self.nombre = main.json()['RESULTADO'][0]['USUARIO']
        self.curso = main.json()['RESULTADO'][0]['MATRICULAS'][0]['CURSO']
        self.unidad = main.json()['RESULTADO'][0]['MATRICULAS'][0]['UNIDAD']
        self.denominacion = main.json()['RESULTADO'][0]['MATRICULAS'][0]['DENOMINACION']
        self.tutor = main.json()['RESULTADO'][0]['MATRICULAS'][0]['TUTOR']
        #IDs que se usarán después
        self.matricula = main.json()['RESULTADO'][0]['MATRICULAS'][0]['X_MATRICULA']
        self.centro = main.json()['RESULTADO'][0]['MATRICULAS'][0]['X_CENTRO']
    
    def convcentro_get(self, convocatorias, notas_evaluacion):
        cantidad_convocatorias = len(convocatorias.json()['RESULTADO'])
        for i in range(0, cantidad_convocatorias):
            if (convocatorias.json()['RESULTADO'][i]['D_CONVOCATORIA'] == notas_evaluacion):
                self.convcentro = convocatorias.json()['RESULTADO'][i]['X_CONVCENTRO']

    
#Facilitar las requests
def req(method, url):
    if (method == "GET"):
        data = requests.get(url, headers=headers, cookies=jar)
        return data
    if (method == "POST"):
        data = requests.post(url, headers=headers, cookies=jar)
        return data


# GTK Handler
class Handler:
    # Global
    def onDestroy(self, *args):
       Gtk.main_quit()
    
    def delete_event(self, widget, event):
        widget.hide()
        return True 
    
    # --------- Botones --------- #
    # Botón login pulsado
    def on_login_clicked(self, button):
        body = 'p={"version":"11.9.1"}&USUARIO=' + builder.get_object('username').get_text() + '&CLAVE=' + builder.get_object('password').get_text()
        login = requests.post("https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/login", headers=headerslogin, data=body)
        # Comprobando si se ha iniciado sesión correctamente
        if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
            builder.get_object('login_error').show()
            quit(1)
        global jar
        jar = requests.cookies.RequestsCookieJar()
        jar.set('SenecaP', login.cookies['SenecaP'], domain='www.juntadeandalucia.es', path='/')
        jar.set('JSESSIONID', login.cookies['JSESSIONID'], domain='www.juntadeandalucia.es', path='/')
        print("Las cookies usadas son: " + str(jar))

        # Guardar configuración de inicio de sesión si se ha marcado el botón de mantener sesión iniciada
        if (str(builder.get_object('sesioniniciada').get_active()) == "True"):
            print("Guardando información de inicio de sesión...")
            config['Cookies'] = {
                'SenecaP': login.cookies['SenecaP'],
                'JSESSIONID': login.cookies['JSESSIONID']}
            
            config['Login'] = {
                'Username': builder.get_object('username').get_text(),
                'Password': builder.get_object('password').get_text()}
            
            config['Config'] = {
                'LoginRemember': "Y"}
        else:
            config['Config'] = {
                'LoginRemember': "N"}
        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        builder.get_object("login_menu").hide()
        builder.get_object("main_menu").show()
    
    # Ventana error al iniciar sesión
    def on_error_volver_boton_clicked(self, button):
        builder.get_object("login_error").destroy()
    
    #Main menu
    
    # Botón avisos pulsado
    def on_avisos_boton_clicked(self, button):
        print("EN CONSTRUCCIÓN")
        #builder.get_object("avisos").show()
        #avisos = req("GET", "https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/avisos")
        #builder.get_object("avisos_label").set_markup(avisos.json()['RESULTADO'][0]['D_AVISO']) #TODO Error
    
    def on_notas_clicked(self,button):
        builder.get_object("notas_menu").show()

    def on_continuar_notas_boton_clicked(self, button):
        # Para poder conseguir las notas, primero hay que conseguir la variable X_CONVCENTRO, la cual está en getConvocatorias

        # TODO Puro spaguetti, lo limpiaré cuando tenga tiempo
        bodyconv = "X_MATRICULA=" + user.matricula
        convocatorias = requests.post("https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/getConvocatorias", headers=headerslogin, cookies=jar, data=bodyconv)
        notas_evaluacion = builder.get_object("notascombo").get_active_text()
        user.convcentro_get(convocatorias, notas_evaluacion)

        notas_menu = builder.get_object("notas_evaluacion_menu")
        notas_grid = Gtk.Grid()
        notas_menu.add(notas_grid)
        bodynotas = "X_MATRICULA=" + user.matricula + "&X_CONVCENTRO=" + str(user.convcentro)
        notas = requests.post("https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/getNotas", headers=headerslogin, cookies=jar, data=bodynotas)
        cantidad_notas = len(notas.json()['RESULTADO'])
        label_asignatura = []
        label_nota = []
        for i in range(0, cantidad_notas):
            label_asignatura.append('label_asignatura' + str(i))
            label_asignatura[i] = Gtk.Label()

            label_nota.append('label_asignatura' + str(i))
            label_nota[i] = Gtk.Label()

            if (i == 0):
                print("Creado")
                notas_grid.add(label_asignatura[i])

                notas_grid.attach_next_to(label_nota[i], label_asignatura[i], Gtk.PositionType.RIGHT, 1, 2)
            else:
                notas_grid.attach_next_to(label_asignatura[i], label_asignatura[i-1], Gtk.PositionType.BOTTOM, 1, 2)

                notas_grid.attach_next_to(label_nota[i], label_asignatura[i], Gtk.PositionType.RIGHT, 1, 2)
            
            if (notas.json()['RESULTADO'][i]['CONV'] == notas_evaluacion):
                print("Escribiendo asignatura: " + notas.json()['RESULTADO'][i]['D_MATERIA'] + " y nota:" + notas.json()['RESULTADO'][i]['NOTA'] + " en " + str(label_asignatura[i]) + " y " + str(label_nota[i]))
                label_asignatura[i].set_text(notas.json()['RESULTADO'][i]['D_MATERIA'])
                label_nota[i].set_text(notas.json()['RESULTADO'][i]['NOTA'])


            else:
                print(notas.json()['RESULTADO'][i]['CONV'] + " y " + notas_evaluacion + " no coinciden")

        
        builder.get_object("notas_evaluacion_menu").show_all()
    #Barra de herramientas

    # Botón acerca de pulsado
    def on_ayuda_clicked(self, button):
        builder.get_object("about").show()
    
    def on_perfil_activate(self, button):
        builder.get_object("perfil_menu").show()

        builder.get_object("curso_label").set_markup(user.curso)
        builder.get_object("unidad_label").set_markup(user.unidad)
        builder.get_object("centro_label").set_markup(user.denominacion)
        builder.get_object("tutor_label").set_markup(user.tutor)

    def on_centro_activate(self, button):
        builder.get_object("centro_menu").show()
        body = "X_CENTRO=" + user.centro
        centro = requests.post("https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/datosCentro", headers=headerslogin, cookies=jar, data=body)
        centro.json()['RESULTADO'][0]['DATOS']
    
    # Botón cerrar sesión pulsado
    def on_cerrarsesion_activate(self,button):
        config.remove_section('Cookies')
        config.remove_section('Login')
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        builder.get_object('main_menu').hide()
        builder.get_object('login_menu').show()
    
    # --------- Funciones que se ejecutan cuando se abre una ventana --------- #
    # Ejecutar cuando el menú principal se muestre
    def on_main_menu_show(self, *args):
        try:
            main = req("GET", "https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/infoSesion")
            print("Escribiendo datos del usuario...")
            global user
            user = userinfo(main)
            builder.get_object("bienvenido_label").set_text("Bienvenido, " + user.nombre)
        
        #Si hay un KeyError es que las cookies han caducado, por lo que intenta volver a iniciar sesión
        except KeyError:
            builder.get_object('main_menu').hide()
            print("Las cookies han expirado, generando nuevas...")
            body = 'p={"version":"11.9.1"}&USUARIO=' + config['Login']['Username'] + '&CLAVE=' + config['Login']['Password']
            login = requests.post("https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/login", headers=headerslogin, data=body)
            if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
                print("Error al iniciar sesión, ¿tienes conexión a Internet?")
                quit(1)
            if (config['Config']['LoginRemember'] == "Y"):
                config['Cookies'] = {
                    'SenecaP': login.cookies['SenecaP'],
                    'JSESSIONID': login.cookies['JSESSIONID']}
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                    builder.get_object('main_menu').show()

# Iniciar builder y mostrar menú login
config = configparser.ConfigParser()
config.read('config.ini')
builder = Gtk.Builder()
builder.add_from_file("assets/glade/openpasen.glade")
builder.connect_signals(Handler())

# Si hay una configuración ya creada iniciar sesión con esa información
try:
    config.items('Login')
    jar = requests.cookies.RequestsCookieJar()
    jar.set('SenecaP', config['Cookies']['senecap'], domain='www.juntadeandalucia.es', path='/')
    jar.set('JSESSIONID', config['Cookies']['JSESSIONID'], domain='www.juntadeandalucia.es', path='/')
    builder.get_object("main_menu").show()
except configparser.NoSectionError:
    builder.get_object("login_menu").show()

Gtk.main()