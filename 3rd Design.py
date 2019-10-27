# 3rd Design of GUI, barely interactable

from tkinter import *
from tkinter.ttk import Treeview, Scrollbar, Style


class MainWindow:

    def __init__(self, root):
        self.tab_list = list()

        # Sets Up window
        self.root = root
        pad = 100
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth()-pad, self.root.winfo_screenheight()-pad))
        self.window_dimensions = (self.root.winfo_screenwidth()-pad, self.root.winfo_screenheight()-pad)
        self.root.resizable(False, False)
        #self.root.state('zoomed')

        # Creates Main Containers
        self.tab_holder = Frame(self.root, width=self.window_dimensions[0], height=60, bg='#000000')
        self.mainFrame = Frame(self.root, width=self.window_dimensions[1], height=self.window_dimensions[1]-30, bg='#66ff33')
        self.contacts_tab = Canvas(self.tab_holder, width=150, height=60, bg='#CB4335', highlightthickness=0) # red
        self.groupings_tab = Canvas(self.tab_holder, width=150, height=50, bg='#F1C40F', highlightthickness=0) # yellow
        self.messaging_tab = Canvas(self.tab_holder, width=150, height=50, bg='#3498DB', highlightthickness=0) # blue

        # Layout Main Containers
        self.tab_holder.pack(fill='x')
        self.tab_holder.grid_rowconfigure(0, weight=0)
        self.tab_holder.grid_columnconfigure(0, weight=0)
        self.tab_holder.grid_columnconfigure(1, weight=0)
        self.tab_holder.grid_columnconfigure(2, weight=0)
        self.tab_holder.grid_columnconfigure(3, weight=1)
        self.tab_holder.grid_rowconfigure(2, weight=1)
        self.contacts_tab.grid(row=0, column=0, sticky='nw')
        self.tab_list.append(['ContactsPage', self.contacts_tab])
        self.groupings_tab.grid(row=0, column=1, sticky='nw')
        self.tab_list.append(['GroupingsPage', self.groupings_tab])
        self.messaging_tab.grid(row=0, column=2, sticky='nw')
        self.tab_list.append(['MessagingPage', self.messaging_tab])

        self.mainFrame.pack(fill='both', side='bottom', expand='True')
        self.mainFrame.grid_rowconfigure(0, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=1)

        # Create Frames in mainFrame
        self.frames = dict()
        for F in (ContactsPage, GroupingsPage, MessagingPage):
            page_name = F.__name__
            frame = F(parent=self.mainFrame, controller=self)
            self.frames[page_name] = frame

            # Stacks frames on top of one another, raises whichever is on screen
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ContactsPage")

        # Create Widgets
        self.contacts_tab_title = self.contacts_tab.create_text(5, 20, anchor='nw')
        self.groupings_tab_title = self.groupings_tab.create_text(5, 20, anchor='nw')
        self.messaging_tab_title = self.messaging_tab.create_text(5, 20, anchor='nw')

        # Layout Widgets
        self.contacts_tab.itemconfig(self.contacts_tab_title, font=('Helvetica', 18), text='Contacts')
        self.groupings_tab.itemconfig(self.groupings_tab_title, font=('Helvetica', 18), text='Groupings')
        self.messaging_tab.itemconfig(self.messaging_tab_title, font=('Helvetica', 18), text='Messaging')

        # Key Bindings
        self.contacts_tab.bind('<ButtonPress-1>', self.select_tab)
        self.groupings_tab.bind('<ButtonPress-1>', self.select_tab)
        self.messaging_tab.bind('<ButtonPress-1>', self.select_tab)

    def select_tab(self, event):
        """INCREASES SELECTED TAB BOTTOM AND MOVES UP SELECTED FRAME"""
        if event.widget.winfo_height() == 50:
            for tab in self.tab_list:
                if tab[1].winfo_height() != 50:
                    tab[1].config(height=50)
                if tab[1] == event.widget:
                    self.show_frame(tab[0])
            event.widget.config(height=event.widget.winfo_height()+10)
        # for tab in self.tab_list:
        #     if tab[1] == event.widget:
        #         self.show_frame(tab[0])
        #         event.widget.config(highlightthickness=0)
        #     else:
        #         tab[1].config(highlightthickness=1)



    def show_frame(self, page_name):
        """MOVES UP NAMED FRAME"""
        frame = self.frames[page_name]
        frame.tkraise()


class ContactsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='#FFA500')
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.search_entry = Entry(self, borderwidth=1, font=('TimesNewRoman', 20), justify='center')
        self.search_entry.insert(0, 'Search Contacts')
        self.search_entry.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        self.add_contact_button = Button(self, text='+ Add Contact', font=('Courier', 15), width=16, height=2, command=self.add_contact_popup)
        self.add_contact_button.grid(row=1, column=0, padx=25, pady=10, sticky='e')

        self.select_all_button = Button(self, text='Select All', command=lambda: print('CONTACTS - SELECT ALL'))
        self.select_all_button.grid(row=2, column=0, padx=25, pady=5, sticky='e')

        contact_list_frame = Frame(self)
        contact_list_frame.grid(row=3, column=0, padx=25, pady=30, sticky='nsew')
        contact_list_frame.grid_rowconfigure(0, weight=1)
        contact_list_frame.grid_columnconfigure(0, weight=1)

        self.contacts_list_tree = Treeview(contact_list_frame, columns=('one', 'two', 'three', 'four', 'five'))
        self.contacts_list_tree.heading('#0', text='Name', anchor=W)
        self.contacts_list_tree.heading('one', text='Company', anchor=W)
        self.contacts_list_tree.heading('two', text='Job Title', anchor=W)
        self.contacts_list_tree.heading('three', text='Email', anchor=W)
        self.contacts_list_tree.heading('four', text='Phone', anchor=W)
        self.contacts_list_tree.heading('five', text='Notes', anchor=W)
        self.contacts_list_tree.grid(row=0, column=0, sticky='nsew')
        self.add_contact_list_tree_elements()

        self.y_contacts_scrollbar = Scrollbar(contact_list_frame, orient='vertical', command=self.contacts_list_tree.yview)
        self.y_contacts_scrollbar.grid(row=0, column=1, sticky='nes')
        self.contacts_list_tree.configure(yscroll=self.y_contacts_scrollbar.set)

        self.contacts_list_tree.bind('<Button-1>', self.prevent_resize)
        self.contacts_list_tree.bind('<Motion>', self.prevent_resize)

    def add_contact_list_tree_elements(self):
        """TEMPORARY: ADDS A BUNCH OF FAKE CONTACTS TO CONTACT LIST"""
        for i in range(1, 25):
            contact = self.contacts_list_tree.insert('', 'end', text='MyName'+str(i), values=('MyCompanyName'+str(i), 'MyJob'+str(i), 'MyEmail'+str(i), 'MyPhone'+str(i), 'MyNotes'+str(i)))
            if i % 2 == 0:
                self.contacts_list_tree.item(contact, tags=('even',))
            else:
                self.contacts_list_tree.item(contact, tags=('odd',))

        self.contacts_list_tree.tag_configure('odd', background='#E8E8E8')
        self.contacts_list_tree.tag_configure('even', background='#F5F5F5')

    def add_contact_popup(self):
        """CREATES TRANSPARENCY/SHADOW ON TOP OF GROUPINGS TAB
        AND A WINDOW TO ADD GROUPINGS"""
        self.popup_frame = Frame(self.master, width=900, height=500, bg='#FF0000', highlightthickness=2, highlightbackground='#000000')
        self.popup_frame.grid(row=0, column=0)
        self.delete_popup_funcid = self.master.bind_all('<Button-1>', self.delete_popup)

        title_canvas = Canvas(self.popup_frame, width=900, height=50, highlightthickness=0)
        title_canvas.grid(row=0, sticky='new')
        popup_title = title_canvas.create_text(5, 5, anchor='nw')
        title_canvas.itemconfig(popup_title, font=('Helvetica', 20, 'bold', 'underline'), text=' New Contact ')



    def delete_popup(self, event):
        """Destroys Pop Up Frame and its binding id if Mouse 1 clicks outside frame"""
        # turning a wdiget into str returns the path of the widget
        # to check if widget is child, grandchild, etc of another widget, just check if their starting paths are equal
        if not str(self.master.winfo_containing(event.x_root, event.y_root)).startswith(str(self.popup_frame)):
            self.popup_frame.destroy()
            self.master.unbind('<Button-1>', self.delete_popup_funcid)
            del self.delete_popup_funcid
            print('pop up deleted')


    def prevent_resize(self, event):
        """PREVENTS THE RESIZING OF COLUMNS IN contact_list_tree"""
        if self.winfo_containing(event.x_root, event.y_root).identify_region(event.x, event.y) == 'separator':
            return 'break'


class GroupingsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='#ff69b4')
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.search_entry = Entry(self, borderwidth=1, font=('TimesNewRoman', 20), justify='center')
        self.search_entry.insert(0, 'Search Groupings')
        self.search_entry.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        self.add_contact_button = Button(self, text='+ Add Grouping', font=('Courier', 15), width=16, height=2, command=self.add_grouping_popup)
        self.add_contact_button.grid(row=1, column=0, padx=25, pady=10, sticky='e')

        self.select_all_button = Button(self, text='Select All', command=lambda: print('GROUPINGS - SELECT ALL'))
        self.select_all_button.grid(row=2, column=0, padx=25, pady=5, sticky='e')

        groupings_list_frame = Frame(self)
        groupings_list_frame.grid(row=3, column=0, padx=25, pady=30, sticky='nsew')
        groupings_list_frame.grid_rowconfigure(0, weight=1)
        groupings_list_frame.grid_columnconfigure(0, weight=1)

        self.groupings_list_tree = Treeview(groupings_list_frame, columns=('one', 'two'))
        self.groupings_list_tree.heading('#0', text='Grouping Name', anchor=W)
        self.groupings_list_tree.heading('one', text='Number of Members', anchor=W)
        self.groupings_list_tree.heading('two', text='Description', anchor=W)
        self.groupings_list_tree.grid(row=0, column=0, sticky='nsew')
        self.add_groupings_list_elements()

        self.y_groupings_scrollbar = Scrollbar(groupings_list_frame, orient='vertical', command=self.groupings_list_tree.yview)
        self.y_groupings_scrollbar.grid(row=0, column=1, sticky='nes')
        self.groupings_list_tree.configure(yscroll=self.y_groupings_scrollbar.set)

        self.groupings_list_tree.bind('<Button-1>', self.prevent_resize)
        self.groupings_list_tree.bind('<Motion>', self.prevent_resize)

    def add_groupings_list_elements(self):
        """TEMPORARY: ADDS A BUNCH OF FAKE GROUPINGS TO groupings_list_tree"""
        for i in range(1, 25):
            group = self.groupings_list_tree.insert('', 'end', text='MyGrouping' + str(i), values=('4', 'MyDescription' + str(i)))
            if i % 2 == 0:
                self.groupings_list_tree.item(group, tags=('even',))
            else:
                self.groupings_list_tree.item(group, tags=('odd',))
            for j in range(1, 5):
                self.groupings_list_tree.insert(group, 'end', text='MyContact'+str(j), values=('', 'MyContactNotes'+str(j)))

        self.groupings_list_tree.tag_configure('odd', background='#E8E8E8')
        self.groupings_list_tree.tag_configure('even', background='#F5F5F5')

    def prevent_resize(self, event):
        """PREVENTS THE RESIZING OF COLUMNS IN groupings_list_tree"""
        if self.winfo_containing(event.x_root, event.y_root).identify_region(event.x, event.y) == 'separator':
            return 'break'

    def add_grouping_popup(self):
        """CREATES TRANSPARENCY/SHADOW ON TOP OF GROUPINGS TAB
        AND A WINDOW TO ADD GROUPINGS"""
        self.popup_frame = Frame(self.master, width=900, height=500, bg='#FF0000', highlightthickness=2, highlightbackground='#000000')
        self.popup_frame.grid(row=0, column=0)
        self.delete_popup_funcid = self.master.bind_all('<Button-1>', self.delete_popup)

        title_canvas = Canvas(self.popup_frame, width=900, height=50, highlightthickness=0)
        title_canvas.grid(row=0, sticky='new')
        popup_title = title_canvas.create_text(5, 5, anchor='nw')
        title_canvas.itemconfig(popup_title, font=('Helvetica', 20, 'bold', 'underline'), text=' New Grouping ')

        information_frame = Frame(self.popup_frame, width=900)
        information_frame.grid_columnconfigure(0, weight=0)
        information_frame.grid_columnconfigure(1, weight=1)
        information_frame.grid(row=1, column=0, sticky='ew')

        name_canvas = Canvas(information_frame, width=100, height=30, highlightthickness=0)
        name_canvas.grid(row=0, column=0, sticky='w')
        name_title = name_canvas.create_text(10, 1, anchor='nw')
        name_canvas.itemconfig(name_title, font=('TimesNewRoman', 15), text='Name:')
        name_entry = Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')
        name_entry.grid(row=0, column=1, sticky='ew', padx=15)

        description_canvas = Canvas(information_frame, width=220, height=30, highlightthickness=0)
        description_canvas.grid(row=1, column=0, sticky='w')
        description_title = description_canvas.create_text(10, 1, anchor='nw')
        description_canvas.itemconfig(description_title, font=('TimesNewRoman', 15), text='Description (Optional):')
        description_entry = Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')
        description_entry.grid(row=1, column=1, sticky='ew', padx=15)

        members_frame = Frame(self.popup_frame, width=900)
        members_frame.grid(row=2, column=0, sticky='ew')

        members_canvas = Canvas(members_frame, width=900, height=50, highlightthickness=0)
        members_canvas.grid(row=0, column=0, sticky='ew', pady=10)
        members_title = members_canvas.create_text(10, 20, anchor='nw')
        members_canvas.itemconfig(members_title, font=('TimesNewRoman', 18, 'underline'), text='Members:')

        import_excel_button = Button(members_frame, text='Import from Excel', font=('Courier', 14), command=lambda: print('GROUPINGS - POPUP - IMPORT FROM EXCEL'))
        import_excel_button.grid(row=0, column=0, sticky='e', padx=20)

        search_contacts_entry = Entry(members_frame, borderwidth=1, font=('TimesNewRoman', 20), justify='center')
        search_contacts_entry.insert(0, 'Search Contacts')
        search_contacts_entry.grid(row=1, column=0, sticky='ew', padx=20)

        tables_frame = Frame(members_frame, width=900)
        tables_frame.grid(row=3, column=0, sticky='ew', pady=(0, 20))

        contacts_table_canvas = Canvas(tables_frame, width=900, height=30, highlightthickness=0)
        contacts_table_canvas.grid(row=0, column=0, sticky='ew', pady=10)
        contacts_table_title = contacts_table_canvas.create_text(15, 1, anchor='nw')
        contacts_table_canvas.itemconfig(contacts_table_title, font=('TimesNewRoman', 15, 'underline'), text='From Contacts:')

        contacts_table_frame = Frame(tables_frame, width=900)
        contacts_table_frame.grid(row=1, column=0, sticky='ew', padx=40)

        contacts_table = Treeview(contacts_table_frame, columns=('one', 'two', 'three', 'four', 'five', 'six'))
        contacts_table.column('#0', stretch=False, width=150) # width out of 800
        contacts_table.heading('#0', text='Name', anchor=W)
        contacts_table['height'] = 6
        for columnIndex in range(len(contacts_table['columns'])-1):
            column_name = contacts_table['columns'][columnIndex]
            text_name = ('Company', 'Job Title', 'Email', 'Phone', 'Notes')[columnIndex]
            contacts_table.column(column_name, stretch=False, width=124)
            contacts_table.heading(column_name, text=text_name, anchor=W)
        contacts_table.column('six', stretch=False, width=30)
        contacts_table.heading('six', text='Add', anchor=W)
        contacts_table.grid(row=0, column=0, sticky='w')

        y_contacts_scrollbar = Scrollbar(contacts_table_frame, orient='vertical', command=contacts_table.yview)
        y_contacts_scrollbar.grid(row=0, column=1, sticky='nsw')
        # x_contacts_scrollbar = Scrollbar(contacts_table_frame, orient='horizontal', command=contacts_table.xview)
        # x_contacts_scrollbar.grid(row=1, column=0, sticky='ew')
        contacts_table.configure(yscroll=y_contacts_scrollbar.set)#, xscroll=x_contacts_scrollbar.set)

        members_table_canvas = Canvas(tables_frame, width=900, height=30, highlightthickness=0)
        members_table_canvas.grid(row=2, column=0, sticky='w', pady=10)
        members_table_title = members_table_canvas.create_text(15, 1, anchor='nw')
        members_table_canvas.itemconfig(members_table_title, font=('TimesNewRoman', 15, 'underline'), text='Added Members:')

        members_table_frame = Frame(tables_frame, width=900)
        members_table_frame.grid(row=3, column=0, sticky='w', padx=40)

        members_table = Treeview(members_table_frame, columns=('one', 'two', 'three', 'four', 'five', 'six'))
        members_table.column('#0', stretch=False, width=150) # width out of 800
        members_table.heading('#0', text='Name', anchor=W)
        members_table['height'] = 6
        for columnIndex in range(len(members_table['columns'])-1):
            column_name = members_table['columns'][columnIndex]
            text_name = ('Company', 'Job Title', 'Email', 'Phone', 'Notes')[columnIndex]
            members_table.column(column_name, stretch=False, width=124)
            members_table.heading(column_name, text=text_name, anchor=W)
        members_table.column('six', stretch=False, width=30)
        members_table.heading('six', text='Remove', anchor=W)
        members_table.grid(row=0, column=0, sticky='w')

        y_members_scrollbar = Scrollbar(members_table_frame, orient='vertical', command=members_table.yview)
        y_members_scrollbar.grid(row=0, column=1, sticky='nsw')
        members_table.configure(yscroll=y_members_scrollbar.set)

        contacts_table.bind('<Button-1>', self.prevent_resize)
        contacts_table.bind('<Motion>', self.prevent_resize)
        members_table.bind('<Button-1>', self.prevent_resize)
        members_table.bind('<Motion>', self.prevent_resize)



    def delete_popup(self, event):
        """Destroys Pop Up Frame and its binding id if Mouse 1 clicks outside frame"""
        # turning a wdiget into str returns the path of the widget
        # to check if widget is child, grandchild, etc of another widget, just check if their starting paths are equal
        if not str(self.master.winfo_containing(event.x_root, event.y_root)).startswith(str(self.popup_frame)):
            self.popup_frame.destroy()
            self.master.unbind('<Button-1>', self.delete_popup_funcid)
            del self.delete_popup_funcid
            print('pop up deleted')


class MessagingPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='#800080')
        self.controller = controller





if __name__ == '__main__':
    root = Tk()
    window = MainWindow(root)
    root.mainloop()
