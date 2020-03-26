import requests
import json
import gi
#import configparser TODO
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#Initial variables
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
        self.matricula = main.json()['RESULTADO'][0]['MATRICULAS'][0]['X_MATRICULA']
        self.centro = main.json()['RESULTADO'][0]['MATRICULAS'][0]['X_CENTRO']
    
#Facilitar las requests
def req(method, url):
    if (method == "GET"):
        data = requests.get(url, headers=headers, cookies=jar)
        return data
    if (method == "POST"):
        data = requests.post(url, headers=headers, cookies=jar)
        return data

#GTK Handler
class Handler:
    def onDestroy(self, *args):
       Gtk.main_quit()
    
    #Ventana error al iniciar sesión
    def on_error_volver_boton_clicked(self, button):
        builder.get_object("login_error").destroy()
    
    #Ventana acerca de activada
    def on_about_button_activate(self, button):
        builder = Gtk.Builder()
        builder.get_object("about").show()
    
    #Botón login pulsado
    def on_login_clicked(self, button):
        username = builder.get_object('username').get_text()
        password = builder.get_object('password').get_text()
        body = 'p={ "version":"11.9.1" }&USUARIO=' + username + '&CLAVE=' + password
        login = requests.post("https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/login", headers=headerslogin, data=body)
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
    
    #Ejecutar cuando el menú principal se muestre
    def on_main_menu_show(self, *args):
        main = req("GET", "https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/infoSesion")
        print("Escribiendo datos del usuario...")
        user = userinfo(main)
        builder.get_object("bienvenido_buffer").set_text("Bienvenido, " + user.nombre)

        # TODO Hacer aparecer imagen alumno

builder = Gtk.Builder()
builder.add_from_file("assets/glade/openpasen.glade")
builder.connect_signals(Handler())
builder.get_object("login_menu").show()
Gtk.main()

# TODO https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/avisos (Avisos ventana emergente) | GET
# TODO https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/getComunicaciones (Comunicaciones profe <-> alumno) | GET
# TODO https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/getConvocatorias (Actividades evaluables) | POST?
# TODO https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/getNotas (NOTAS) | POST