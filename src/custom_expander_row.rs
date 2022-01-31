use adw::prelude::*;
use gtk::subclass::prelude::*;
use gtk::{gio, glib, CompositeTemplate};

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/org/gustavoperedo/FontDownloader/ui/expander_row.ui")]
    pub struct CustomExpanderRow {
        // Template widgets
        #[template_child]
        pub uninstall_button: TemplateChild<gtk::Button>,
        #[template_child]
        pub install_button: TemplateChild<gtk::Button>,
        #[template_child]
        pub download_button: TemplateChild<gtk::Button>,
        
        #[template_child]
        pub font_categories_label: TemplateChild<gtk::Label>,
        #[template_child]
        pub font_name_label: TemplateChild<gtk::Label>,
        #[template_child]
        pub font_alphabets_label: TemplateChild<gtk::Label>,

        #[template_child]
        pub revealer: TemplateChild<gtk::Revealer>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for CustomExpanderRow {
        const NAME: &'static str = "CustomExpanderRow";
        type Type = super::CustomExpanderRow;
        type ParentType = gtk::Box;

        fn class_init(klass: &mut Self::Class) {
            Self::bind_template(klass);
            Self::bind_template_callbacks(klass);
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl CustomExpanderRow {
        #[template_callback]
        fn on_activation(&self) -> bool {
            self.revealer.is_child_revealed()
            //self.revealer.set_reveal_child(true);
        }
    }

    impl ObjectImpl for CustomExpanderRow {}
    impl WidgetImpl for CustomExpanderRow {}
    impl BoxImpl for CustomExpanderRow {}
}

glib::wrapper! {
    pub struct CustomExpanderRow(ObjectSubclass<imp::CustomExpanderRow>)
        @extends gtk::Widget, gtk::Box,
        @implements gio::ActionGroup, gio::ActionMap;
}

impl CustomExpanderRow {
    pub fn new() -> CustomExpanderRow {
        glib::Object::new(&[])
            .expect("Failed to create FontDownloaderWindow")
    }
    pub fn get_revealer(&self) -> bool {
        let imp = self.imp();
        imp.revealer.is_child_revealed()
        //self.inner.revealer.is_child_revealed()
    }
    pub fn set_revealer(&self, reveal: bool) {
        let imp = self.imp();
        imp.revealer.set_reveal_child(reveal);
    }
}
