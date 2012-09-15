import gtk
import xml.etree.ElementTree as ET

class PreferencesWindow:
    pages = dict()
    configFile = None

    # Callbacks #
    def destroy_window(self, caller_widget):
        self.window.destroy()
        
    def file_selected(self, caller_widget, data):
        caller_widget.set_filename(data)
    # End Callbacks #
    
    def ParseConfig(self):
        try:
            self.configFile = open('./config.xml')
        except IOError:
           return

        if self.configFile:
            tree = ET.parse('config.xml')
            root = tree.getroot()
            for page in root.findall('page'):
              name  = page.find('name').text
              url   = page.find('url').text
              img   = page.find('img').text
              order = page.find('order').text
              self.pages[name] = [order, url, img]
        
    def CreateBottomButtons(self):
        hbox = gtk.HBox(False, 0)
        hbox.set_spacing(10)
        save = gtk.Button(stock = gtk.STOCK_SAVE)
        cancel = gtk.Button(stock = gtk.STOCK_CANCEL)
        cancel.connect('clicked', self.destroy_window)
        
        hbox.pack_start(gtk.Label(''), True, False)
        hbox.pack_start(save, False)
        hbox.pack_start(cancel, False)
        hbox.pack_start(gtk.Label(''), True, False)

        self.vbox.pack_start(hbox, False)
        self.vbox.pack_start(gtk.Label(''), False)
        
    def CreateNameField(self, vbox, nameText):
        name = gtk.HBox()
        name.set_spacing(10)
        name.pack_start(gtk.Label(''), False)
        nameLabel = gtk.Label('Name')
        nameLabel.set_width_chars(5)
        nameEntry = gtk.Entry()
        nameEntry.set_text(nameText)
        name.pack_start(nameLabel, False)
        name.pack_start(nameEntry)
        name.pack_start(gtk.Label(''), False)
        vbox.pack_start(name, False)
        
    def CreateURLField(self, vbox, urlText):
        url = gtk.HBox()
        url.set_spacing(10)
        url.pack_start(gtk.Label(''), False)
        urlLabel = gtk.Label('URL')
        urlLabel.set_width_chars(5)
        urlEntry = gtk.Entry()
        urlEntry.set_text(urlText)
        url.pack_start(urlLabel, False)
        url.pack_start(urlEntry, True)
        url.pack_start(gtk.Label(''), False)
        vbox.pack_start(url, False)
    
    def CreateImagePicker(self, vbox, path):
        img = gtk.HBox()
        img.set_spacing(10)
        img.pack_start(gtk.Label(''), False)
        imgLabel = gtk.Label('Image')
        imgLabel.set_width_chars(5)
        imgChooser = gtk.FileChooserButton('Image')
        imgChooser.set_current_folder(".")
        #imgChooser.set_current_file(path)
        imgChooser.connect('file-activated', self.file_selected, path)
        imgChooser.emit('file-activated')
        img.pack_start(imgLabel, False)
        img.pack_start(imgChooser)
        img.pack_start(gtk.Label(''), False)
        vbox.pack_start(img, False)
           
    def CreatePageEntry(self, name, url, img):
        vbox = gtk.VBox()
        vbox.set_spacing(10)
        #vbox.pack_start(gtk.Label(''), False)
        
        self.CreateNameField(vbox, name)
        self.CreateURLField(vbox, url)
        self.CreateImagePicker(vbox, img)        

        vbox.pack_start(gtk.HSeparator(), False)
        
        self.vbox.pack_start(vbox, False)
    
    def CreatePreferences(self):   
        self.ParseConfig()
        self.vbox.pack_start(gtk.Label(''), False)
        if self.configFile:
            count = 1
            while count <= len(self.pages):
                for name in self.pages:
                    print self.pages[name][0], ':::', count
                    if int(self.pages[name][0]) == count:
                        self.CreatePageEntry(name, self.pages[name][1], self.pages[name][2])
                count = count + 1
        else:
            self.CreatePageEntry('', '', '.')
            # fill first page entry
            # create others as needed
        self.CreateBottomButtons()
        
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title('Preferences')
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)

        self.window.set_position(gtk.WIN_POS_CENTER)
        #self.window.resize(500, 500)
        self.window.set_default_size(500, 100)
        
        self.window.connect('destroy', self.destroy_window)
        self.vbox = gtk.VBox(False, 0)
        self.vbox.set_spacing(15)

        self.CreatePreferences()
        
        
        self.window.add(self.vbox)
        self.window.show_all()
