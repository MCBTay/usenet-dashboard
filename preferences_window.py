import gtk

class PreferencesWindow:

    def DestroyWindow(self, caller_widget):
        self.window.destroy()
        
    def CreateBottomButtons(self):
        hbox = gtk.HBox(False, 0)
        hbox.set_spacing(10)
        save = gtk.Button(stock = gtk.STOCK_SAVE)
        cancel = gtk.Button(stock = gtk.STOCK_CANCEL)
        cancel.connect('clicked', self.DestroyWindow)
        
        hbox.pack_start(gtk.Label(''), True, False)
        hbox.pack_start(save, False)
        hbox.pack_start(cancel, False)
        hbox.pack_start(gtk.Label(''), True, False)

        self.vbox.pack_start(hbox, False)
        self.vbox.pack_start(gtk.Label(''), False)
        
    def CreateNameField(self, vbox):
        name = gtk.HBox()
        name.set_spacing(10)
        name.pack_start(gtk.Label(''), False)
        nameLabel = gtk.Label('Name')
        nameLabel.set_width_chars(5)
        nameEntry = gtk.Entry();
        name.pack_start(nameLabel, False)
        name.pack_start(nameEntry)
        name.pack_start(gtk.Label(''), False)
        vbox.pack_start(name, False)
        
    def CreateURLField(self, vbox):
        url = gtk.HBox()
        url.set_spacing(10)
        url.pack_start(gtk.Label(''), False)
        urlLabel = gtk.Label('URL')
        urlLabel.set_width_chars(5)
        urlEntry = gtk.Entry();
        url.pack_start(urlLabel, False)
        url.pack_start(urlEntry, True)
        url.pack_start(gtk.Label(''), False)
        vbox.pack_start(url, False)
    
    def CreateImagePicker(self, vbox):
        img = gtk.HBox()
        img.set_spacing(10)
        img.pack_start(gtk.Label(''), False)
        imgLabel = gtk.Label('Image');
        imgLabel.set_width_chars(5)
        imgChooser = gtk.FileChooserButton('Image')
        img.pack_start(imgLabel, False)
        img.pack_start(imgChooser)
        img.pack_start(gtk.Label(''), False)
        vbox.pack_start(img, False)
    
        
    def CreatePageEntry(self):
        vbox = gtk.VBox()
        vbox.set_spacing(10)
        vbox.pack_start(gtk.Label(''), False)
        
        self.CreateNameField(vbox)
        self.CreateURLField(vbox)
        self.CreateImagePicker(vbox)        
        
        vbox.pack_start(gtk.Label(''), False)
        
        vbox.pack_start(gtk.HSeparator(), False);
        
        vbox.pack_start(gtk.Label(''), False);
        
        self.vbox.pack_start(vbox, False)

    def CreatePreferences(self):        
        self.CreatePageEntry()
        self.CreateBottomButtons()
        
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title('Preferences')
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)

        self.window.set_position(gtk.WIN_POS_CENTER)
        #self.window.resize(500, 500)
        self.window.set_default_size(500, 100)
        
        self.window.connect('destroy', self.DestroyWindow)
        self.vbox = gtk.VBox(False, 0)
        self.CreatePreferences()
        
        
        self.window.add(self.vbox)
        self.window.show_all()
