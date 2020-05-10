#!/usr/bin/env python
# -*- coding: utf-8 -*-



# ADVERTENCIA
# ESTE ARCHIVO YA NO SE UTILIZA. EN SU LUGAR, UTILIZA openpython.py



import requests
import json
import configparser
import shutil
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

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

base_url = "https://www.juntadeandalucia.es/educacion/seneca/seneca/jsp/pasendroid/" # Este es el comienzo de todas las URLs de PASEN

class userinfo:
    # Al conseguir iniciar sesión, establecer variables, se utilizan luego
    def __init__(self, main):
        # Info Básica
        self.nombre = main.json()['RESULTADO'][0]['USUARIO']
        # Mi perfil
        self.curso = main.json()['RESULTADO'][0]['MATRICULAS'][0]['CURSO']
        self.unidad = main.json()['RESULTADO'][0]['MATRICULAS'][0]['UNIDAD']
        self.denominacion = main.json()['RESULTADO'][0]['MATRICULAS'][0]['DENOMINACION']
        self.tutor = main.json()['RESULTADO'][0]['MATRICULAS'][0]['TUTOR']
        # Mi centro
        # IDs que se usarán después
        self.matricula = main.json()['RESULTADO'][0]['MATRICULAS'][0]['X_MATRICULA']
        self.centro = main.json()['RESULTADO'][0]['MATRICULAS'][0]['X_CENTRO']
    
    def convcentro_get(self, evaluacion):
        bodyconv = "X_MATRICULA=" + user.matricula
        convocatorias = req("POST", base_url + "getConvocatorias", bodyconv)
        cantidad_convocatorias = len(convocatorias.json()['RESULTADO'])
        for i in range(0, cantidad_convocatorias):
            if (convocatorias.json()['RESULTADO'][i]['D_CONVOCATORIA'] == evaluacion):
                self.convcentro = convocatorias.json()['RESULTADO'][i]['X_CONVCENTRO']
    
    def getfoto(self):
        # Para ahorrar tiempo, comprueba primero si el archivo existe
        try:
            local_file = open('data/imagen.png', 'rb')
        except IOError:
            # Si no existe lo descarga
            bodyfoto = "X_MATRICULA=" + user.matricula
            foto_req = requests.post(base_url + "imageAlumno", headers=headerspost, cookies=jar, data=bodyfoto, stream=True, timeout=3)
            # Guarda el archivo localmente
            local_file = open('data/imagen.png', 'wb')
            foto_req.raw.decode_content = True
            shutil.copyfileobj(foto_req.raw, local_file)

