import gtk

class PreferencesWindow:
    def DestroyWindow(caller_widget):
        window.destroy()
        
    def __init__(self):
        window = gtk.Window()

        window.set_position(gtk.WIN_POS_CENTER)
        window.resize(150, 300)

        window.connect("destroy", self.DestroyWindow)

        window.show_all()
    
    
    
        
