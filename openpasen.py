#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import common
import api
import reporte
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from notebook import Notebook as main_notebook

class Handler:
    # Init
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
    def on_main_menu_show(self, *args):
        builder.get_object("bienvenido_label").set_text(f'Bienvenido, {user["nombre"]}')

    # Notebook, parte principal del programa
    # A partir del id ejecuta distintas funciones
    def on_main_notebook_switch_page(self,notebook, page, page_num):
        # Actividades evaluables
        if (page_num == 1):
            main_notebook.actividades(self, builder)
        # Observaciones
        elif(page_num == 2):
            main_notebook.observaciones(self, builder)
        # Faltas
        elif(page_num == 3):
            main_notebook.faltas(self, builder)
        # Conductas
        elif(page_num == 4):
            main_notebook.conductas(self, builder)
        # Horario
        elif(page_num == 5):
            main_notebook.horario(self, builder)
        # Avisos
        elif(page_num == 6):
            main_notebook.avisos(self, builder)
        else:
            pass

    # Notas
    def on_continuar_notas_boton_clicked(self, button):
        # Por algún motivo, esto es necesario para que al cerrar y volver a abrir se pueda ver el treeview
        notas_menu = builder.get_object("notas_evaluacion_menu")
        notas_box = builder.get_object("notas_box")
        notas_box.get_parent().remove(notas_box)
        notas_menu.add(notas_box)

        notas_evaluacion = builder.get_object("notascombo").get_active_text()
        convcentro = api.convcentro(notas_evaluacion)
        # Asignaturas_list tiene los nombres de las asignaturas mientras que notas_numero_list tiene la nota numérica.
        notas = api.getNotas(convcentro, notas_evaluacion)
        # Si no hay notas disponibles, avisar y no continuar, ya que tendríamos una ZeroDivisionError
        if (notas["notas_num"] == []):
            builder.get_object("notas_info").set_markup(f'{notas_evaluacion} no tiene notas disponibles')
        else:
            tree = builder.get_object("notas_treeview")
            store = builder.get_object("notas_store")
            store.clear()
            for i in range(0, len(notas["asignaturas"])):
                store.append([notas["asignaturas"][i], notas["notas_num"][i]])
            # Crear columnas si no existen
            if not tree.get_columns():
                columns = ["Asignatura", "Nota"]
                cell = Gtk.CellRendererText()
                for i, column in enumerate(columns):
                    col = Gtk.TreeViewColumn(column, cell, text=i)
                    tree.append_column(col)
            # Nota media
            media_final = sum(int (i) for i in notas["notas_num"]) / len(notas["notas_num"])
            builder.get_object("notas_media").set_markup(f'Tu nota media es de {str(round(media_final, 2))}')
            notas_menu.show()

    def on_actividades_continuar_clicked(self, button):
        # TODO, optimizar
        # Por algún motivo, esto es necesario para que al cerrar y volver a abrir se pueda ver el treeview
        actividades_menu = builder.get_object("act_eval_menu")
        actividades_box = builder.get_object("actividades_box")
        actividades_box.get_parent().remove(actividades_box)
        actividades_menu.add(actividades_box)

        actividades_asignatura = builder.get_object("actividades_asignaturas").get_active_text()
        actividades_evaluacion = builder.get_object("actividades_evaluaciones").get_active_text()
        convcentro = api.convcentro(actividades_evaluacion)
        acteval = api.actividadesevaluables(convcentro, actividades_asignatura)

        tree = builder.get_object("actividades_treeview")
        store = builder.get_object("actividades_store")
        store.clear()
        for i in range(0, len(acteval["tema"])):
            store.append([acteval["tema"][i], acteval["nota"][i]])
        # Crear columnas si no existen
        if not tree.get_columns():
            print("Creando columnas...")
            columns = ["Tema", "Nota"]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                tree.append_column(col)
        
        builder.get_object("actividades_label").set_markup(f'{actividades_asignatura} - {actividades_evaluacion}')
        builder.get_object("act_eval_menu").show()

    # -- Header menú principal -- #
    # Acerca de
    def on_acercade_activate(self, button):
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
    
    def on_reporte_activate(self, button):
        builder.get_object("reporte_menu").show()
    
    def on_reporte_continuar_clicked(self,button):
        seleccion = builder.get_object("reporte_evaluaciones").get_active_text()
        out = reporte.generar(seleccion)
        if out not in "ImportError":
            builder.get_object("reporte_label").set_markup(f'Se ha generado el reporte en el directorio:\n{out}')
        else:
            builder.get_object("reporte_label").set_markup("Ha habido un error al generar el reporte")
    # Cerrar sesión
    def on_cerrarsesion_activate(self,button):
        api.cerrarsesion()
        builder.get_object('main_menu').hide()
        builder.get_object('login_menu').show()


if __name__ == "__main__":
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
