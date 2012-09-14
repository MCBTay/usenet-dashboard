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
        
    def CreatePreferences(self):
        buttonText = gtk.CheckButton('Show text for buttons')        
        buttonIcon = gtk.CheckButton('Show icons for buttons (if entered)')
        
        self.vbox.pack_start(buttonText)
        self.vbox.pack_start(buttonIcon)
        
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title('Preferences')
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)

        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.resize(150, 300)
        
        self.window.connect('destroy', self.DestroyWindow)
        self.vbox = gtk.VBox(False, 0)
        self.CreatePreferences()
        self.vbox.pack_start(gtk.HSeparator())
        self.CreateBottomButtons()
        self.window.add(self.vbox)
        self.window.show_all()
