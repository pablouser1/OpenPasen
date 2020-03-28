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
        self.matricula = main.json()['RESULTADO'][0]['MATRICULAS'][0]['X_MATRICULA']
        self.centro = main.json()['RESULTADO'][0]['MATRICULAS'][0]['X_CENTRO']
        self.curso = main.json()['RESULTADO'][0]['MATRICULAS'][0]['CURSO']
        self.unidad = main.json()['RESULTADO'][0]['MATRICULAS'][0]['UNIDAD']
    
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
    # Global (Destroy)
    def onDestroy(self, *args):
       Gtk.main_quit()
    
    # --------- Botones --------- #
    # Botón login pulsado
    def on_login_clicked(self, button):
        body = 'p={"version":"11.9.1"}&USUARIO=' + builder.get_object('username').get_text() + '&CLAVE=' + builder.get_object('password').get_text()
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
        if (builder.get_object('sesioniniciada').get_active):
            config['Login'] = {
                'SenecaP': login.cookies['SenecaP'],
                'JSESSIONID': login.cookies['JSESSIONID']}
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
        #builder.get_object("avisos_label").set_markup(avisos.json()['RESULTADO'][0]['D_AVISO']) #Error, target
    
    #Barra de herramientas

    # Botón acerca de pulsado
    def on_about_boton_activate(self, button):
        builder.get_object("about").show()
    
    def on_perfil_boton_activate(self, button):
        print("WIP")
    # Botón cerrar sesión pulsado
    def on_logout_boton_activate(self,button):
        config.remove_section('Login')
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        builder.get_object('main_menu').hide()
        builder.get_object('login_menu').show()
    
    # --------- Funciones que se ejecutan cuando se abre una ventana --------- #
    # Ejecutar cuando el menú principal se muestre
    def on_main_menu_show(self, *args):
        main = req("GET", "https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/infoSesion")
        print("Escribiendo datos del usuario...")
        global user
        user = userinfo(main)
        builder.get_object("bienvenido_buffer").set_text("Bienvenido, " + user.nombre)
        # TODO Hacer aparecer imagen alumno

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
    jar.set('SenecaP', config['Login']['senecap'], domain='www.juntadeandalucia.es', path='/')
    jar.set('JSESSIONID', config['Login']['JSESSIONID'], domain='www.juntadeandalucia.es', path='/')
    builder.get_object("main_menu").show()
except configparser.NoSectionError:
    builder.get_object("login_menu").show()

Gtk.main()