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
#Import necessary libraries and modules
#from gettext import gettext as _
from gi.repository import Gdk, Gio, Gtk, GLib, Handy, GObject, WebKit2, Pango
from os import path, makedirs, listdir
import locale
import json
import threading
from copy import deepcopy
from .fsync import async_function
from time import sleep
from urllib.request import urlretrieve, urlopen

#Init Webkit and Handy libs
Handy.init()
WebKit2.WebView()

locale.bindtextdomain('fontdownloader', path.join(path.dirname(__file__).split('fontdownloader')[0],'locale'))
locale.textdomain('fontdownloader')

webfontsData = json.load(open(path.join(path.dirname(__file__).split('fontdownloader')[0],'fontdownloader/fontdownloader/webfonts.json'), 'r'))

SAMPLE_STRING = Pango.language_get_default().get_sample_string()

#Here we import the font-box template which is used for the fonts' boxes
@Gtk.Template(resource_path='/org/gustavoperedo/FontDownloader/font-box.ui')
class FontBox(Gtk.Box):
    __gtype_name__ = 'FontBox'

    fontFamily = Gtk.Template.Child()
    fontCategory = Gtk.Template.Child()
    installed_box = Gtk.Template.Child()
    update_box = Gtk.Template.Child()
    system_installed_box = Gtk.Template.Child()

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        #When creating, add all information on a data variable
        self.data = data
        #Set labels' texts
        self.fontFamily.set_text(data['family'])
        category = data['category']
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
    colorful_switch = Gtk.Template.Child()
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
    header_leaflet = Gtk.Template.Child()
    scroll_window = Gtk.Template.Child()
    preview_stack = Gtk.Template.Child()
    preview_box = Gtk.Template.Child()
    failed_box = Gtk.Template.Child()
    loading_box = Gtk.Template.Child()
    revealer = Gtk.Template.Child()
    notification_label = Gtk.Template.Child()
    dismiss_notification = Gtk.Template.Child()
    progress_bar = Gtk.Template.Child()
    developer_switch = Gtk.Template.Child()
    developer_box = Gtk.Template.Child()
    style_textbox = Gtk.Template.Child()
    text_buffer = Gtk.Template.Child()

    #On initialization do:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Creates temporary variables for our window
        self.defaultPath = path.join(path.expanduser('~'), '.local/share/fonts') if self.settings.get_string('default-directory') == 'Default' else self.settings.get_string('default-directory')
        self.jsonOfInstalledFonts = json.loads(self.settings.get_string('installed-fonts'))
        self.CurrentSelectedFont = ''
        self.CurrentText = SAMPLE_STRING
        self.CurrentFilters = {
            'serif': self.serif_check.get_active(),
            'sans-serif': self.sans_check.get_active(),
            'display': self.display_check.get_active(),
            'handwriting': self.handwriting_check.get_active(),
            'monospace': self.mono_check.get_active()
        }

        #Connect buttons, clicks, key presses to their functions
        self.fonts_list.connect('row-activated', self.fontChanged)
        self.text_entry.connect('changed', self.updatedTextEntry)
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
        self.colorful_switch.connect('notify::active', self.flipSwitch)
        self.developer_switch.connect('notify::active', self.flipDevSwitch)
        self.settings_button.connect('clicked', self.presentSettings)
        self.close_settings_button.connect('clicked', self.closeSettings)
        self.folder_settings_button.connect('clicked', self.on_open)
        self.any_alphabet_button.connect('clicked', self.anyAlphabet)
        self.reset_button.connect('clicked', self.reset)
        self.header_group.connect('update-decoration-layouts', self.updateSize)
        self.scroll_window.connect('edge-reached', self.increaseSearch)
        self.connect("key-press-event", self.toggleSearchKeyboard)
        self.connect_after("key-press-event", self.toggleSearchKeyboardAfter)
        self.font_preview.connect("load-changed", self.webviewLoading)
        self.dismiss_notification.connect('clicked', self.removeNotification)

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

        self.size_increase = 1
        self.text_entry_active = False
        self.current_alphabet_list = self.settings.get_string('current-alphabet').split(';')
        self.any_alphabet_button.set_active(self.settings.get_boolean('any-alphabet'))
        self.any_alphabet = self.any_alphabet_button.get_active()

        for i in range(len(self.alphabet_list)):
            if self.alphabet_list[i] in self.current_alphabet_list:
                self.alphabet_buttons[i].set_active(True)
            else:
                self.alphabet_buttons[i].set_active(False)

        self.anyAlphabet()

        #Get list of fonts stored in gschema
        #self.settings.set_string('installed-fonts', '{"kind": "webfonts#webfontList","items": []}')

        #Get fonts on default-directory
        self.updateListOfInstalledFonts()

        #Select the first row and show all rows
        #self.fonts_list.select_row(self.fonts_list.get_row_at_index(0))
        self.fonts_list.show()
        self.folder_settings_button.set_label(_('Default') if self.settings.get_string('default-directory')=='Default' else self.settings.get_string('default-directory'))

        for buttons in self.alphabet_buttons:
            buttons.connect("toggled", self.updateAlphabet)

        self.dark_mode_button.set_active(self.settings.get_boolean('dark-mode'))
        self.colorful_switch.set_active(self.settings.get_boolean('colorful-mode'))
        self.developer_switch.set_active(self.settings.get_boolean('developer-window'))
        self.changeTheme()

        #Sets up borders
        self.setup_css()

    #About dialog, courtesy of GeorgesStavracas
    def on_about(self, *args, **kwargs):
        authors = ['Gustavo Machado Peredo']
        contributors = ['Georges Basile Stavracas Neto',
                        'Martin Abente Lahaye', 'Manuel Quiñones']
        translators = ['Gustavo Machado Peredo', 'Victor Ibragimov',
                       'Manuel Quiñones', 'Heimen Stoffels', 'Jiri Grönroos',
                       'Julian. hofer', 'Åke Engelbrektson', 'oscfdezdz',
                       'milotype', 'Kblaesi', 'Roberto', 'Xemafuentes',
                       'Mauricemeysel', 'Hemish04082005', 'TA',
                       '小山田 純', 'Efraín Epifanio',
                       "usnotv", "Xemafuentes", "Lumingzh",
                       ]
        dialog = Gtk.AboutDialog(transient_for=self, modal=True)
        dialog.props.authors = authors
        dialog.add_credit_section(_("Contributors"), contributors)
        dialog.add_credit_section(_("Translators"), translators)
        dialog.props.copyright = 'Copyright \xa9 2021 Gustavo Peredo'
        dialog.props.license_type = Gtk.License.GPL_3_0
        dialog.props.logo_icon_name = 'org.gustavoperedo.FontDownloader'
        dialog.props.program_name = _('Font Downloader')

        dialog.present()


    def setup_css(self, *args, **kwargs):
        #Setup the CSS and load it.
        uri = 'resource:///org/gustavoperedo/FontDownloader/'
        provider = Gtk.CssProvider()

        if self.settings.get_boolean('colorful-mode'):
            provider_file = Gio.File.new_for_uri(uri + "green.css")
        else:
            provider_file = Gio.File.new_for_uri(uri + "style.css")

        provider.load_from_file(provider_file)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def updateListOfInstalledFonts(self, *args, **kwargs):
        #Check if path exists :P
        if not path.exists(self.defaultPath):
            makedirs(self.defaultPath)

        #Get list of actual installed fonts in directory
        listOfInstalledFonts = [f for f in listdir(self.defaultPath) if path.isfile(path.join(self.defaultPath, f))]
        listOfSystemInstalledFonts = [f for f in listdir("/usr/share/fonts")]

        #Compare json with installed fonts and files on the default-directory
        for useless in webfontsData['items']:
            for i in range(len(self.jsonOfInstalledFonts['items'])):
                if not (self.jsonOfInstalledFonts['items'][i]['family'] in str(listOfInstalledFonts)):
                    if not (self.jsonOfInstalledFonts['items'][i]['family'].lower() in str(listOfSystemInstalledFonts)):
                        self.jsonOfInstalledFonts['items'].pop(i)
                        break
                    self.jsonOfInstalledFonts['items'].pop(i)
                    break

        for j in listOfSystemInstalledFonts:
            for i in range(len(webfontsData['items'])):
                #Gather data from webfontsData
                if webfontsData['items'][i]['family'].lower() in j:
                    if not (webfontsData['items'][i]['family'] in str(self.jsonOfInstalledFonts['items'])):
                        #Add "System" as version since it's system installed
                        l = deepcopy(webfontsData)
                        l['items'][i]['version'] = "System"
                        self.jsonOfInstalledFonts['items'].append(l['items'][i])

        for j in listOfInstalledFonts:
            for i in range(len(webfontsData['items'])):
                #Gather data from webfontsData
                if webfontsData['items'][i]['family'] in j[:len(j[:-4])]:
                    if not (webfontsData['items'][i]['family'] in str(self.jsonOfInstalledFonts['items'])):
                        #Remove version since we don't know
                        l = deepcopy(webfontsData)
                        l['items'][i]['version'] = "None"
                        self.jsonOfInstalledFonts['items'].append(l['items'][i])
        #Remove duplicates
        listOfInstalledFontsItems = self.jsonOfInstalledFonts['items']
        self.jsonOfInstalledFonts['items'] = []
        for i in listOfInstalledFontsItems:
            if not(i['family'] in str(self.jsonOfInstalledFonts['items'])):
                self.jsonOfInstalledFonts['items'].append(i)
        #Save new installed fonts string
        self.settings.set_string('installed-fonts', json.dumps(self.jsonOfInstalledFonts))
        self.updateFilter()

    def updateProgressBar(self, chosen_path, links, is_download, data=None):
        def on_done_updating(result, error):
            if error:
                print(error)
                if is_download:
                    self.notification_label.set_label(_("Failed to download font. Check your internet connection and folder permissions"))
                else:
                    self.notification_label.set_label(_("Failed to install font. Check your internet connection and folder permissions"))
            else:
                if is_download:
                    self.notification_label.set_label(_("Font downloaded successfully!"))
                else:
                    self.notification_label.set_label(_("Font installed successfully!"))
                    if data['family'] in str(self.jsonOfInstalledFonts['items']):
                        for i in range(len(self.jsonOfInstalledFonts['items'])):
                            if (self.jsonOfInstalledFonts['items'][i]['family'] == data['family']):
                                self.jsonOfInstalledFonts['items'].pop(i)
                                self.jsonOfInstalledFonts['items'].append(data)
                                break
                    else:
                        self.jsonOfInstalledFonts['items'].append(data)

            self.revealer.set_reveal_child(True)
            self.updateListOfInstalledFonts()
            self.main_download_button.set_sensitive(True)
            self.main_install_button.set_sensitive(True)
            self.progress_bar.set_visible(False)

        def update_on_thread():
            percentile = round(1/len(links), 2)
            current_percentile = 0
            self.progress_bar.set_visible(True)
            self.main_download_button.set_sensitive(False)
            self.main_install_button.set_sensitive(False)
            try:
                for key in links:
                    urlretrieve(links[key], path.join(chosen_path, self.CurrentSelectedFont + " " + key + links[key][-4:]))
                    current_percentile = current_percentile + percentile
                    self.progress_bar.set_fraction(current_percentile)
                on_done_updating("", "")
            except Exception as e:
                on_done_updating("", e)
        update_on_thread()

    def installFont(self, button):
        #This function gets the selected font's link and downloads
        #to the '.local/share/fonts' directory
        data = self.fonts_list.get_selected_row().get_child().data
        thread = threading.Thread(target=GLib.idle_add, args=(self.updateProgressBar, self.defaultPath, data['files'], False, data))
        thread.daemon = True
        thread.start()

    def downloadFont(self, button):
        #This function gets the selected font's link and downloads
        #to the user's download directory
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
                Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        links = self.fonts_list.get_selected_row().get_child().data['files']

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            absolutePath = dialog.get_filename()
            if not path.exists(absolutePath):
                makedirs(absolutePath)
            dialog.destroy()
            thread = threading.Thread(target=GLib.idle_add, args=(self.updateProgressBar, absolutePath, links, True))
            thread.daemon = True
            thread.start()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def removeNotification(self, *args, **kwargs):
        self.revealer.set_reveal_child(False)

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
        #Get category filters
        self.CurrentFilters = {
            'serif': self.serif_check.get_active(),
            'sans-serif': self.sans_check.get_active(),
            'display': self.display_check.get_active(),
            'handwriting': self.handwriting_check.get_active(),
            'monospace': self.mono_check.get_active()
        }
        filtered = [filters for filters in self.CurrentFilters if self.CurrentFilters[filters]]

        #Creates a counters so limited amount of results appear
        self.private_counter = 0

        #Get search bar text from search
        searchBarText = self.search_entry.get_text().lower()

        #Remove all rows
        for i in range(len(self.fonts_list)):
            self.fonts_list.remove(self.fonts_list.get_row_at_index(0))

        #Add them if seen necessary (this is faster than filtering them :P)
        for i in range(len(webfontsData['items'])):
            if webfontsData['items'][i]['category'] in filtered:
                if searchBarText in webfontsData['items'][i]['family'].lower():
                    if (all(k in webfontsData['items'][i]['subsets'] for k in self.current_alphabet_list)) or (self.any_alphabet):
                        if self.private_counter <= (25*self.size_increase):
                            self.newBox = FontBox(webfontsData['items'][i])
                            #Make it visible and append it to our fonts panel
                            for j in self.jsonOfInstalledFonts['items']:
                                if webfontsData['items'][i]['family'] == j['family']:
                                    if j['version'] == "System":
                                        self.newBox.system_installed_box.show()
                                    elif j['version'] != webfontsData['items'][i]['version']:
                                        self.newBox.update_box.show()
                                    else:
                                        self.newBox.installed_box.show()
                            self.newBox.set_visible(True)
                            self.fonts_list.add(self.newBox)
                            self.private_counter = self.private_counter + 1
                elif searchBarText in "installed" or searchBarText in "update":
                    if (all(k in webfontsData['items'][i]['subsets'] for k in self.current_alphabet_list)) or (self.any_alphabet):
                        if self.private_counter <= (25*self.size_increase):
                            for j in self.jsonOfInstalledFonts['items']:
                                if webfontsData['items'][i]['family'] == j['family']:
                                    self.newBox = FontBox(webfontsData['items'][i])
                                    if j['version'] == "System":
                                        self.newBox.system_installed_box.show()
                                    elif j['version'] != webfontsData['items'][i]['version']:
                                        self.newBox.update_box.show()
                                    else:
                                        self.newBox.installed_box.show()
                                    self.newBox.set_visible(True)
                                    self.fonts_list.add(self.newBox)
                                    self.private_counter = self.private_counter + 1

    def increaseSearch(self, *args, **kwargs):
        if self.scroll_window.get_vadjustment().get_value() > 100:
            self.updateFilter()
            self.size_increase = self.size_increase + 1

    def updatedTextEntry(self, *args, **kwargs):
        self.text_entry_active = True
        self.fontChanged()

    def fontChanged(self, *args, **kwargs):
        #Whenever the user does something that should change the font preview:
        if self.fonts_list.get_selected_row():
            #We colect the data from the selected font
            #The variable CurrentSelectedFont carries the font name
            self.CurrentSelectedFont = self.fonts_list.get_selected_row().get_child().data['family']

        self.main_install_button.set_sensitive(False)
        self.main_download_button.set_sensitive(False)

        #Get the text from the text entry
        self.CurrentText = self.text_entry.get_text()
        if self.CurrentText == "":
            self.CurrentText = SAMPLE_STRING
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
        font_category = self.fonts_list.get_selected_row().get_child().data['category']
        self.headerbar2.set_subtitle(_('sans-serif')
            if font_category=='sans-serif'
            else (_('serif') if font_category=='serif' else (_('display')
            if font_category=='display' else (_('monospaced')
            if font_category=='monospace' else _('handwriting')))))
        self.leaflet.set_visible_child(self.box2)
        self.header_leaflet.set_visible_child(self.headerbar2)

    def webviewLoading(self, *args, **kwargs):
        def webview_show(result, error):
            if error:
                self.preview_stack.set_visible_child(self.failed_box)
                print(error)
            else:
                if not self.main_install_button.get_sensitive():
                    self.main_install_button.set_sensitive(True)
                    self.main_download_button.set_sensitive(True)
                self.text_buffer.set_text(result.replace("\\n", "\n").replace(result[0:2], "\n").replace(result[-1], ""))
                if not self.text_entry_active:
                    self.preview_stack.set_visible_child(self.preview_box)
                if not self.text_entry.is_focus():
                    self.text_entry_active = False

        @async_function(on_done=webview_show)
        def webview_loading():
            if not self.text_entry_active:
                self.preview_stack.set_visible_child(self.loading_box)
            return str(urlopen("https://fonts.googleapis.com/css2?family=" + self.CurrentSelectedFont.replace(' ','+') + "&display=swap").read())

        text_to_set = ""
        webview_loading()


    def updateSize(self, *args, **kwargs):
        self.back_button.set_sensitive(self.header_leaflet.get_folded())

    #Turns search on or off
    def toggleSearch(self, *args, **kwargs):
        self.updateFilter()
        self.search_bar.set_search_mode(not self.search_bar.get_search_mode())

    #Thanks udayantandon for this implementation :)
    #https://udayantandon.wordpress.com/2015/07/29/a-custom-searchbar-in-gtk-and-python/
    def toggleSearchKeyboard(self, widget, event, *args):
        keyname = Gdk.keyval_name(event.keyval)
        if not self.text_entry_active:
            if keyname == 'Escape' and self.search_button.get_active():
                if self.search_entry.is_focus():
                    self.search_button.set_active(False)
                else:
                    self.search_entry.grab_focus()
                return True

            if event.state & Gdk.ModifierType.CONTROL_MASK:
                if keyname == 'f':
                    self.search_button.set_active(True)
                    return True

        return False

    def toggleSearchKeyboardAfter(self, widget, event, *args):
        if not self.text_entry_active:
            if (not self.search_button.get_active() or not self.search_entry.is_focus()):
                if self.search_entry.im_context_filter_keypress(event):
                    self.search_button.set_active(True)
                    self.search_entry.grab_focus()

                    # Text in entry is selected, deselect it
                    l = self.search_entry.get_text_length()
                    self.search_entry.select_region(l, l)

                    return True

        return False

    #If the user press back_button, return focus to list view
    def bringListForward(self, *args, **kwargs):
        self.leaflet.set_visible_child(self.box1)
        self.header_leaflet.set_visible_child(self.headerbar1)

    def changeTheme(self, *args, **kwargs):
        if self.dark_mode_button.get_active():
            Gtk.Settings.get_default().set_property('gtk-application-prefer-dark-theme', True)
            self.settings.set_boolean('dark-mode', True)
        else:
            Gtk.Settings.get_default().set_property('gtk-application-prefer-dark-theme', False)
            self.settings.set_boolean('dark-mode', False)

    def flipSwitch(self, button, *args, **kwargs):
        self.settings.set_boolean('colorful-mode', button.get_active())

    def flipDevSwitch(self, button, *args, **kwargs):
        if button.get_active():
            self.developer_box.set_visible(True)
            self.settings.set_boolean('developer-window', True)
        else:
            self.developer_box.set_visible(False)
            self.settings.set_boolean('developer-window', False)

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
                self.alphabet_buttons[i].set_active(not self.any_alphabet)
            elif self.alphabet_buttons[i].get_active():
                self.current_alphabet_list.append(self.alphabet_list[i])
        self.settings.set_string('current-alphabet', ';'.join(self.current_alphabet_list))
        self.updateFilter()

    def anyAlphabet(self, *args, **kwargs):
        self.any_alphabet = self.any_alphabet_button.get_active()
        for i in range(len(self.alphabet_list)):
            self.alphabet_buttons[i].set_sensitive(not self.any_alphabet)
        self.settings.set_boolean('any-alphabet', self.any_alphabet)
        self.updateAlphabet()

    def reset(self, *args, **kwargs):
        self.settings.set_string('default-directory', 'Default')
        self.folder_settings_button.set_label('Default')
        self.any_alphabet_button.set_active(True)
        self.colorful_switch.set_active(False)
        self.developer_switch.set_active(False)
        self.light_mode_button.set_active(True)
        self.updateAlphabet()
