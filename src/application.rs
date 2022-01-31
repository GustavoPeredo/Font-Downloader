use adw::prelude::*;
use glib::clone;
use gtk::subclass::prelude::*;
use gtk::{gio, glib};

use std::path::PathBuf;

use crate::config::VERSION;
use crate::FontDownloaderWindow;
use crate::CustomExpanderRow;

use font_catcher;

mod imp {
    use super::*;

    #[derive(Debug, Default)]
    pub struct FontDownloaderApplication {}

    #[glib::object_subclass]
    impl ObjectSubclass for FontDownloaderApplication {
        const NAME: &'static str = "FontDownloaderApplication";
        type Type = super::FontDownloaderApplication;
        type ParentType = gtk::Application;
    }

    impl ObjectImpl for FontDownloaderApplication {
        fn constructed(&self, obj: &Self::Type) {
            self.parent_constructed(obj);

            obj.setup_gactions();
            obj.set_accels_for_action("app.quit", &["<primary>q"]);
        }
    }

    impl ApplicationImpl for FontDownloaderApplication {
        // We connect to the activate callback to create a window when the application
        // has been launched. Additionally, this callback notifies us when the user
        // tries to launch a "second instance" of the application. When they try
        // to do that, we'll just present any existing window.
        fn activate(&self, application: &Self::Type) {
            // Get the current window or create one if necessary
            let window = if let Some(window) = application.active_window() {
                window
            } else {
                let window = FontDownloaderWindow::new(application);
                window.set_default_size(600, 300);
                let test = CustomExpanderRow::new();
                let test2 = CustomExpanderRow::new();
                let imp = window.imp();
                imp.list_box.append(&test);
                imp.list_box.append(&test2);
                imp.list_box.connect_row_activated(move |_,row| {
                    let expander_row = row.child().expect("").downcast::<CustomExpanderRow>().expect("");
                    let status = expander_row.get_revealer();
                    expander_row.set_revealer(!status);
                });
                window.upcast()
            };
            
            /*let list_box = gtk::ListBox::new();
            let custom_label = gtk::Button::with_label("Hello");

            //test.add_row(&another_row.clone());
            /*test.uninstall_button.connect_clicked(move |_| {
                        eprintln!(
                            "{:?}", "test1" 
                        );
                    });
test.install_button.connect_clicked(move |_| {
                        eprintln!(
                            "{:?}", "test2" 
                        );
                    });
test.download_button.connect_clicked(move |_| {
                        eprintln!(
                            "{:?}", "test3" 
                        );
                    });*/
            list_box.append(&test);
            list_box.append(&test2);
            //let a = list_box.selected_row();
            list_box.connect_selected_rows_changed(move |a| {
                let b = a.selected_row().unwrap().child().expect("").downcast::<CustomExpanderRow>().expect("");
                b.set_revealer(true);
            });
            //list_box.append(&an_another_row);
            window.set_child(Some(&list_box));
            /*let list_box = gtk::ListBox::new();
            window.set_child(Some(&));
            let fonts_hashmap = font_catcher::init().expect("Failed to init \
                font_catcher");
            for (font_name,font) in fonts_hashmap.iter() {
                let font = font.clone();
                if font.is_font_in_repo("Open Font Repository") {
                    let button = gtk::Button::with_label(&(font_name.to_owned() + "Variants"));
                    let variants = font.get_repo_variants("Open Font Repository").unwrap();
                    button.connect_clicked(move |_| {
                        eprintln!(
                            "{:?}", variants
                        );
                    });
                    let download_button = gtk::Button::with_label(&(font_name.to_owned() + "Download"));
                    download_button.connect_clicked(move |_| {
                        font.download(None, &PathBuf::from("/home/gustavo/Projekte/Font-Downloader"), false);
                    });
                    list_box.append(&button);
                    list_box.append(&download_button);
                }
            }
            */*/
            
            // Ask the window manager/compositor to present the window
            window.present();
        }
    }

    impl GtkApplicationImpl for FontDownloaderApplication {}
}

glib::wrapper! {
    pub struct FontDownloaderApplication(ObjectSubclass<imp::FontDownloaderApplication>)
        @extends gio::Application, gtk::Application,
        @implements gio::ActionGroup, gio::ActionMap;
}

impl FontDownloaderApplication {
    pub fn new(application_id: &str, flags: &gio::ApplicationFlags) -> Self {
        glib::Object::new(&[("application-id", &application_id), ("flags", flags)])
            .expect("Failed to create FontDownloaderApplication")
    }

    fn setup_gactions(&self) {
        self.connect_startup(|_| {
            adw::init();
        });    
        let quit_action = gio::SimpleAction::new("quit", None);
        quit_action.connect_activate(clone!(@weak self as app => move |_, _| {
            app.quit();
        }));
        self.add_action(&quit_action);

        let about_action = gio::SimpleAction::new("about", None);
        about_action.connect_activate(clone!(@weak self as app => move |_, _| {
            app.show_about();
        }));
        self.add_action(&about_action);
    }

    fn show_about(&self) {
        let window = self.active_window().unwrap();
        let dialog = gtk::builders::AboutDialogBuilder::new()
            .transient_for(&window)
            .modal(true)
            .program_name("font-downloader")
            .version(VERSION)
            .authors(vec!["Gustavoperedo".into()])
            .build();

        dialog.present();
    }
}
