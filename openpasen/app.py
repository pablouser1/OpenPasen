import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from openpasen.common import user
from openpasen.gui.signals import GuiSignals
from openpasen.api.auth import Auth

class App:
    builder = Gtk.Builder()

    def start(self):
        print("Inciando GUI")
        first_menu = "login_menu"
        loggedIn = Auth.checkSession()
        if loggedIn:
            user.getUser()
            first_menu = "main_menu"
        self.builder.add_from_file("assets/templates/glade/openpasen.glade")
        # Main signals
        self.builder.connect_signals(GuiSignals(self.builder, Gtk.main_quit))
        self.builder.get_object(first_menu).show()
        Gtk.main()
