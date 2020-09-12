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

from gi.repository import Gtk, Handy, GObject, WebKit2
import json

WebKit2.WebView()

"Update webfonts.json"

from urllib.request import urlretrieve
urlretrieve('https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyA2dEVFiF8o1q8JnSGCsq1reUAbzZR6z0I', 'webfonts.json')
webfontsData = json.load(open("webfonts.json", 'r'))



@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/font-box.ui')
class FontBox(Gtk.Frame):
    __gtype_name__ = 'FontBox'

    fontFamily = Gtk.Template.Child()
    fontCategory = Gtk.Template.Child()

    def __init__(self, familyName, category, **kwargs):
        super().__init__(**kwargs)
        self.fontFamily.set_text(familyName)
        self.fontCategory.set_text(category)

@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/font-list-pane.ui')
class FontListPane(Gtk.Frame):
    __gtype_name__ = 'FontsListPane'

    fontsListBox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for i in range(25):
            self.newBox = FontBox(webfontsData['items'][i]['family'],webfontsData['items'][i]['category'])
            self.newBox.set_visible(True)
            self.fontsListBox.add(self.newBox)

        self.fontsListBox.show()

@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/fontpreview.ui')
class FontPreviewPane(Gtk.Frame):
    __gtype_name__ = 'FontPreviewPane'

    fontPreview = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fontPreview.show()

GObject.type_ensure(Handy.TitleBar)
@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/window.ui')
class FontdownloaderWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'FontdownloaderWindow'

    list_pane_stack = Gtk.Template.Child()
    fontpreview_pane = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.FontsList = FontListPane()
        self.FontPreview = FontPreviewPane()

        self.FontsList.set_visible(True)

        self.list_pane_stack.add_named(self.FontsList, 'Font List Pane')

        self.list_pane_stack.set_visible_child_name('Font List Pane')

        self.list_pane_stack.show()

        self.fontpreview_pane.add(self.FontPreview)

        self.fontpreview_pane.show()



        
