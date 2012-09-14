import gtk

class PreferencesWindow:

    def DestroyWindow(self, caller_widget):
        self.window.destroy()
        
    def CreateBottomButtons(self):
        hbox = gtk.HBox(False, 0)

        save = gtk.Button(stock = gtk.STOCK_SAVE)
        cancel = gtk.Button(stock = gtk.STOCK_CANCEL)
        cancel.connect("clicked", self.DestroyWindow)
        
        hbox.pack_start(save, False)
        hbox.pack_start(cancel, False)
        self.window.add(hbox)
        
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)

        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.resize(150, 300)
        
        self.window.connect("destroy", self.DestroyWindow)
        self.CreateBottomButtons()
        self.window.show_all()
