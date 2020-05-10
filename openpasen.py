#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common
import api
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Handler:
    def __init__(self):
        print("GTK Handler Init")
    
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
        logininfo = [
            builder.get_object('username').get_text(),
            builder.get_object('password').get_text(),
            str(builder.get_object('sesioniniciada').get_active())
        ]

        api.login(logininfo)
        global user
        user = api.userinfo()
        builder.get_object("login_menu").hide()
        builder.get_object("main_menu").show()
    
    # -- Main menu -- #
    # Init
    def on_main_menu_show(self, *args):
        builder.get_object("bienvenido_label").set_text("Bienvenido, " + user["nombre"])
    # Notas
    def on_notas_clicked(self,button):
        builder.get_object("notas_menu").show()

        # TODO, completar
    def on_continuar_notas_boton_clicked(self, button):
        notas_evaluacion = builder.get_object("notascombo").get_active_text()
        api.convcentro(notas_evaluacion)
        notas_menu = builder.get_object("notas_evaluacion_menu")
        notas_grid = builder.get_object("notas_grid")

        # Muy importante, hace que el usuario pueda elegir otra evaluación en la misma sesión sin recibir los mismos resultados
        notas_grid.destroy()

        notas_menu.add(notas_grid)
        # Requests para conseguir las notas con su body. Asignación de variables iniciales
        # Para poder conseguir las notas, primero hay que conseguir la variable X_CONVCENTRO, la cual está en getConvocatorias
        notas = api.notas()
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

    # Actividades evaluables
    def on_act_eval_clicked(self, button):
        builder.get_object("actividades_eval_menu").show()
        # TODO, completar

    def on_continuar_acteval_boton_clicked(self,button):
        # TODO, completar
        pass

    # Avisos
    def on_avisos_boton_clicked(self, button):
        avisos = api.avisos()
        if (avisos.text == '{"ESTADO":{"CODIGO":"C"},"RESULTADO":[]}'):
            builder.get_object("avisos_label").set_markup("No hay avisos disponibles")
        else:
            builder.get_object("avisos_label").set_markup(avisos.json()['RESULTADO'][0]['D_AVISO']) # A veces puede fallar, investigando mejores métodos
        builder.get_object("avisos").show()
        # TODO, completar

    # Conductas contrarias
    def on_conductas_clicked(self, button):
        conductas = api.conductas()
        if (conductas.text == '{"ESTADO":{"CODIGO":"C"},"RESULTADO":[]}'):
            builder.get_object("label_conductas").set_markup("No tienes ninguna conducta contraria")
        else:
            builder.get_object("label_conductas").set_markup("WIP")

        builder.get_object("conductas_menu").show_all()
        # TODO, completar

    # Observaciones del alumnado
    def on_observaciones_clicked(self, button):
        obs_menu = builder.get_object("observaciones_menu")
        obs_box = builder.get_object("observaciones_box")
        observaciones = api.observaciones()
        cantidad_obs = len(observaciones.json()['RESULTADO'])
        label_obs = []
        for i in range(0, cantidad_obs):
            label_obs.append('label_obs' + str(i))
            label_obs[i] = Gtk.Label()
            obs_box.add(label_obs[i])
            label_obs[i].set_text(observaciones.json()['RESULTADO'][i]['PROFESOR'] + ": " + observaciones.json()['RESULTADO'][i]['D_MATERIAC'] + ". Escrito el " + observaciones.json()['RESULTADO'][i]['F_OBSMAT'] + "\n" + observaciones.json()['RESULTADO'][i]['T_OBSMATERIA'])
        
        obs_menu.show_all()

    # -- Header menú principal -- #
    # Acerca de
    def on_ayuda_clicked(self, button):
        builder.get_object("about").show()

    # Perfil
    def on_perfil_activate(self, button):
        builder.get_object("curso_label").set_markup(user["curso"])
        builder.get_object("unidad_label").set_markup(user["unidad"])
        builder.get_object("centro_label").set_markup(user["denominacion"])
        builder.get_object("tutor_label").set_markup(user["tutor"])
        builder.get_object("perfil_menu").show()

    # Mi centro
    def on_centro_activate(self, button):
        centro = api.centro()
        builder.get_object("centro_menu").show()
        # TODO, completar

    # Cerrar sesión
    def on_cerrarsesion_activate(self,button):
        api.cerrarsesion()
        builder.get_object('main_menu').hide()
        builder.get_object('login_menu').show()

# Initial startup
common.init()
api.init()
start = common.getsession()

if (start == "main_menu"):
    api.checksession()
    global user
    user = api.userinfo() # Consigue la información básica del usuario

# Start GTK builder
builder = Gtk.Builder()
builder.add_from_file("assets/glade/openpasen.glade")
builder.connect_signals(Handler())

builder.get_object(str(start)).show()
Gtk.main()
