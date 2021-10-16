<h1><img src="./data/icons/hicolor/scalable/apps/org.gustavoperedo.FontDownloader.svg"> Font Downloader</h1>

![master](https://github.com/GustavoPeredo/Font-Downloader/actions/workflows/build.yml/badge.svg)

## About

One day I was bored of my terminal font and wanted to switch, unfortunately going through the entire process of searching Google Fonts for a font, then downloading, then copying and pasting it into my .fonts folder to only then test a font was a pain. So I decided to create this app!
<div align="right">
    <a href='https://flathub.org/apps/details/org.gustavoperedo.FontDownloader'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a>
</div>


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

They are here and need your help! Don't be afraid to open an issue or contribute to the translations here: [https://poeditor.com/join/project?hash=hfnXv8Iw4o](https://poeditor.com/join/project?hash=hfnXv8Iw4o)

## Special thanks
For all the contributers, translators, atareao (fsync) and Selenium.H (theme) 

<div align="center">
    <p><b> Proudly part of the GNOME Circle </b></p>
    <a href='https://circle.gnome.org/'><img width='240' alt='GNOME Circle' src='https://gitlab.gnome.org/Teams/Circle/-/raw/master/assets/button/circle-button-fullcolor.svg'/></a>
</div>
