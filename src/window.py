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

#Import nescessary libraries and modules
#from gettext import gettext as _
from gi.repository import Gdk, Gio, Gtk, Handy, GObject, WebKit2
from os import path, makedirs
import locale
import json
from urllib.request import urlretrieve

#Init Webkit and Handy libs
Handy.init()
WebKit2.WebView()

locale.bindtextdomain('fontdownloader', path.join(path.dirname(__file__).split('fontdownloader')[0],'locale'))
locale.textdomain('fontdownloader')
#Try to update webfonts, otherwise pass
try:
    urlretrieve('https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyA2dEVFiF8o1q8JnSGCsq1reUAbzZR6z0I', 'webfonts.json')
except:
    pass

webfontsData = json.load(open("webfonts.json", 'r'))

#Here we import the font-box template which is used for the fonts' boxes
@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/font-box.ui')
class FontBox(Gtk.Box):
    __gtype_name__ = 'FontBox'

    fontFamily = Gtk.Template.Child()
    fontCategory = Gtk.Template.Child()

    def __init__(self, familyName, category, index, variants, subset, **kwargs):
        super().__init__(**kwargs)
        #When creating, add all information on a data variable
        self.data = [familyName, category, variants, subset]
        #Set labels' texts
        self.fontFamily.set_text(familyName)
        self.fontCategory.set_text(category)

