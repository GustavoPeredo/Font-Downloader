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
from os import path, makedirs, listdir
import locale
import json
from urllib.request import urlretrieve

#Init Webkit and Handy libs
Handy.init()

locale.bindtextdomain('fontdownloader', path.join(path.dirname(__file__).split('fontdownloader')[0],'locale'))
locale.textdomain('fontdownloader')
webfontsData = json.load(open(path.join(path.dirname(__file__).split('fontdownloader')[0],'fontdownloader/fontdownloader/webfonts.json'), 'r'))

#Here we import the font-box template which is used for the fonts' boxes
@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/font-box.ui')
class FontBox(Gtk.Box):
    __gtype_name__ = 'FontBox'

    fontFamily = Gtk.Template.Child()
    fontCategory = Gtk.Template.Child()
    installed_box = Gtk.Template.Child()

    def __init__(self, familyName, category, index, variants, subset, **kwargs):
        super().__init__(**kwargs)
        #When creating, add all information on a data variable
        self.data = [familyName, category, variants, subset]
        #Set labels' texts
        self.fontFamily.set_text(familyName)
        #Change category to it's translation

        self.fontCategory.set_text(_('sans-serif') if category=='sans-serif' else (_('serif') if category=='serif' else (_('display') if category=='display' else (_('monospaced') if category=='monospace' else _('handwriting')))))


