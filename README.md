# A Simple GTK application to install and download fonts.

## About

One day I was bored of my terminal font and wanted to switch, unfortunately going through the entire process of searching Google Fonts for a font, then downloading, then copying and pasting it into my .fonts folder to only then test a font was a pain. So I decided to create this app!

## Screenshots

![](https://raw.githubusercontent.com/GustavoPeredo/font-downloader/master/data/screenshots/entire.png)
![](https://raw.githubusercontent.com/GustavoPeredo/font-downloader/master/data/screenshots/compact.png)
![](https://raw.githubusercontent.com/GustavoPeredo/font-downloader/master/data/screenshots/dark_entire.png)
![](https://raw.githubusercontent.com/GustavoPeredo/font-downloader/master/data/screenshots/dark_compact.png)

## How to compile

If you use GNOME Builder, simply cloning the project is enough, otherwise you need to install libhandy as a dependency.

Dependencies in Fedora:
```
sudo dnf install cmake meson ninja 
sudo dnf install libhandy1-dev
```


Then build using meson:

```
git clone https://github.com/GustavoPeredo/font-downloader.git
cd font-downloader
mkdir build
meson build .
cd build
ninja
ninja install
```

To run it from terminal:
```
fontdownloader
```

## Translations!

They are here and need your help! I translated the app for languages that I've had some contact with in the past (German, French, Spanish and English), but they aren't my mother languages, so if you find any spelling/grammar mistake or want to add your language, don't be afraid to open an issue or contribute to the translations here: [https://poeditor.com/join/project?hash=hfnXv8Iw4o](https://poeditor.com/join/project?hash=hfnXv8Iw4o)

## To-Dos

* ~~Learn how po works~~
* ~~Do some translations~~
* ~~See if it is ready for flatpak~~
* ~~Add GtkFileChooser dialog for user to choose where to download fonts to~~
* ~~Create settings panel (default installation directory and dark mode)~~
* ~~Create about window~~
* ~~Visual feedback for when fonts are done installing/downloading~~
* ~~Show a little check for when a font is already installed~~
* ~~Add new filters (depending on alphabet, will probably require a redesign of the app)~~
* ~~Optimize code~~
* ~~Update to libhandy 1.0 and update glade files acordingly~~
* ~~Find a way to remove the "back_button" without check-resize~~
* ~~Fix fonts names~~
* ~~Translate new strings~~
