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
        builder.get_object("bienvenido_img").set_from_file(f'{common.config_path}imagen.png') # Perfil usuario
        builder.get_object("login_menu").hide()
        builder.get_object("main_menu").show()
    
    # -- Main menu -- #
    # Init
    def on_main_menu_show(self, *args):
        builder.get_object("bienvenido_label").set_text(f'Bienvenido, {user["nombre"]}')
    # Notas
    def on_notas_clicked(self,button):
        builder.get_object("notas_menu").show()
    def on_continuar_notas_boton_clicked(self, button):
        # Por algún motivo, esto es necesario para que al cerrar y volver a abrir se pueda ver el treeview
        notas_menu = builder.get_object("notas_evaluacion_menu")
        notas_box = builder.get_object("notas_box")
        notas_box.get_parent().remove(notas_box)
        notas_menu.add(notas_box)

        notas_evaluacion = builder.get_object("notascombo").get_active_text()
        convcentro = api.convcentro(notas_evaluacion)
        # Asignaturas_list tiene los nombres de las asignaturas mientras que notas_numero_list tiene la nota numérica.
        asignaturas_list, notas_numero_list = api.getNotas(convcentro, notas_evaluacion)
        # Si no hay notas disponibles, avisar y no continuar, ya que tendríamos una ZeroDivisionError
        if (notas_numero_list == []):
            builder.get_object("notas_info").set_markup(f'{notas_evaluacion} no tiene notas disponibles')
        else:
            tree = builder.get_object("notas_treeview")
            store = builder.get_object("notas_store")
            store.clear()
            for i in range(0, len(asignaturas_list)):
                store.append([asignaturas_list[i], notas_numero_list[i]])
            # Crear columnas si no existen
            if not tree.get_columns():
                columns = [
                    "Asignatura",
                    "Nota"
                    ]
                cell = Gtk.CellRendererText()
                for i, column in enumerate(columns):
                    col = Gtk.TreeViewColumn(column, cell, text=i)
                    tree.append_column(col)
            # Nota media
            media_final = sum(int (i) for i in notas_numero_list) / len(notas_numero_list)
            builder.get_object("notas_media").set_markup(f'Tu nota media es de {str(round(media_final, 2))}')
            notas_menu.show()

    # Actividades evaluables
    def on_act_eval_clicked(self, button):
        # Lista con asignaturas
        actividades_asignaturas = builder.get_object("actividades_asignaturas")
        materias = api.getMateriasMatricula()
        materias_store = Gtk.ListStore(str)
        materias_store.append(["Todas"])
        for materia in materias:
            materias_store.append([materia])
        actividades_asignaturas.set_model(materias_store)
        cell = Gtk.CellRendererText()
        actividades_asignaturas.pack_start(cell, False)
        actividades_asignaturas.set_active(0)
        builder.get_object("actividades_menu").show()

    def on_actividades_continuar_clicked(self, button):
        # Por algún motivo, esto es necesario para que al cerrar y volver a abrir se pueda ver el treeview
        actividades_menu = builder.get_object("act_eval_menu")
        actividades_box = builder.get_object("actividades_box")
        actividades_box.get_parent().remove(actividades_box)
        actividades_menu.add(actividades_box)

        actividades_asignatura = builder.get_object("actividades_asignaturas").get_active_text()
        actividades_evaluacion = builder.get_object("actividades_evaluaciones").get_active_text()
        convcentro = api.convcentro(actividades_evaluacion)
        tema_list, nota_list = api.actividadesevaluables(convcentro, actividades_asignatura)

        tree = builder.get_object("actividades_treeview")
        store = builder.get_object("actividades_store")
        store.clear()
        for i in range(0, len(tema_list)):
            store.append([tema_list[i], nota_list[i]])
        # Crear columnas si no existen
        if not tree.get_columns():
            print("Creando columnas...")
            columns = [
                "Tema",
                "Nota"
                ]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                tree.append_column(col)
        
        builder.get_object("actividades_label").set_markup(f'{actividades_asignatura} - {actividades_evaluacion}')
        builder.get_object("act_eval_menu").show()


    # Avisos
    def on_avisos_boton_clicked(self, button):
        avisos = api.avisos()
        if (avisos.text == '{"ESTADO":{"CODIGO":"C"},"RESULTADO":[]}'):
            builder.get_object("avisos_label").set_markup("No hay avisos disponibles")
        else:
            builder.get_object("avisos_label").set_markup(avisos.json()['RESULTADO'][0]['D_AVISO']) # A veces puede fallar, investigando mejores métodos
        builder.get_object("avisos").show()
    def on_avisos_ok_clicked(self, button):
        builder.get_object("avisos").hide()

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
        observaciones_asignaturas, observaciones_mensajes = api.observaciones()
        tree = builder.get_object("observaciones_treeview")
        store = builder.get_object("observaciones_store")
        # Necesario para que no se reincluye al volver a entrar
        store.clear()
        for i in range(0, len(observaciones_asignaturas)):
            store.append([observaciones_asignaturas[i],observaciones_mensajes[i]])

        if not tree.get_columns():
            columns = [
                "Asignatura",
                "Mensaje"
                ]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
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

# Start GTK builder
builder = Gtk.Builder()
builder.add_from_file("assets/glade/openpasen.glade")
builder.connect_signals(Handler())

if (start == "main_menu"):
    api.checksession()
    global user
    user = api.userinfo() # Consigue la información básica del usuario
    # Establece imagen del usuario, quizás hay una mejor forma de hacer esto
    builder.get_object("bienvenido_img").set_from_file(f'{common.config_path}imagen.png')

builder.get_object(str(start)).show()
Gtk.main()