# GTK Handler
class Handler:
    # Global
    def onDestroy(self, *args):
       Gtk.main_quit()

    # Muy importante, hace que al abrir y cerrar un widget, en el momento de volver a abrirlo se muestre correctamente
    def delete_event(self, widget, event):
        widget.hide()
        return True

    # --------- Botones --------- #
    # Botón login pulsado
    def on_login_clicked(self, button):
        body = 'p={"version":"11.9.1"}&USUARIO=' + builder.get_object('username').get_text() + '&CLAVE=' + builder.get_object('password').get_text()
        login = requests.post(base_url + "login", headers=headerspost, data=body)
        # Comprobando si se ha iniciado sesión correctamente
        if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
            print("Error al iniciar sesión")
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

        with open('data/config.ini', 'w') as configfile:
            config.write(configfile)
        builder.get_object("login_menu").hide()
        builder.get_object("main_menu").show()

    # Ventana error al iniciar sesión
    def on_error_volver_boton_clicked(self, button):
        builder.get_object("login_error").destroy()
    
    #Main menu
    def on_notas_clicked(self,button):
        builder.get_object("notas_menu").show()  

    def on_continuar_notas_boton_clicked(self, button):
        # TODO Puro spaguetti, lo limpiaré cuando tenga tiempo
        notas_evaluacion = builder.get_object("notascombo").get_active_text()
        user.convcentro_get(notas_evaluacion) # Conseguir la convcentro desde la clase userinfo

        notas_menu = builder.get_object("notas_evaluacion_menu")
        notas_grid = builder.get_object("notas_grid")

        # Muy importante, hace que el usuario pueda elegir otra evaluación en la misma sesión sin recibir los mismos resultados
        notas_grid.destroy()

        notas_menu.add(notas_grid)
        # Requests para conseguir las notas con su body. Asignación de variables iniciales
        # Para poder conseguir las notas, primero hay que conseguir la variable X_CONVCENTRO, la cual está en getConvocatorias
        bodynotas = "X_MATRICULA=" + user.matricula + "&X_CONVCENTRO=" + str(user.convcentro)
        notas = req("POST", base_url + "getNotas", bodynotas)
        cantidad_notas = len(notas.json()['RESULTADO'])
        label_asignatura = []
        label_nota = []
        nota_media = []
        for i in range(0, cantidad_notas):
            label_asignatura.append('label_asignatura' + str(i))
            label_asignatura[i] = Gtk.Label()

            label_nota.append('label_asignatura' + str(i))
            label_nota[i] = Gtk.Label()
            
            if (notas.json()['RESULTADO'][i]['CONV'] == notas_evaluacion):
                if (i == 0):
                    print("Creado")
                    notas_grid.add(label_asignatura[i])
                    notas_grid.attach_next_to(label_nota[i], label_asignatura[i], Gtk.PositionType.RIGHT, 1, 1)
                else:
                    notas_grid.attach_next_to(label_asignatura[i], label_asignatura[i-1], Gtk.PositionType.BOTTOM, 1, 1)
                    notas_grid.attach_next_to(label_nota[i], label_asignatura[i], Gtk.PositionType.RIGHT, 1, 1)
                
                if (i == cantidad_notas - 1):
                    label_nota_ultimo = label_nota[i]
                    label_asignatura_ultimo = label_asignatura[i]
                
                # TODO DEPRECATED, REMPLAZAR CUANDO SEA POSIBLE, escribe color dependiendo de la nota
                if (int(notas.json()['RESULTADO'][i]['NOTA']) < 5):
                    label_nota[i].modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))
                elif (int(notas.json()['RESULTADO'][i]['NOTA']) == 5):
                    label_nota[i].modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("orange"))
                elif (int(notas.json()['RESULTADO'][i]['NOTA']) > 5):
                    label_nota[i].modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("green"))
                
                label_asignatura[i].set_text(notas.json()['RESULTADO'][i]['D_MATERIA'])
                label_nota[i].set_text(notas.json()['RESULTADO'][i]['NOTA'])
                nota_media.append(int(notas.json()['RESULTADO'][i]['NOTA']))
                print("Escribiendo asignatura (" + str(i) + "): " + notas.json()['RESULTADO'][i]['D_MATERIA'] + " y nota: " + notas.json()['RESULTADO'][i]['NOTA'] + " en " + str(label_asignatura[i]) + " y " + str(label_nota[i]))

            else:
                print(notas.json()['RESULTADO'][i]['CONV'] + " y " + notas_evaluacion + " no coinciden")
        
        if (label_nota == []):
            label_notfound = Gtk.Label()
            notas_grid.add(label_notfound)
            label_notfound.set_text("No hay notas en esta evaluación")
        
        else:
            # Detalles finales, media y aviso
            media_final = sum(nota_media) / len(nota_media)
            label_media_titulo = Gtk.Label()
            label_media_num = Gtk.Label()
            #label_advertencia_txt = Gtk.Label()

            notas_grid.attach_next_to(label_media_titulo, label_asignatura_ultimo, Gtk.PositionType.BOTTOM, 1, 2)
            notas_grid.attach_next_to(label_media_num, label_nota_ultimo, Gtk.PositionType.BOTTOM, 1, 2)
            #notas_grid.attach_next_to(label_advertencia_txt, label_media_num, Gtk.PositionType.BOTTOM, 2, 1)
            label_media_titulo.set_text("Tu media de esta evaluación es: ")

            if (int(notas.json()['RESULTADO'][i]['NOTA']) < 5):
                label_media_num.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))
            elif (int(notas.json()['RESULTADO'][i]['NOTA']) == 5):
                label_media_num.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("orange"))
            elif (int(notas.json()['RESULTADO'][i]['NOTA']) > 5):
                label_media_num.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("green"))
            
            label_media_num.set_text(str(round(media_final, 2)))
            #label_advertencia_txt.set_text(notas.json()['ESTADO']['DESCRIPCION'])

            #TODO Mostrar advertencia usando las dos filas disponibles

        notas_menu.show_all()

    def on_act_eval_clicked(self, button):
        builder.get_object("actividades_eval_menu").show()
    
    def on_continuar_acteval_boton_clicked(self,button):
        acteval_evaluacion = builder.get_object("actevalcombo").get_active_text()
        user.convcentro_get(acteval_evaluacion)

        #acteval = requests.post(base_url + "getActividadesEvaluables", headers=headerslogin, cookies=jar, data=bodynotas)
        # TODO Continuar con las actividades evaluables

    # Botón avisos pulsado
    def on_avisos_boton_clicked(self, button):
        print("EN CONSTRUCCIÓN")
        builder.get_object("avisos").show()
        avisos = req("GET", base_url + "avisos")
        if (avisos.text == '{"ESTADO":{"CODIGO":"C"},"RESULTADO":[]}'):
            builder.get_object("avisos_label").set_markup("No hay avisos disponibles")
        else:
            builder.get_object("avisos_label").set_markup(avisos.json()['RESULTADO'][0]['D_AVISO']) # A veces puede fallar, investigando mejores métodos
    
    def on_conductas_clicked(self, button):
        # TODO Prácticamente un placeholder
        body_cond = "X_MATRICULA=" + user.matricula 
        cond = req("POST", base_url + "getConductasContrarias", body_cond)
        if (cond.text == '{"ESTADO":{"CODIGO":"C"},"RESULTADO":[]}'):
            builder.get_object("label_conductas").set_markup("No tienes ninguna conducta contraria")
        
        builder.get_object("conductas_menu").show_all()
    def on_observaciones_clicked(self, button):
        obs_menu = builder.get_object("observaciones_menu")
        obs_box = builder.get_object("observaciones_box")
        body_obs = "X_MATRICULA=" + user.matricula
        obs = req("POST", base_url + "getObservaciones", body_obs)
        cantidad_obs = len(obs.json()['RESULTADO'])
        label_obs = []
        for i in range(0, cantidad_obs):
            label_obs.append('label_obs' + str(i))
            label_obs[i] = Gtk.Label()
            obs_box.add(label_obs[i])
            label_obs[i].set_text(obs.json()['RESULTADO'][i]['PROFESOR'] + ": " + obs.json()['RESULTADO'][i]['D_MATERIAC'] + ". Escrito el " + obs.json()['RESULTADO'][i]['F_OBSMAT'] + "\n" + obs.json()['RESULTADO'][i]['T_OBSMATERIA'])
        
        obs_menu.show_all()
    
    #Header menú principal
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
        centro = req("POST", base_url + "datosCentro", body)
        centro.json()['RESULTADO'][0]['DATOS']
    
    # Botón cerrar sesión pulsado
    def on_cerrarsesion_activate(self,button):
        config.remove_section('Cookies')
        config.remove_section('Login')
        with open("data/config.ini", "w") as configfile:
            config.write(configfile)
        builder.get_object('main_menu').hide()
        builder.get_object('login_menu').show()
    
    # --------- Funciones que se ejecutan cuando se abre una ventana --------- #
    # Ejecutar cuando el menú principal se muestre
    def on_main_menu_show(self, *args):
        try:
            main = req("GET", base_url + "infoSesion")
            global user
            user = userinfo(main)
            user.getfoto()
            builder.get_object("bienvenido_label").set_text("Bienvenido, " + user.nombre)
        
        #Si hay un KeyError es que las cookies han caducado, por lo que intenta volver a iniciar sesión
        except KeyError:
            builder.get_object('main_menu').hide()
            print("Las cookies han expirado, generando nuevas...")
            body = 'p={"version":"11.9.1"}&USUARIO=' + config['Login']['Username'] + '&CLAVE=' + config['Login']['Password']
            login = req("POST", base_url + "login", body)

            if (login.text != '{"ESTADO":{"CODIGO":"C"}}'):
                print("Error al iniciar sesión")
                quit(1)
            
            # Algo ha tenido que cambiar en los servidores de la Junta, de momento esto funciona
            try:
                jar.set('JSESSIONID', login.cookies['JSESSIONID'], domain='www.juntadeandalucia.es', path='/')
                config.set('Cookies', 'JSESSIONID', login.cookies['JSESSIONID'])
            except KeyError:
                print("JSESSIONID no recibido")

            try:
                jar.set('SenecaP', login.cookies['SenecaP'], domain='www.juntadeandalucia.es', path='/')
                config.set('Cookies', 'SenecaP', login.cookies['SenecaP'])
            except KeyError:
                print("SenecaP no recibido")
            
            with open('data/config.ini', 'w') as configfile:
                config.write(configfile)

            print("Reiniciado")
            builder.get_object('main_menu').show_all()

# Iniciar builder y mostrar menú login
config = configparser.ConfigParser()
config.read('data/config.ini')
builder = Gtk.Builder()
builder.add_from_file("assets/glade/openpasen.glade")
builder.connect_signals(Handler())

# Si hay una configuración ya creada iniciar sesión con esa información
try:
    config.items('Login')
    jar = requests.cookies.RequestsCookieJar()
    jar.set('SenecaP', config['Cookies']['SenecaP'], domain='www.juntadeandalucia.es', path='/')
    jar.set('JSESSIONID', config['Cookies']['JSESSIONID'], domain='www.juntadeandalucia.es', path='/')
    builder.get_object("main_menu").show()
except configparser.NoSectionError:
    builder.get_object("login_menu").show()

Gtk.main()
