import os, gtk, gobject

class AboutWindow:
    # Callbacks
    def destroy_window(self, caller_widget):
        self.window.destroy()
    # End Callbacks
    
    def CreateWindow(self):
        self.window = gtk.Window()
        self.vbox = gtk.VBox(False, 2)
        self.vbox.set_spacing(15)
        self.window.set_title('About')
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_default_size(500, 100)
        self.window.connect('destroy', self.destroy_window)

    def CreateIcon(self):
        icon = gtk.Image()
        icon_filepath = os.path.join(os.path.dirname(__file__), 'img/logo.png')
        icon.set_from_file(icon_filepath)
        self.vbox.pack_start(icon)
        
    def CreateLabel(self, string, markup=None):
        label = gtk.Label(string)
        if markup:
            label.set_markup(markup)
        self.vbox.pack_start(label)
 
    def __init__(self):
        self.CreateWindow()   
        self.vbox.pack_start(gtk.Label(''))
        self.CreateIcon()
        self.CreateLabel('Version 0.9')
        self.CreateLabel('written by Bryan Taylor and Spencer Smith')
        self.CreateLabel('', '<a href="http://github.com/MCBTay/usenet-dashboard">http://github.com/MCBTay/usenet-dashboard</a>')
        self.CreateLabel('A dashboard for managing all usenet-related windows in one easy spot.')                      
        self.vbox.pack_start(gtk.Label(''))
        self.window.add(self.vbox)
        self.window.show_all()
