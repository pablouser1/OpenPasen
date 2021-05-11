from gi.repository import Gtk
from openpasen.api.user import PasenAPI
from openpasen.common import user, config

class GuiSignals:
    # Init
    def __init__(self, builder, main_quit):
        self.builder = builder
        self.onDestroy = main_quit
        print("GTK Handler Init")
    
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


    # Notebook, parte principal del programa
    # A partir del id ejecuta distintas funciones
    def on_main_notebook_switch_page(self, notebook, page, page_num):
        """
        # Actividades evaluables
        if (page_num == 1):
            main_notebook.actividades(self, self.builder)
        # Observaciones
        elif(page_num == 2):
            main_notebook.observaciones(self, self.builder)
        # Faltas
        elif(page_num == 3):
            main_notebook.faltas(self, self.builder)
        # Conductas
        elif(page_num == 4):
            main_notebook.conductas(self, self.builder)
        # Horario
        elif(page_num == 5):
            main_notebook.horario(self, self.builder)
        else:
            pass
        """
        pass

    # Notas
    def on_notas_clicked(self, button):
        # Por algún motivo, esto es necesario para que al cerrar y volver a abrir se pueda ver el treeview
        notas_menu = self.builder.get_object("notas_menu")
        dropdown = self.builder.get_object("notas_dropdown")
        convcentro = PasenAPI.convocatorias(user.id)

        dropdown.remove_all()
        for conv in convcentro:
            dropdown.append(str(conv["id"]), conv["name"])

        notas_menu.show()
    
    def on_notas_dropdown_changed(self, dropdown):
        notas_treeview = self.builder.get_object("notas_treeview")
        store = self.builder.get_object("notas_store")
        conv = dropdown.get_active_id()
        notas = PasenAPI.notas(user.id, conv)
        store.clear()
        if notas:
            total = 0
            for nota in notas:
                total += int(nota["nota"])
                store.append([nota["nombre"], nota["nota"]])
            media = total / len(notas)
            self.builder.get_object("notas_media").set_text(f'Tu nota media es de: {str(media)}')
            if not notas_treeview.get_columns():
                columns = ["Asignatura", "Nota"]
                cell = Gtk.CellRendererText()
                for i, column in enumerate(columns):
                    col = Gtk.TreeViewColumn(column, cell, text=i)
                    notas_treeview.append_column(col)
    def on_actividades_continuar_clicked(self, button):
        """
        # TODO, optimizar
        # Por algún motivo, esto es necesario para que al cerrar y volver a abrir se pueda ver el treeview
        actividades_menu = self.builder.get_object("act_eval_menu")
        actividades_box = self.builder.get_object("actividades_box")
        actividades_box.get_parent().remove(actividades_box)
        actividades_menu.add(actividades_box)

        actividades_asignatura = self.builder.get_object("actividades_asignaturas").get_active_text()
        actividades_evaluacion = self.builder.get_object("actividades_evaluaciones").get_active_text()
        convcentro = api.convcentro(actividades_evaluacion)
        acteval = api.actividadesevaluables(convcentro, actividades_asignatura)

        tree = self.builder.get_object("actividades_treeview")
        store = self.builder.get_object("actividades_store")
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
        
        self.builder.get_object("actividades_label").set_markup(f'{actividades_asignatura} - {actividades_evaluacion}')
        self.builder.get_object("act_eval_menu").show()
        """
        pass

    # -- Header menú principal -- #
    # Acerca de
    def on_acercade_activate(self, button):
        self.builder.get_object("about").show()

    # Perfil
    def on_perfil_activate(self, button):
        """
        self.builder.get_object("curso_label").set_markup(user.curso)
        self.builder.get_object("unidad_label").set_markup(user.unidad)
        self.builder.get_object("centro_label").set_markup(user["denominacion"])
        self.builder.get_object("tutor_label").set_markup(user["tutor"])
        self.builder.get_object("perfil_menu").show()
        """
        pass

    # Mi centro
    def on_centro_activate(self, button):
        """
        centro = api.centro()
        centro_menu = self.builder.get_object("centro_menu")

        tree = self.builder.get_object("centro_treeview")
        store = self.builder.get_object("centro_store")
        store.clear()
        for info in centro:
            for i in range(0, len(centro[info])):
                store.append([centro[info][i][0], str(centro[info][i][1])])
        # Crear columnas si no existen
        if not tree.get_columns():
            print("Creando columnas...")
            columns = ["Seccion", "Datos"]
            cell = Gtk.CellRendererText()
            for i, column in enumerate(columns):
                col = Gtk.TreeViewColumn(column, cell, text=i)
                tree.append_column(col)
        centro_menu.show()
        """
        pass
    
    # -- Comunicaciones -- #
    def on_comunicaciones_activate(self, button):
        pass

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