#Here we import the main window template
@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/window.ui')
class FontdownloaderWindow(Handy.Window):
    __gtype_name__ = 'FontdownloaderWindow'
    #Get settings schema
    settings = Gio.Settings.new('org.gustavoperedo.FontDownloader')

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
    light_mode_button = Gtk.Template.Child()
    dark_mode_button = Gtk.Template.Child()
    settings_button = Gtk.Template.Child()
    SettingsWindow = Gtk.Template.Child()
    close_settings_button = Gtk.Template.Child()
    folder_settings_button = Gtk.Template.Child()
    arabic_button = Gtk.Template.Child()
    bengali_button = Gtk.Template.Child()
    chinese_hk_button = Gtk.Template.Child()
    chinese_SIMP_button = Gtk.Template.Child()
    chinese_trad_button = Gtk.Template.Child()
    cyrillic_button = Gtk.Template.Child()
    cyrillic_ext_button = Gtk.Template.Child()
    devanagari_button = Gtk.Template.Child()
    greek_button = Gtk.Template.Child()
    greek_ext_button = Gtk.Template.Child()
    gujarati_button = Gtk.Template.Child()
    gurmukhi_button = Gtk.Template.Child()
    hebrew_button = Gtk.Template.Child()
    japanese_button = Gtk.Template.Child()
    kannada_button = Gtk.Template.Child()
    khmer_button = Gtk.Template.Child()
    korean_button = Gtk.Template.Child()
    latin_button = Gtk.Template.Child()
    latin_ext_button = Gtk.Template.Child()
    malayalam_button = Gtk.Template.Child()
    myanmar_button = Gtk.Template.Child()
    oriya_button = Gtk.Template.Child()
    sinhala_button = Gtk.Template.Child()
    tamil_button = Gtk.Template.Child()
    telugu_button = Gtk.Template.Child()
    thai_button = Gtk.Template.Child()
    tibetan_button = Gtk.Template.Child()
    vietnamese_button = Gtk.Template.Child()
    any_alphabet_button = Gtk.Template.Child()
    reset_button = Gtk.Template.Child()
    header_group = Gtk.Template.Child()

    WebKit2.WebView()
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
        self.light_mode_button.connect('clicked', self.changeTheme)
        self.dark_mode_button.connect('clicked', self.changeTheme)
        self.settings_button.connect('clicked', self.presentSettings)
        self.close_settings_button.connect('clicked', self.closeSettings)
        self.folder_settings_button.connect('clicked', self.on_open)
        self.any_alphabet_button.connect('clicked', self.anyAlphabet)
        self.reset_button.connect('clicked', self.reset)
        self.header_group.connect('update-decoration-layouts', self.updateSize)

        self.alphabet_buttons = [self.arabic_button, self.bengali_button,
        self.chinese_hk_button, self.chinese_SIMP_button,
        self.chinese_trad_button, self.cyrillic_button,
        self.cyrillic_ext_button, self.devanagari_button,
        self.greek_button, self.greek_ext_button, self.gujarati_button,
        self.gurmukhi_button, self.hebrew_button, self.japanese_button,
        self.kannada_button, self.khmer_button, self.korean_button,
        self.latin_button, self.latin_ext_button,
        self.malayalam_button, self.myanmar_button, self.oriya_button,
        self.sinhala_button, self.tamil_button, self.telugu_button,
        self.thai_button, self.tibetan_button, self.vietnamese_button]

        self.alphabet_list = ['arabic', 'bengali', 'chinese-hongkong',
        'chinese-simplified', 'chinese-traditional', 'cyrillic',
        'cyrillic-ext', 'devanagari', 'greek', 'greek-ext', 'gujarati',
        'gurmukhi', 'hebrew', 'japanese', 'kannada', 'khmer', 'korean',
        'latin', 'latin-ext', 'malayalam', 'myanmar', 'oriya', 'sinhala',
        'tamil', 'telugu', 'thai', 'tibetan', 'vietnamese']

        self.current_alphabet_list = self.settings.get_string('current-alphabet').split(';')
        self.any_alphabet_button.set_active(self.settings.get_boolean('any-alphabet'))
        self.any_alphabet = self.any_alphabet_button.get_active()

        for i in range(len(self.alphabet_list)):
            if self.alphabet_list[i] in self.current_alphabet_list:
                self.alphabet_buttons[i].set_active(True)
            else:
                self.alphabet_buttons[i].set_active(False)

        self.anyAlphabet()
        self.folder_settings_button.set_label(_('Default') if self.settings.get_string('default-directory')=='Default' else self.settings.get_string('default-directory'))

        for buttons in self.alphabet_buttons:
            buttons.connect("toggled", self.updateAlphabet)

        #Calls fontChanged function to update first view
        self.fontChanged()

        self.dark_mode_button.set_active(self.settings.get_boolean('dark-mode'))
        self.changeTheme()

        #Sets up borders
        self.setup_css();

        self.checkForInstalledFonts()

    @property
    def folded(self):
        self.fontChanged()

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
        absolutePath = path.join(path.expanduser('~'), '.local/share/fonts') if self.settings.get_string('default-directory') == 'Default' else self.settings.get_string('default-directory')
        if not path.exists(absolutePath):
            makedirs(absolutePath)
        for key in links:
           urlretrieve(links[key], path.join(absolutePath,
                        self.CurrentSelectedFont + " " + key + links[key][-4:]))
        self.checkForInstalledFonts()

    def downloadFont(self, *args, **kwargs):
        #This function gets the selected font's link and downloads
        #to the user's download directory
        links = webfontsData['items'][self.fonts_list.get_selected_row().get_index()]['files']

        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            absolutePath = dialog.get_filename()
            if not path.exists(absolutePath):
                makedirs(absolutePath)
            for key in links:
               urlretrieve(links[key], path.join(absolutePath,
                            self.CurrentSelectedFont + " " + key + links[key][-4:]))

        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

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
        if not self.any_alphabet:
            if any(i in self.current_alphabet_list for i in row.get_child().data[3]):
                return ((searchBarText == row.get_child().data[0][:len(searchBarText)].lower()) and (row.get_child().data[1] in filtered))
            else:
                return False
        else:
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
        self.headerbar2.set_subtitle(_('sans-serif') if self.temp_data[1]=='sans-serif' else (_('serif') if self.temp_data[1]=='serif' else (_('display') if self.temp_data[1]=='display' else (_('monospaced') if self.temp_data[1]=='monospaced' else _('handwriting')))))
        self.leaflet.set_visible_child(self.box2)


    def updateSize(self, *args, **kwargs):
        #If the screen is too small, change to font preview pane and show
        #the return button, otherwise, do the opposite
        if self.leaflet.get_folded():
            self.back_button.show()
            self.main_download_button.set_label('')
            #self.leaflet.set_visible_child(self.box2)
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

    def changeTheme(self, *args, **kwargs):
        if self.dark_mode_button.get_active():
            Gtk.Settings.get_default().set_property('gtk-application-prefer-dark-theme', True)
            self.settings.set_boolean('dark-mode', True)
        else:
            Gtk.Settings.get_default().set_property('gtk-application-prefer-dark-theme', False)
            self.settings.set_boolean('dark-mode', False)

    def presentSettings(self, *args, **kwargs):
        self.SettingsWindow.show()

    def closeSettings(self, *args, **kwargs):
        self.SettingsWindow.hide()

    def on_open(self, event):
        dialog = Gtk.FileChooserDialog(_("Please choose a folder"), self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            self.folder_settings_button.set_label(file_path)
            self.settings.set_string('default-directory', file_path)
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def updateAlphabet(self, *args, **kwargs):
        self.current_alphabet_list = []
        for i in range(len(self.alphabet_list)):
            if self.any_alphabet:
                self.alphabet_buttons[i].set_active(self.any_alphabet)
            elif self.alphabet_buttons[i].get_active():
                self.current_alphabet_list.append(self.alphabet_list[i])
        self.settings.set_string('current-alphabet', ';'.join(self.current_alphabet_list))
        self.updateFilter()

    def anyAlphabet(self, *args, **kwargs):
        self.any_alphabet = self.any_alphabet_button.get_active()
        if self.any_alphabet:
            for i in range(len(self.alphabet_list)):
                self.alphabet_buttons[i].set_active(self.any_alphabet)
        self.settings.set_boolean('any-alphabet', self.any_alphabet)
        self.updateAlphabet()

    def reset(self, *args, **kwargs):
        self.settings.set_string('default-directory', 'Default')
        self.folder_settings_button.set_label('Default')
        self.any_alphabet_button.set_active(True)
        self.updateAlphabet()

    def checkForInstalledFonts(self, *args, **kwargs):
        defaultPath = path.join(path.expanduser('~'), '.local/share/fonts') if self.settings.get_string('default-directory') == 'Default' else self.settings.get_string('default-directory')
        if not path.exists(defaultPath):
            makedirs(defaultPath)
        onlyfiles = [f for f in listdir(defaultPath) if path.isfile(path.join(defaultPath, f))]
        getrows = []
        for i in webfontsData['items']:
            getrows.append(i['family'])
        for i in getrows:
            for j in onlyfiles:
                if i in j[:len(j[:-4])]:
                    self.fonts_list.get_row_at_index(getrows.index(i)).get_child().installed_box.show()





        
