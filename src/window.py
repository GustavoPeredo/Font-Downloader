# window.py
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

from gi.repository import Gtk, Handy, GObject

@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/font-box.ui')
class FontBox(Gtk.Frame):
    __gtype_name__ = 'FontBox'

    fontName = Gtk.Template.Child()
    descriptionName = Gtk.Template.Child()

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.fontName.set_text(text)

@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/font-list-pane.ui')
class FontListPane(Gtk.Frame):
    __gtype_name__ = 'FontsListPane'

    fontsListBox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(10):
            self.newBox = FontBox(str(i))
            self.newBox.set_visible(True)
            self.fontsListBox.add(self.newBox)

        self.fontsListBox.show()


GObject.type_ensure(Handy.TitleBar)
@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/window.ui')
class FontdownloaderWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'FontdownloaderWindow'

    list_pane_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.FontsList = FontListPane()

        self.FontsList.set_visible(True)

        self.list_pane_stack.add_named(self.FontsList, 'Font List Pane')

        self.list_pane_stack.set_visible_child_name('Font List Pane')

        print(self.list_pane_stack.get_visible_child_name())

        self.list_pane_stack.show()



        
