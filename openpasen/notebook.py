#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Funciones que afentan a los widgets dentro del Notebook del main menu
from openpasen import api
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
class Notebook:
    # Actividades evaluables
    def actividades(self, builder):
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

    # Observaciones del alumnado
    def observaciones(self, builder):
        observaciones = api.observaciones()
        tree = builder.get_object("observaciones_treeview")
        store = builder.get_object("observaciones_store")
        # Necesario para que no se reincluye al volver a entrar
        store.clear()
        for i in range(0, len(observaciones["Asignaturas"])):
            store.append([observaciones["Asignaturas"][i], observaciones["Mensajes"][i], observaciones["Fechas"][i]])

        if not tree.get_columns():
            columns = ["Asignatura", "Mensaje", "Fecha"]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                tree.append_column(col)

    def faltas(self, builder):
        tree = builder.get_object("faltas_treeview")
        store = builder.get_object("faltas_store")
        store.clear()
        faltas = api.faltas()
        for i in range(0, len(faltas["Asignaturas"])):
            store.append([faltas["Asignaturas"][i], faltas["Fechas y Horas"][i], faltas["Justificada"][i]])

        if not tree.get_columns():
            columns = ["Asignaturas", "Fecha/Hora", "Justificada"]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                tree.append_column(col)

    def conductas(self, builder):
        conductas = api.conductas()
        if (conductas.text == '{"ESTADO":{"CODIGO":"C"},"RESULTADO":[]}'):
            builder.get_object("label_conductas").set_markup("No tienes ninguna conducta contraria")
        else:
            builder.get_object("label_conductas").set_markup("WIP")
        # TODO, completar

    def horario(self, builder):
        tree = builder.get_object("horario_treeview")
        store = builder.get_object("horario_store")
        store.clear()
        horario_dict = api.horario()
        for i in range(0, 6):
            store.append([horario_dict["Lunes"][i], horario_dict["Martes"][i], horario_dict["Miercoles"][i], horario_dict["Jueves"][i], horario_dict["Viernes"][i]])

        if not tree.get_columns():
            columns = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                tree.append_column(col)
