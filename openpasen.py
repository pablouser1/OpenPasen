import requests
import os
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#Initial variables
headers = {
    "Content-Type": "application/json; charset=UTF-8"
}

headerslogin = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

#Facilitar las requests
def req(method, url):
    if (method == "GET"):
        data = requests.get(url, headers=headers, cookies=jar)
        return data
    if (method == "POST"):
        data = requests.post(url, headers=headers, cookies=jar)
        return data

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    #Botón login pulsado
    def on_login_clicked(self, button):
        username = builder.get_object('username').get_text()
        password = builder.get_object('password').get_text()
        body = 'p={ "version":"11.9.1" }&USUARIO=' + username + '&CLAVE=' + password
        login = requests.post("https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/login", headers=headerslogin, data=body)
        print(username + " " + password)
        # Comprobando si se ha iniciado sesión correctamente
        if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
            print("Error al iniciar sesión, ¿ha escrito la contraseña correcta?")
            quit(1)
        global jar
        jar = requests.cookies.RequestsCookieJar()
        jar.set('SenecaP', login.cookies['SenecaP'], domain='www.juntadeandalucia.es', path='/')
        jar.set('JSESSIONID', login.cookies['JSESSIONID'], domain='www.juntadeandalucia.es', path='/')
        print("Las cookies usadas son: " + str(jar))
        builder.get_object("login_menu").hide()
        builder.get_object("main_menu").show()

    def on_main_menu_show(self, *args):
        main = req("GET", "https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/infoSesion")
        print("Escribiendo datos del usuario...")
        builder.get_object("textbuffer1").set_text("Bienvenido, " + main.json()['RESULTADO'][0]['USUARIO'])
        #builder.get_object("bienvenido_img").
        

builder = Gtk.Builder()
builder.add_from_file("login.glade")
builder.connect_signals(Handler())

builder.get_object("login_menu").show()
Gtk.main()