# main.py
#
# Copyright 2020 GustavoPeredo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
gi.require_version('WebKit2', '4.0')
gi.require_version('Pango', '1.0')

from gi.repository import Gtk, Gio, Handy
if os.environ['XDG_SESSION_TYPE'].lower() == "wayland":
    from .window import FontdownloaderWindow
else:
    from .windowX11 import FontdownloaderWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.gustavoperedo.FontDownloader',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = FontdownloaderWindow(application=self)
        win.present()


def main(version):
    app = Application()
    return app.run(sys.argv)
