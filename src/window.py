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
from os import path, makedirs
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
    searchBar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for i in range(len(webfontsData['items'])):
            self.newBox = FontBox(webfontsData['items'][i]['family'],webfontsData['items'][i]['category'])
            self.newBox.set_visible(True)
            self.fontsListBox.add(self.newBox)
        self.fontsListBox.select_row(self.fontsListBox.get_row_at_index(0))
        self.fontsListBox.show()

@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/fontpreview.ui')
class FontPreviewPane(Gtk.Frame):
    __gtype_name__ = 'FontPreviewPane'

    fontPreviewWebview = Gtk.Template.Child()
    fontPreviewText = Gtk.Template.Child()

    def __init__(self, **kwargs):
        self.html = ''
        super().__init__(**kwargs)



GObject.type_ensure(Handy.TitleBar)
@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/window.ui')
class FontdownloaderWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'FontdownloaderWindow'

    list_pane_stack = Gtk.Template.Child()
    fontpreview_pane = Gtk.Template.Child()
    back_button = Gtk.Template.Child()
    main_download_button = Gtk.Template.Child()
    compact_download_button = Gtk.Template.Child()
    search_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.CurrentSelectedFont = ''
        self.CurrentText = 'The quick brown fox jumps over the lazy dog.'
        self.CurrentStatus = 'LONG'
        self.CurrentWidth = 0

        self.FontsList = FontListPane()
        self.FontPreview = FontPreviewPane()
        self.FontPreview2 = FontPreviewPane()

        self.FontsList.set_visible(True)
        self.FontPreview.set_visible(True)
        self.FontPreview2.set_visible(True)

        self.list_pane_stack.add_named(self.FontsList, 'Font List Pane')

        self.list_pane_stack.add_named(self.FontPreview2, 'Font Preview Pane')

        self.list_pane_stack.set_visible_child_name('Font List Pane')

        self.fontpreview_pane.add_overlay(self.FontPreview)

        self.FontsList.fontsListBox.connect('row-activated', self.fontChanged)
        self.FontPreview.fontPreviewText.connect('changed', self.fontChanged, 1)
        self.FontPreview2.fontPreviewText.connect('changed', self.fontChanged, 2)
        self.connect('check-resize', self.switchLayouts)
        self.back_button.connect('clicked', self.bringListFoward)
        self.main_download_button.connect('clicked', self.downloadFont)
        self.compact_download_button.connect('clicked', self.downloadFont)
        self.search_button.connect('toggled', self.toggleSearch)

        self.fontpreview_pane.show()
        self.list_pane_stack.show()
        self.back_button.hide()
        self.compact_download_button.hide()

        self.fontChanged(self, 1)

    def downloadFont(self, *args, **kwargs):
        links = webfontsData['items'][self.FontsList.fontsListBox.get_selected_row().get_index()]['files']
        absolutePath = path.join(path.expanduser('~'), '.fonts')
        if not path.exists(absolutePath):
            makedirs(absolutePath)
        for key in links:
           urlretrieve(links[key], path.join(absolutePath, self.CurrentSelectedFont + " " + key + links[key][-4:]))


    def fontChanged(self, widget, which, *args, **kwargs):
        self.CurrentSelectedFont = ((self.FontsList.fontsListBox.get_selected_row()).get_child()).fontFamily.get_text()
        if which == 1:
            self.CurrentText = self.FontPreview.fontPreviewText.get_text()
        else:
            self.CurrentText = self.FontPreview2.fontPreviewText.get_text()
        if self.CurrentText == "":
            self.CurrentText = "The quick brown fox jumps over the lazy dog."

        self.FontPreview.html ="""
        <!DOCTYPE html>
        <html>
	        <style>
	        body {
	            overflow-wrap: break-word;
	            background-color: #F6F5F4;
	            font-family: '""" + self.CurrentSelectedFont + """';
	        }
	        @media(prefers-color-scheme: dark) {
	            body {
	                background-color: #353535;
	                color: #ffffff;
	            }
	        }
	        </style>
	        <link href="https://fonts.googleapis.com/css2?family=""" + self.CurrentSelectedFont.replace(' ','+') + """&display=swap" rel="stylesheet">
            <body>
                <h1> """ + self.CurrentText +  """ </h1>
                <h2> """ + self.CurrentText +  """ </h2>
                <h3> """ + self.CurrentText +  """ </h3>
                <h4> """ + self.CurrentText +  """ </h4>
                <p> """ + self.CurrentText +  """ </p>
            </body>
        </html>
        """

        self.FontPreview.fontPreviewWebview.load_html(self.FontPreview.html)
        self.FontPreview2.fontPreviewWebview.load_html(self.FontPreview.html)

        if self.CurrentStatus == 'COMPACT':
            self.compact_download_button.show()
            self.list_pane_stack.set_transition_type(Gtk.StackTransitionType.OVER_LEFT)
            self.list_pane_stack.set_visible_child_name('Font Preview Pane')
            self.back_button.show()
        else:
            self.compact_download_button.hide()

    def toggleSearch(self, *args, **kwargs):
        self.FontsList.searchBar.set_search_mode(not self.FontsList.searchBar.get_search_mode())

    def bringListFoward(self, *args, **kwargs):
        self.list_pane_stack.set_transition_type(Gtk.StackTransitionType.UNDER_RIGHT)
        self.list_pane_stack.set_visible_child_name('Font List Pane')
        self.back_button.hide()
        self.compact_download_button.hide()

    def switchLayouts(self, *args, **kwargs):
        self.CurrentWidth = self.get_size()[0]
        if (self.CurrentWidth <= 434) and (self.CurrentStatus == 'LONG'):
            self.list_pane_stack.set_transition_type(Gtk.StackTransitionType.OVER_LEFT)
            self.list_pane_stack.set_visible_child_name('Font Preview Pane')
            self.back_button.show()
            self.compact_download_button.show()
            self.CurrentStatus = 'COMPACT'
        elif (self.CurrentWidth > 434) and (self.CurrentStatus == 'COMPACT'):
            self.list_pane_stack.set_transition_type(Gtk.StackTransitionType.UNDER_RIGHT)
            self.list_pane_stack.set_visible_child_name('Font List Pane')
            self.back_button.hide()
            self.compact_download_button.hide()
            self.CurrentStatus = 'LONG'




        