#Here we import the main window template
@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/window.ui')
class FontdownloaderWindow(Handy.Window):
    __gtype_name__ = 'FontdownloaderWindow'

    #And here we import everything, basically
    back_button = Gtk.Template.Child()
    main_download_button = Gtk.Template.Child()
    main_install_button = Gtk.Template.Child()
    search_button = Gtk.Template.Child()
    all_check = Gtk.Template.Child()
    serif_check = Gtk.Template.Child()
    sans_check = Gtk.Template.Child()
    display_check = Gtk.Template.Child()
    handwriting_check = Gtk.Template.Child()
    mono_check = Gtk.Template.Child()
    fonts_list = Gtk.Template.Child()
    search_entry = Gtk.Template.Child()
    search_bar = Gtk.Template.Child()
    text_entry = Gtk.Template.Child()
    font_preview = Gtk.Template.Child()
    leaflet = Gtk.Template.Child()
    box1 = Gtk.Template.Child()
    box2 = Gtk.Template.Child()
    about_button = Gtk.Template.Child()
    headerbar1 = Gtk.Template.Child()
    headerbar2 = Gtk.Template.Child()

    #On initalization do:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Create a box for each font
        for i in range(len(webfontsData['items'])):
            self.newBox = FontBox(webfontsData['items'][i]['family'],
                                  webfontsData['items'][i]['category'],
                                  i,webfontsData['items'][i]['variants'],
                                  webfontsData['items'][i]['subsets'])
            #Make it visible and append it to our fonts panel
            self.newBox.set_visible(True)
            self.fonts_list.add(self.newBox)
        #Select the first row and show all rows
        self.fonts_list.select_row(self.fonts_list.get_row_at_index(0))
        self.fonts_list.show()

        #Creates temporary variables for our window
        self.CurrentSelectedFont = ''
        self.CurrentText = 'The quick brown fox jumps over the lazy dog.'
        self.CurrentFilters = {
            'serif': self.serif_check.get_active(),
            'sans-serif': self.sans_check.get_active(),
            'display': self.display_check.get_active(),
            'handwriting': self.handwriting_check.get_active(),
            'monospace': self.mono_check.get_active()
        }

        #Connect buttons, clicks, key presses to their functions
        self.fonts_list.connect('row-activated', self.fontChanged)
        self.text_entry.connect('changed', self.fontChanged)
        self.back_button.connect('clicked', self.bringListForward)
        self.main_download_button.connect('clicked', self.downloadFont)
        self.main_install_button.connect('clicked', self.installFont)
        self.search_button.connect('toggled', self.toggleSearch)
        self.all_check.connect('toggled', self.checkAllFilters)
        self.serif_check.connect('toggled', self.updateFilter)
        self.sans_check.connect('toggled', self.updateFilter)
        self.display_check.connect('toggled', self.updateFilter)
        self.handwriting_check.connect('toggled', self.updateFilter)
        self.mono_check.connect('toggled', self.updateFilter)
        self.search_entry.connect('changed', self.updateFilter)
        self.about_button.connect("clicked", self.on_about)

        #Calls fontChanged function to update first view
        self.fontChanged()

        #Sets up borders
        self.setup_css();


    #About dialog, courtesy of GeorgesStavracas
    def on_about(self, *args, **kwargs):
        authors = ['Gustavo Machado Peredo', 'Georges Basile Stavracas Neto']
        translators = ['Gustavo Machado Peredo', 'Victor Ibragimov']
        dialog = Gtk.AboutDialog(transient_for=self, modal=True)
        dialog.props.authors = authors
        dialog.add_credit_section(_("Translators"), translators)
        dialog.props.copyright = 'Copyright \xa9 2020 Gustavo Peredo'
        dialog.props.license_type = Gtk.License.GPL_3_0
        dialog.props.logo_icon_name = 'org.gustavoperedo.FontDownloader'
        dialog.props.program_name = _('Font Downloader')

        dialog.present()


    def setup_css(self, *args, **kwargs):
        #Setup the CSS and load it.
        uri = 'resource:///org/gustavoperedo/FontDownloader/style.css'
        provider_file = Gio.File.new_for_uri(uri)

        provider = Gtk.CssProvider()
        provider.load_from_file(provider_file)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def installFont(self, *args, **kwargs):
        #This function gets the selected font's link and downloads
        #to the '.local/share/fonts' directory
        links = webfontsData['items'][self.fonts_list.get_selected_row().get_index()]['files']
        absolutePath = path.join(path.expanduser('~'), '.local/share/fonts')
        if not path.exists(absolutePath):
            makedirs(absolutePath)
        for key in links:
           urlretrieve(links[key], path.join(absolutePath,
                        self.CurrentSelectedFont + " " + key + links[key][-4:]))

    def downloadFont(self, *args, **kwargs):
        #This function gets the selected font's link and downloads
        #to the user's download directory
        links = webfontsData['items'][self.fonts_list.get_selected_row().get_index()]['files']
        absolutePath = path.join(path.expanduser('~'), 'Downloads')
        if not path.exists(absolutePath):
            makedirs(absolutePath)
        for key in links:
           urlretrieve(links[key], path.join(absolutePath,
                        self.CurrentSelectedFont + " " + key + links[key][-4:]))

    def checkAllFilters(self, *args, **kwargs):
        #If the user select "All" on filters, check all
        isAll = self.all_check.get_active()
        self.serif_check.set_active(isAll)
        self.sans_check.set_active(isAll)
        self.display_check.set_active(isAll)
        self.handwriting_check.set_active(isAll)
        self.mono_check.set_active(isAll)
        self.updateFilter()

    def updateFilter(self, *args, **kwargs):
        #Updates the fonts list's filter
        self.fonts_list.set_filter_func(self.filterFonts, None, True)

    def filterFonts(self, row, data, notifyDestroy):
        #Where the actual filter happens, if it returns True, the row appears
        #otherwise disappears
        self.CurrentFilters = {
            'serif': self.serif_check.get_active(),
            'sans-serif': self.sans_check.get_active(),
            'display': self.display_check.get_active(),
            'handwriting': self.handwriting_check.get_active(),
            'monospace': self.mono_check.get_active()
        }

        filtered = [filters for filters in self.CurrentFilters if self.CurrentFilters[filters]]
        searchBarText = self.search_entry.get_text().lower()
        return ((searchBarText == row.get_child().data[0][:len(searchBarText)].lower()) and (row.get_child().data[1] in filtered))

    def fontChanged(self, *args, **kwargs):
        #Whenever the user does something that should change the font preview:
        #We colect the data from the selected font
        self.temp_data = self.fonts_list.get_selected_row().get_child().data
        #The variable CurrentSelectedFont carries the font name
        self.CurrentSelectedFont = self.temp_data[0]
        #Get the text from the text entry
        self.CurrentText = self.text_entry.get_text()
        if self.CurrentText == "":
            self.CurrentText = "The quick brown fox jumps over the lazy dog."
        #Creates a html file with everything (font and text, basically) :P
        self.html ="""
        <!DOCTYPE html>
        <html>
	        <style>
	        body {
	            overflow-wrap: break-word;
	            background-color: white;
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

        #Load the html, set title and subtitle
        self.font_preview.load_html(self.html)
        self.headerbar2.set_title(self.CurrentSelectedFont)
        self.headerbar2.set_subtitle(self.temp_data[1])

        #If the screen is too small, change to font preview pane and show
        #the return button, otherwise, do the opposite
        if self.leaflet.get_folded():
            self.back_button.show()
            self.main_download_button.set_label('')
            self.leaflet.set_visible_child(self.box2)
        else:
            self.bringListForward()

    #Turns search on or off
    def toggleSearch(self, *args, **kwargs):
        self.search_bar.set_search_mode(not self.search_bar.get_search_mode())

    #If the user press back_button, return focus to list view
    def bringListForward(self, *args, **kwargs):
        self.leaflet.set_visible_child(self.box1)
        self.main_download_button.set_label(_('Download'))
        self.back_button.hide()
