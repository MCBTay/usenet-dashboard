import os
import gtk, gobject
import operator
import xml.etree.ElementTree as ET
import xml.dom.minidom
import dashboard_common

class PreferencesWindow:
    pages = dict()
    page_entries = dict()
    count = 1
    entry_vbox = gtk.VBox(False, 0)

    # Callbacks #
    def destroy_window(self, caller_widget):
        self.window.destroy()
        
    def file_selected(self, caller_widget, data):
        caller_widget.set_filename(data)
        
    def save_preferences(self, caller_widget):
        dashboard_common.WriteConfig(self.pages)
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
        if name:
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
                del(self.pages[nameText])
                self.RemoveEntry(nameText)
        dialog.destroy()
        
    def add_clicked(self, caller_widget):
        labelString = 'What would you like to call the new site?'
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL, labelString)
        
        entry = gtk.Entry()
        entry.connect('activate', self.new_dialog_response, dialog, gtk.RESPONSE_OK)
        hbox = gtk.HBox()
        hbox.pack_start(entry)
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        response = dialog.run()
        new_site_name = ''
        if response == gtk.RESPONSE_OK:
            new_site_name = entry.get_text()
            entry.emit('activate')
        dialog.destroy()

    def new_dialog_response(self, caller_widget, dialog, response):
        new_site_name = caller_widget.get_text()
        if new_site_name != '':
            highest = 0
            for page in self.pages.keys():
                if int(self.pages[page][0]) > highest:
                    highest = int(self.pages[page][0])
            self.pages[new_site_name] = ['', '', '']
            self.CreatePageEntry(str(highest+1), new_site_name, '', '')    
            self.UpdateComboBoxes()  
            self.vbox.show_all()
        dialog.destroy()
    # End Callbacks #
    
    def UpdateComboBoxes(self):
        comboboxes = list()
        for entry in self.entry_vbox.get_children():
            for row in entry.get_children():
                for child in row.get_children():
                    if type(child) == gtk.ComboBox:
                        comboboxes.append(child)       
                break # combo box is always in first row of entry
                
        liststore = gtk.ListStore(str)
        count = 1
        while count <= len(comboboxes):
            liststore.append(str(count))
            count = count + 1
            
        for cb in comboboxes:
            oldactive = cb.get_active()
            cb.set_model(liststore)
            cb.set_active(oldactive)
    
    def RemoveEntry(self, name):
        if (self.page_entries[name]):
            self.entry_vbox.remove(self.page_entries[name])
        self.vbox.show_all()
        self.window.resize(1, 1)
    
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
        
    def CreateButton(self, text, icon):
        
        button = gtk.Button()
        hbox = gtk.HBox(False, 0)
        image = gtk.Image()
        image.set_from_stock(icon, 4)
        hbox.pack_start(image, False)
        hbox.pack_start(gtk.Label(' '), False)
        hbox.pack_start(gtk.Label(text), False)
        button.add(hbox)
        return button
        
        
    def CreateBottomButtons(self):
        hbox = gtk.HBox(False, 0)
        hbox.set_spacing(10)
        save = self.CreateButton('Save', gtk.STOCK_SAVE)
        save.connect('clicked', self.save_preferences)
        cancel = self.CreateButton('Cancel', gtk.STOCK_CANCEL)
        cancel.connect('clicked', self.destroy_window)
        add = self.CreateButton('Add New Page', gtk.STOCK_ADD)
        add.connect('clicked', self.add_clicked)
        
        hbox.pack_start(gtk.Label(''), True, False)
        hbox.pack_start(save, False)
        hbox.pack_start(cancel, False)
        hbox.pack_start(add, False)
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
        image.set_from_stock(gtk.STOCK_CLOSE, 4)
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
        if not urlText:
            urlText = ''
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
        
        self.entry_vbox.pack_start(vbox, False)
        self.page_entries[name] = vbox
    
    def CreatePreferences(self):   
        
        self.vbox.pack_start(gtk.Label(''), False)
        
        if self.pages:
            sorted_pages = sorted(self.pages.iteritems(), key=operator.itemgetter(1))
            for page in sorted_pages:
                pageName = page[0]
  
                order = self.pages[pageName][0]
                url   = self.pages[pageName][1]
                img   = self.pages[pageName][2]
                self.CreatePageEntry(order, pageName, url, img)
        else:
            self.CreatePageEntry('1', '', '', '.')
           
        self.vbox.pack_start(self.entry_vbox, False)
        self.CreateBottomButtons()
        
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title('Preferences')
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)

        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_default_size(500, 100)
        self.window.resize(1, 1)
        
        self.window.connect('destroy', self.destroy_window)
        self.vbox = gtk.VBox(False, 0)
        self.vbox.set_spacing(15)

        self.pages = dashboard_common.ParseConfig()
        self.CreatePreferences()
        
        
        self.window.add(self.vbox)
        self.window.show_all()
