import gtk
import preferences_window

class SiteEntry:
    def __init__ (self, parent, order, name, url, img):
        self.parent = parent
        self.configuration = parent.configuration
        self.entry_hbox = gtk.HBox()
        self.name = name
        self.order = order
        self.url = url
        self.img = img        
        
        self.CreateImagePicker(self.entry_hbox, self.name)
        
        vbox = gtk.VBox()
        vbox.set_spacing(10)
        
        self.CreateNameRow(vbox, self.name, self.order)
        self.CreateURLRow(vbox, self.url, self.name)
        
        self.entry_hbox.pack_start(vbox, False, False)
        
    # Callbacks #
    def create_file_chooser_dialog(self, button):
        chooser = gtk.FileChooserDialog(title=None, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK))
        self.CreateChooserFilter(chooser)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.update_button_thumbnail(button, chooser.get_filename())
        chooser.destroy()    
        
    # order is only passed for the name text entry as it is the key to our dictionary
    # name is passed in to know which record to update in the dictionary
    def entry_changed(self, caller_widget, order = None, name = None):
        newText = caller_widget.get_text()
        if order:
            self.name = newText
            page = self.findPageByOrder(int(order))
            # since we can't change keys, we'll have to create a new entry and delete the old one
            storedOrder = self.configuration['pages'][page][0]
            storedUrl   = self.configuration['pages'][page][1]
            storedImg   = self.configuration['pages'][page][2]
            self.configuration['pages'][newText] = [storedOrder, storedUrl, storedImg]
            for tempField in self.configuration['pages'].keys():
                if tempField == page:
                    del(self.configuration['pages'][tempField])
        else: 
            # so far URL is the only other case, so i'm handling it specifically
            self.configuration['pages'][self.name][1] = newText
            
    def combobox_changed(self, caller_widget, name = None):
        # offset by one because get_active() returns the index of the active, not data
        newOrder = caller_widget.get_active() + 1 
        if name:
            self.configuration['pages'][name][0] = str(newOrder)
        
    def filechooser_changed(self, caller_widget, name = None):
        newImg = caller_widget.get_filename()
        self.configuration['pages'][name][2] = newImg    
        
    def delete_clicked(self, caller_widget, nameText):
        labelString = 'Are you sure you want to delete your entry for ' + nameText + '?'
        dialog = gtk.Dialog('Are you sure?', None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialog.vbox.set_spacing(10)
        dialog.vbox.pack_start(gtk.Label(labelString))
        dialog.show_all()
        if (dialog.run() == gtk.RESPONSE_ACCEPT):
            if (self.configuration['pages'][nameText]):
                del(self.configuration['pages'][nameText])
                self.parent.RemoveEntry(nameText)
        dialog.destroy()            
        
    def update_button_thumbnail(self, button, filename):
        image = gtk.Image()
        image.set_from_file(filename)
        button.set_image(image)
        button.show_all()   
                    
    # End Callbacks #
    
    def findPageByOrder(self, order):
        winner = None
        count = 1
        while count <= len(self.configuration['pages']):
            for name in self.configuration['pages']:
                pageOrder = self.configuration['pages'][name][0]
                if int(pageOrder) == order:
                    winner = name
            count = count + 1 
        return winner
        
    def CreateImagePicker(self, hbox, name):
        button = gtk.Button()
        
        image = gtk.Image()
        imagepath = self.configuration['pages'][name][2]
        if imagepath != '' or imagepath != None:
            image.set_from_file(imagepath)
        else:
            image.set_from_stock(gtk.STOCK_ADD, 5)
        button.set_image(image)
        button.set_size_request(60, 60)
        button.connect('clicked', self.create_file_chooser_dialog)
        hbox.pack_start(gtk.Label(''))
        hbox.pack_start(button, False, False)
        
    def CreateNameRow(self, vbox, nameText, order):
        name = gtk.HBox()
        name.set_spacing(10)
        name.pack_start(gtk.Label(''), False)
        nameLabel = gtk.Label('Name')
        nameLabel.set_width_chars(5)
        nameEntry = gtk.Entry()
        nameEntry.set_text(nameText)
        nameEntry.connect('changed', self.entry_changed, order)
        name.pack_start(nameLabel, False)
        name.pack_start(nameEntry)
        
        self.CreateOrderSelector(name, order, nameText)
        self.CreateDeleteButton(name, nameText)
        
        name.pack_start(gtk.Label(''), False)
        vbox.pack_start(name, False)
        
    def CreateURLRow(self, vbox, urlText, name):
        if not urlText:
            urlText = ''
        url = gtk.HBox()
        url.set_spacing(10)
        url.pack_start(gtk.Label(''), False)
        urlLabel = gtk.Label('URL')
        urlLabel.set_width_chars(5)
        urlEntry = gtk.Entry()
        urlEntry.connect('changed', self.entry_changed, None, self.name)
        urlEntry.set_text(urlText)
        url.pack_start(urlLabel, False)
        url.pack_start(urlEntry, True)
        url.pack_start(gtk.Label(''), False)
        vbox.pack_start(url, False)
        
    def CreateOrderSelector(self, box, order, name):
        box.pack_start(gtk.Label('Order'), False)
        
        liststore = gtk.ListStore(str)
        orderDropdown = gtk.ComboBox()
        cell = gtk.CellRendererText()
        orderDropdown.pack_start(cell, True)
        orderDropdown.add_attribute(cell, 'text', 0)
        orderDropdown.connect('changed', self.combobox_changed, name)
        
        if len(self.configuration['pages']) == 0:
            liststore.append([str(1)])
        else:
            count = 1
            while count <= len(self.configuration['pages']):
                liststore.append([str(count)])
                count = count + 1
         
        orderDropdown.set_model(liststore)
        orderDropdown.set_active(int(order)-1)
        
        box.pack_start(orderDropdown, True)
        
    def CreateDeleteButton(self, name, nameText):
        delete = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE, 4)
        delete.set_image(image)
        name.pack_start(delete, False)
        delete.connect('clicked', self.delete_clicked, nameText)
        
    def CreateChooserFilter(self, file_chooser):
        filter = gtk.FileFilter()
        filter.set_name('Images')
        filter.add_mime_type('image/png')
        filter.add_mime_type('image/jpeg')
        filter.add_mime_type('image/gif')
        filter.add_pattern('*.png')
        filter.add_pattern('*.svg')
        filter.add_pattern('*.jpg')
        filter.add_pattern('*.gif')
        file_chooser.add_filter(filter)
