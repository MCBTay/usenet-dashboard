import os
import gtk, gobject, glib
import operator
import xml.etree.ElementTree as ET
import xml.dom.minidom
import dashboard_common
import entry
    
class PreferencesWindow:
    configuration = dict()
    page_entries = dict()
    count = 1
    entry_vbox = gtk.VBox(False, 0)
    entry_vbox.set_spacing(10)

    # Callbacks #
    def destroy_window(self, caller_widget):
        self.window.destroy()
        
    def file_selected(self, caller_widget, data):
        caller_widget.set_filename(data)
        
    def save_preferences(self, caller_widget):
        dashboard_common.WriteConfig(self.configuration)
        self.window.destroy()
        # update main window -- reload button names, imgs if applicable
         
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
            for page in self.configuration['pages'].keys():
                if int(self.configuration['pages'][page][0]) > highest:
                    highest = int(self.configuration['pages'][page][0])
            self.configuration['pages'][new_site_name] = ['', '', '']
            self.CreatePageEntry(str(highest+1), new_site_name, '', '')    
            self.UpdateComboBoxes()  
            self.vbox.show_all()
        dialog.destroy()
        
    def filechooser_folder_changed(self, caller_widget, name):
        new_selection = caller_widget.get_filename()
        self.configuration['settings'][name] = new_selection  
        
    def filechooser_changed(self, caller_widget, name):
        new_selection = caller_widget.get_filename()
        self.configuration['settings'][name] = new_selection  
    # End Callbacks #
    
    
    # TODO: FINISH
    def UpdateComboBoxes(self):
        comboboxes = list()
        for entry in self.page_entries:
            hbox = self.page_entries[entry].get_children()[0]
            namerow = hbox.get_children()[1].get_children()[0]
            if type(entry) == gtk.ComboBox:
                comboboxes.append(child)       
           # break # combo box is always in first row of entry
                
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
        self.UpdateComboBoxes() 
        
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
        
    def CreatePageEntry(self, order, name, url, img):
        page_entry = entry.SiteEntry(self, order, name, url, img)
        vbox = gtk.VBox()
        vbox.set_spacing(10)
        vbox.pack_start(page_entry.entry_hbox, False, False)
        vbox.pack_start(gtk.HSeparator(), False)
        self.entry_vbox.pack_start(vbox, False, False)
        self.page_entries[name] = vbox
           
    def CreateSiteConfigurationTab(self, notebook):
        sites_config = gtk.Frame()
        sites_config.set_shadow_type(gtk.SHADOW_NONE)
        notebook.append_page(sites_config, gtk.Label('Website Configuration'))
        
        self.entry_vbox.pack_start(gtk.Label(''), False)
        if self.configuration['pages']:
            sorted_pages = sorted(self.configuration['pages'].iteritems(), key=operator.itemgetter(1))
            for page in sorted_pages:
                pageName = page[0]
                order = self.configuration['pages'][pageName][0]
                url   = self.configuration['pages'][pageName][1]
                img   = self.configuration['pages'][pageName][2]
                self.CreatePageEntry(order, pageName, url, img)
        else:
            self.CreatePageEntry('1', '', '', '.')
            
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_shadow_type(gtk.SHADOW_NONE)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        viewport = gtk.Viewport()
        viewport.set_shadow_type(gtk.SHADOW_NONE)
        viewport.add(self.entry_vbox)
        scrolled_window.add(viewport)
        sites_config.add(scrolled_window)
    
    def CreateGeneralOptionsTab(self, notebook):
        options = gtk.Frame()
        options.set_shadow_type(gtk.SHADOW_NONE)
        notebook.append_page(options, gtk.Label('General Options'))
        
        vbox = gtk.VBox()
        vbox.set_spacing(10)
        vbox.pack_start(gtk.Label(''), False)
        self.CreateDownloadsPathEntry(vbox, options)
        self.CreateLibsoupPathEntry(vbox, options)
        self.CreateLibwebkitPathEntry(vbox, options)
        options.add(vbox)
        
    def CreateDownloadsPathEntry(self, vbox, options):
        hbox = gtk.HBox()
        hbox.set_spacing(15)
        hbox.pack_start(gtk.Label(''), False)
        hboxLabel = gtk.Label('Downloads Path')
        hboxLabel.set_width_chars(13)
        downloadChooser = gtk.FileChooserButton('Downloads Path')
        downloadChooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        
        saved_path = self.configuration['settings']['downloadPath']
        if saved_path:
            downloadChooser.connect('file-activated', self.file_selected, saved_path)
            downloadChooser.emit('file-activated')
        
        downloadChooser.connect('selection-changed', self.filechooser_folder_changed, 'downloadPath')
        hbox.pack_start(hboxLabel, False)
        hbox.pack_start(downloadChooser)
        hbox.pack_start(gtk.Label(''), False)
        vbox.pack_start(hbox, False)
        
    def CreateLibsoupPathEntry(self, vbox, options):
        img = gtk.HBox()
        img.set_spacing(15)
        img.pack_start(gtk.Label(''), False)
        imgLabel = gtk.Label('libsoup Path')
        imgLabel.set_width_chars(13)
        imgChooser = gtk.FileChooserButton('libsoup Path')
        
        saved_path = self.configuration['settings']['libsoupPath']
        if saved_path:
            imgChooser.connect('file-activated', self.file_selected, saved_path)
            imgChooser.emit('file-activated')
            
        imgChooser.connect('file-set', self.filechooser_changed, 'libsoupPath')
        img.pack_start(imgLabel, False)
        img.pack_start(imgChooser)
        img.pack_start(gtk.Label(''), False)
        vbox.pack_start(img, False)
    
    def CreateLibwebkitPathEntry(self, vbox, options):
        img = gtk.HBox()
        img.set_spacing(15)
        img.pack_start(gtk.Label(''), False)
        imgLabel = gtk.Label('libwebkit Path')
        imgLabel.set_width_chars(13)
        imgChooser = gtk.FileChooserButton('libwebkit Path')
        
        saved_path = self.configuration['settings']['libwebkitPath']
        if saved_path:
            imgChooser.connect('file-activated', self.file_selected, saved_path)
            imgChooser.emit('file-activated')
        imgChooser.connect('file-set', self.filechooser_changed, 'libwebkitPath')
        img.pack_start(imgLabel, False)
        img.pack_start(imgChooser)
        img.pack_start(gtk.Label(''), False)
        vbox.pack_start(img, False)
        
    def CreatePreferences(self):             
        notebook = gtk.Notebook()
        self.CreateGeneralOptionsTab(notebook)
        self.CreateSiteConfigurationTab(notebook)  
        
        self.vbox.pack_start(notebook)
        self.CreateBottomButtons()
          
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title('Preferences')
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)
        self.window.set_size_request(450, 400)
        self.window.set_resizable(False)
        
        self.window.set_position(gtk.WIN_POS_CENTER)
        
        self.window.connect('destroy', self.destroy_window)
        self.vbox = gtk.VBox(False, 0)
        self.vbox.set_spacing(15)
        self.configuration = dashboard_common.ParseConfig()
        self.CreatePreferences()
        self.window.add(self.vbox)
        self.window.show_all()
