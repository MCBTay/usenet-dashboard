import gtk
import operator
import xml.etree.ElementTree as ET
import xml.dom.minidom

class PreferencesWindow:
    pages = dict()
    configFile = None

    # Callbacks #
    def destroy_window(self, caller_widget):
        self.window.destroy()
        
    def file_selected(self, caller_widget, data):
        caller_widget.set_filename(data)
        
    def save_preferences(self, caller_widget):
        self.WriteConfig()
        self.window.destroy()
        # update main window -- reload button names, imgs if applicable
        
    # order is only passed for the name text entry as it is the key to our dictionary
    # name is passed in to know which record to update in the dictionary
    def entry_changed(self, caller_widget, order = None, name = None):
        newText = caller_widget.get_text()
        
        if order:
            page = self.findPageByOrder(int(order))
            # since we can't change keys, we'll have to create a new entry and delete the old one
            storedOrder = self.pages[page][0]
            storedUrl   = self.pages[page][1]
            storedImg   = self.pages[page][2]
            self.pages[newText] = [storedOrder, storedUrl, storedImg]
            for tempField in self.pages.keys():
                if tempField == page:
                    del(self.pages[tempField])
        else: 
            # so far URL is the only other case, so i'm handling it specifically
            self.pages[name][1] = newText
            
    def combobox_changed(self, caller_widget, name = None):
        # offset by one because get_active() returns the index of the active, not data
        newOrder = caller_widget.get_active() + 1 
        self.pages[name][0] = str(newOrder)
        
    def filechooser_changed(self, caller_widget, name = None):
        newImg = caller_widget.get_filename()
        self.pages[name][2] = newImg    
        
    def delete_clicked(self, caller_widget, nameText):
        labelString = 'Are you sure you want to delete your entry for ' + nameText + '?'
        dialog = gtk.Dialog('Are you sure?', None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialog.vbox.set_spacing(10)
        dialog.vbox.pack_start(gtk.Label(labelString))
        dialog.show_all()
        if (dialog.run() == gtk.RESPONSE_ACCEPT):
            if (self.pages[nameText]):
                print self.pages
                del(self.pages[nameText])
                print self.pages
                self.RedrawPreferences()
        dialog.destroy()
    # End Callbacks #
    
    def RedrawPreferences(self):
        for child in self.vbox.get_children():
            self.vbox.remove(child)
        self.CreatePreferences()
        self.vbox.show_all()
    
    def findPageByOrder(self, order):
        winner = None
        count = 1
        while count <= len(self.pages):
            for name in self.pages:
                pageOrder = self.pages[name][0]
                if int(pageOrder) == order:
                    winner = name
            count = count + 1 
        return winner
        
    def PrettyPrint(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.PrettyPrint(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    def WriteConfig(self):
        try:
            self.configFile = open('./config.xml', 'w+')
        except IOError:
            print "exception"
            
        root = ET.Element('pages')
        for name in self.pages:
            order = self.pages[name][0]
            url   = self.pages[name][1]
            img   = self.pages[name][2]
 
            pageNode = ET.SubElement(root, 'page')
            
            orderNode = ET.SubElement(pageNode, 'order')
            orderNode.text = order
            
            nameNode = ET.SubElement(pageNode, 'name')
            nameNode.text = name
            
            urlNode = ET.SubElement(pageNode, 'url')
            urlNode.text = url
            
            imgNode = ET.SubElement(pageNode, 'img')                        
            imgNode.text = img
        
        tree = ET.ElementTree(root)
        
        self.PrettyPrint(root)
        
        tree.write('./config.xml')
              
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
        save.connect('clicked', self.save_preferences)
        cancel = gtk.Button(stock = gtk.STOCK_CANCEL)
        cancel.connect('clicked', self.destroy_window)
        
        hbox.pack_start(gtk.Label(''), True, False)
        hbox.pack_start(save, False)
        hbox.pack_start(cancel, False)
        hbox.pack_start(gtk.Label(''), True, False)

        self.vbox.pack_start(hbox, False)
        self.vbox.pack_start(gtk.Label(''), False)
        
    def CreateOrderSelector(self, box, order, name):
        box.pack_start(gtk.Label('Order'), False)
        
        liststore = gtk.ListStore(str)
        orderDropdown = gtk.ComboBox()
        cell = gtk.CellRendererText()
        orderDropdown.pack_start(cell, True)
        orderDropdown.add_attribute(cell, 'text', 0)
        orderDropdown.connect('changed', self.combobox_changed, name)
        
        if len(self.pages) == 0:
            liststore.append([str(1)])
        else:
            count = 1
            while count <= len(self.pages):
                liststore.append([str(count)])
                count = count + 1
         
        orderDropdown.set_model(liststore)
        orderDropdown.set_active(int(order)-1)
        
        box.pack_start(orderDropdown, True)
        
    def CreateDeleteButton(self, name, nameText):
        delete = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE, 32)
        delete.set_image(image)
        name.pack_start(delete, False)
        delete.connect('clicked', self.delete_clicked, nameText)
        
    def CreateNameField(self, vbox, nameText, order):
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
        
    def CreateURLField(self, vbox, urlText, name):
        url = gtk.HBox()
        url.set_spacing(10)
        url.pack_start(gtk.Label(''), False)
        urlLabel = gtk.Label('URL')
        urlLabel.set_width_chars(5)
        urlEntry = gtk.Entry()
        urlEntry.connect('changed', self.entry_changed, None, name)
        urlEntry.set_text(urlText)
        url.pack_start(urlLabel, False)
        url.pack_start(urlEntry, True)
        url.pack_start(gtk.Label(''), False)
        vbox.pack_start(url, False)
    
    def CreateImagePicker(self, vbox, path, name):
        img = gtk.HBox()
        img.set_spacing(10)
        img.pack_start(gtk.Label(''), False)
        imgLabel = gtk.Label('Image')
        imgLabel.set_width_chars(5)
        imgChooser = gtk.FileChooserButton('Image')
        imgChooser.set_current_folder(".")
        imgChooser.connect('file-activated', self.file_selected, path)
        imgChooser.emit('file-activated')
        imgChooser.connect('file-set', self.filechooser_changed, name)
        img.pack_start(imgLabel, False)
        img.pack_start(imgChooser)
        img.pack_start(gtk.Label(''), False)
        vbox.pack_start(img, False)
           
    def CreatePageEntry(self, order, name, url, img):
        vbox = gtk.VBox()
        vbox.set_spacing(10)
        
        self.CreateNameField(vbox, name, order)
        self.CreateURLField(vbox, url, name)
        self.CreateImagePicker(vbox, img, name)        

        vbox.pack_start(gtk.HSeparator(), False)
        
        self.vbox.pack_start(vbox, False)
    
    def CreatePreferences(self):   
        
        self.vbox.pack_start(gtk.Label(''), False)
        
        if self.configFile:
            sorted_pages = sorted(self.pages.iteritems(), key=operator.itemgetter(1))
            for page in sorted_pages:
                pageName = page[0]
  
                order = self.pages[pageName][0]
                url   = self.pages[pageName][1]
                img   = self.pages[pageName][2]
                self.CreatePageEntry(order, pageName, url, img)
        else:
            self.CreatePageEntry('1', '', '', '.')
            
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

        self.ParseConfig()
        self.CreatePreferences()
        
        
        self.window.add(self.vbox)
        self.window.show_all()
