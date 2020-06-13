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
    def on_continuar_notas_boton_clicked(self, button):
        columns = [
            "Asignatura",
            "Nota"
        ]
        notas_evaluacion = builder.get_object("notascombo").get_active_text()
        api.convcentro(notas_evaluacion)
        notas_menu = builder.get_object("notas_evaluacion_menu")
        notas = api.getNotas()
        notas_solicitadas = api.getNotasSolicitadas(notas, notas_evaluacion)
        nota_media = []
        tree = builder.get_object("notas_treeview")
        store = builder.get_object("notas_store")
        store.clear()
        for i in range(0, len(notas_solicitadas)):
            store.insert(i, [notas.json()['RESULTADO'][notas_solicitadas[i]]['D_MATERIA'], notas.json()['RESULTADO'][notas_solicitadas[i]]['NOTA']])
            nota_media.append(int(notas.json()['RESULTADO'][notas_solicitadas[i]]['NOTA']))
        for i, column in enumerate(columns):
            cell = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(column, cell, text=i)
            tree.append_column(col)

        # Nota media
        media_final = sum(nota_media) / len(nota_media)
        builder.get_object("notas_media").set_markup("Tu nota media es de " + str(round(media_final, 2)))
        notas_menu.show()

    # Actividades evaluables
    def on_act_eval_clicked(self, button):
        builder.get_object("actividades_eval_menu").show()
    def on_continuar_acteval_boton_clicked(self,button):
        # TODO, completar
        act_evaluacion = builder.get_object("activiadescombo").get_active_text()
        api.convcentro(act_evaluacion)
        act_menu = builder.get_object("act_evaluacion_menu")
        act_grid = builder.get_object("act_grid")
        acteval = api.actividadesevaluables()

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
        columns = [
            "Asignatura",
            "Mensaje"
        ]
        observaciones = api.observaciones()
        tree = builder.get_object("observaciones_treeview")
        store = builder.get_object("observaciones_store")

        # Necesario para que no se reincluye al volver a entrar
        store.clear()
        for i in range(0, len(observaciones.json()['RESULTADO'])):
            store.append([observaciones.json()['RESULTADO'][i]['D_MATERIAC'],observaciones.json()['RESULTADO'][i]['T_OBSMATERIA']])
        for i, column in enumerate(columns):
            cell = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(column, cell, text=i)
            tree.append_column(col)

        builder.get_object("observaciones_menu").show()
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
        print(centro.text)
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

# Establece imagen del usuario, quizás hay una mejor forma de hacer esto
builder.get_object("bienvenido_img").set_from_file(common.config_path + "imagen.png")

builder.get_object(str(start)).show()
Gtk.main()
