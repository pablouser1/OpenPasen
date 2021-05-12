#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from openpasen.api.user import PasenAPI
from openpasen.common import user, config

class GuiSignals:
    # Init
    def __init__(self, builder, main_quit):
        self.builder = builder
        self.onDestroy = main_quit

    def deleteEvent(self, widget, event):
        widget.hide()
        return True

    # --------- Botones --------- #
    # Botón login pulsado
    def on_login_clicked(self, button):
        username = self.builder.get_object("username").get_text()
        password = self.builder.get_object("password").get_text()
        remember = self.builder.get_object('sesioniniciada').get_active()

        res = PasenAPI.login(username, password)
        if res:
            if remember:
                config.saveLogin(username, password)
            if user.getUser():
                self.builder.get_object("login_menu").hide()
                self.builder.get_object("main_menu").show()

    # -- Main menu -- #
    def on_main_menu_show(self, *args):
        self.builder.get_object("bienvenido_label").set_text(f'Bienvenido, {user.nombre}')

    # Notas
    def on_notas_clicked(self, button):
        # Por algún motivo, esto es necesario para que al cerrar y volver a abrir se pueda ver el treeview
        notas_menu = self.builder.get_object("notas_menu")
        dropdown = self.builder.get_object("notas_dropdown")
        treeview = self.builder.get_object("notas_treeview")
        convcentro = PasenAPI.convocatorias(user.id)

        dropdown.remove_all()
        active = None
        for conv in convcentro:
            if 'S' in conv["active"]:
                active = conv["id"]
            dropdown.append(str(conv["id"]), conv["name"])

        # Generate columns
        if not treeview.get_columns():
            columns = ["Asignatura", "Nota"]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                treeview.append_column(col)

        if active:
            dropdown.set_active_id(str(active))

        notas_menu.show()

    def on_notas_dropdown_changed(self, dropdown):
        store = self.builder.get_object("notas_store")
        conv = dropdown.get_active_id()
        notas = PasenAPI.notas(user.id, conv)
        self.builder.get_object("notas_media").set_text("")
        store.clear()
        if notas:
            total = 0
            # Append to store and get median
            for nota in notas:
                total += int(nota["nota"])
                store.append([nota["nombre"], nota["nota"]])
            media = total / len(notas)
            self.builder.get_object("notas_media").set_text(f'Tu nota media es de: {str(media)}')

    def on_actividades_clicked(self, button):
        actividades_menu = self.builder.get_object("actividades_menu")
        treeview = self.builder.get_object("actividades_treeview")
        asignaturas_dropdown = self.builder.get_object("actividades_asignaturas_dropdown")
        evaluaciones_dropdown = self.builder.get_object("actividades_evaluaciones_dropdown")
        asignaturas = PasenAPI.asignaturas(user.id)
        convcentro = PasenAPI.convocatorias(user.id)

        asignaturas_dropdown.remove_all()
        evaluaciones_dropdown.remove_all()

        asignaturas_dropdown.append("0", "Todas")
        asignaturas_dropdown.set_active_id("0")
        for asignatura in asignaturas:
            asignaturas_dropdown.append(str(asignatura["id"]), asignatura["name"])

        conv_active = None
        for conv in convcentro:
            if 'S' in conv["active"]:
                conv_active = conv["id"]
            evaluaciones_dropdown.append(str(conv["id"]), conv["name"])

        if not treeview.get_columns():
            columns = ["Tema", "Nota"]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                treeview.append_column(col)

        if conv_active:
            evaluaciones_dropdown.set_active_id(str(conv_active))

        actividades_menu.show()

    def on_actividades_dropdown_changed(self, *args):
        asignatura = self.builder.get_object("actividades_asignaturas_dropdown").get_active_id()
        evaluacion = self.builder.get_object("actividades_evaluaciones_dropdown").get_active_id()
        if asignatura and evaluacion:
            store = self.builder.get_object("actividades_store")
            store.clear()
            if asignatura == "0":
                asignatura = None
            actividades = PasenAPI.actividades(user.id, evaluacion, asignatura)
            if actividades:
                for actividad in actividades:
                    store.append([actividad["nombre"], actividad["nota"]])

    def on_horario_clicked(self, button):
        treeview = self.builder.get_object("horario_treeview")
        horario_menu = self.builder.get_object("horario_menu")
        store = self.builder.get_object("horario_store")
        store.clear()
        horario = PasenAPI.horario(user.id)
        for i in range(0, 6):
            store.append(
                [
                    horario["Lunes"][i]["nombre"],
                    horario["Martes"][i]["nombre"],
                    horario["Miercoles"][i]["nombre"],
                    horario["Jueves"][i]["nombre"],
                    horario["Viernes"][i]["nombre"]
                ]
            )

        if not treeview.get_columns():
            columns = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                treeview.append_column(col)
        horario_menu.show()
    # -- Header menú principal -- #
    # Acerca de
    def on_acercade_activate(self, button):
        self.builder.get_object("about").show()

    # Perfil
    def on_perfil_activate(self, button):
        self.builder.get_object("curso_label").set_markup(user.curso)
        self.builder.get_object("unidad_label").set_markup(user.unidad)
        self.builder.get_object("centro_label").set_markup(user.centro["nombre"])
        self.builder.get_object("tutor_label").set_markup(user.tutor)
        self.builder.get_object("perfil_menu").show()

    # Mi centro
    def on_centro_activate(self, button):
        centro = PasenAPI.centro(user.centro["id"])
        print(centro)
        print("WIP")

    # -- Comunicaciones -- #
    def on_comunicaciones_activate(self, button):
        print("WIP")

    def on_reporte_activate(self, button):
        self.builder.get_object("reporte_menu").show()

    def on_reporte_continuar_clicked(self,button):
        """
        seleccion = self.builder.get_object("reporte_evaluaciones").get_active_text()
        out = reporte.generar(seleccion)
        if out not in "ImportError":
            self.builder.get_object("reporte_label").set_markup(f'Se ha generado el reporte en el directorio:\n{out}')
        else:
            self.builder.get_object("reporte_label").set_markup("Ha habido un error al generar el reporte")
        """
        pass
    def on_horario_gen_activate(self, button):
        """
        out = genhorario.generar(user["nombre"], user["unidad"])
        if out not in "ImportError":
            self.builder.get_object("general_label").set_markup(f'Se ha generado el horario en el directorio:\n{out}')
        else:
            self.builder.get_object("general_label").set_markup("Ha habido un error al generar el reporte")
        """
        pass
    # Cerrar sesión
    def on_cerrarsesion_activate(self,button):
        self.builder.get_object('main_menu').hide()
        self.builder.get_object('login_menu').show()
