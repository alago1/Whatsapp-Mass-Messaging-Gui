# 3rd Design of GUI, almost complete UI

__author__ = 'Allan Dolago'
__version__ = '0.0'
import tkinter as tk
from tkinter import ttk

class MainWindow:

    def __init__(self, root):
        self._tab_list = list()
        self._contact_list = list()
        self._groupings_list = list()
        self.fetch_contact_list()
        self.fetch_groupings_list()

        # Sets Up window
        self._root = root
        # pad = 100
        # self._root.geometry("{0}x{1}+0+0".format(self._root.winfo_screenwidth()-pad, self._root.winfo_screenheight()-pad))
        # self._window_dimensions = (self._root.winfo_screenwidth()-pad, self._root.winfo_screenheight()-pad)
        # self._root.resizable(False, False)
        self._root.state('zoomed')

        # Creates Main Containers
        self._tab_holder = tk.Frame(self._root, height=60, bg='#000000')
        self._mainFrame = tk.Frame(self._root, bg='#66ff33')
        self._contacts_tab = tk.Canvas(self._tab_holder, width=150, height=60, bg='#CB4335', highlightthickness=0) # red
        self._groupings_tab = tk.Canvas(self._tab_holder, width=150, height=50, bg='#F1C40F', highlightthickness=0) # yellow
        self._messaging_tab = tk.Canvas(self._tab_holder, width=150, height=50, bg='#3498DB', highlightthickness=0) # blue

        # Layout Main Containers
        self._tab_holder.grid(row=0, column=0, sticky='new')
        self._contacts_tab.grid(row=0, column=0, sticky='nw')
        self._tab_list.append(['ContactsPage', self._contacts_tab])
        self._groupings_tab.grid(row=0, column=1, sticky='nw')
        self._tab_list.append(['GroupingsPage', self._groupings_tab])
        self._messaging_tab.grid(row=0, column=2, sticky='nw')
        self._tab_list.append(['MessagingPage', self._messaging_tab])

        self._mainFrame.grid(row=1, column=0, sticky='nsew')
        self._mainFrame.grid_rowconfigure(0, weight=1)
        self._mainFrame.grid_columnconfigure(0, weight=1)

        # Create Frames in mainFrame
        self._frames = dict()
        for F in (ContactsPage, GroupingsPage, MessagingPage):
            page_name = F.__name__
            frame = F(parent=self._mainFrame, controller=self)
            self._frames[page_name] = frame

            # Stacks frames on top of one another, raises whichever is on screen
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ContactsPage")


        # Create Widgets
        self._contacts_tab_title = self._contacts_tab.create_text(5, 20, anchor='nw')
        self._groupings_tab_title = self._groupings_tab.create_text(5, 20, anchor='nw')
        self._messaging_tab_title = self._messaging_tab.create_text(5, 20, anchor='nw')


        # Layout Widgets
        self._contacts_tab.itemconfig(self._contacts_tab_title, font=('Helvetica', 18), text='Contacts')
        self._groupings_tab.itemconfig(self._groupings_tab_title, font=('Helvetica', 18), text='Groupings')
        self._messaging_tab.itemconfig(self._messaging_tab_title, font=('Helvetica', 18), text='Messaging')


        # Grid Resizing
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        self._tab_holder.grid_rowconfigure(0, weight=0)
        self._tab_holder.grid_columnconfigure(0, weight=0)
        self._tab_holder.grid_columnconfigure(1, weight=0)
        self._tab_holder.grid_columnconfigure(2, weight=0)
        self._tab_holder.grid_columnconfigure(3, weight=1)
        self._tab_holder.grid_rowconfigure(2, weight=1)


        # Key Bindings
        self._contacts_tab.bind('<ButtonPress-1>', self.select_tab)
        self._groupings_tab.bind('<ButtonPress-1>', self.select_tab)
        self._messaging_tab.bind('<ButtonPress-1>', self.select_tab)

    def select_tab(self, event):
        """INCREASES SELECTED TAB BOTTOM AND MOVES UP SELECTED FRAME"""
        if event.widget.winfo_height() == 50:
            for tab in self._tab_list:
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
        frame = self._frames[page_name]
        frame.tkraise()

    def get_contact_list(self):
        return self._contact_list

    def get_groupings_list(self):
        return self._groupings_list

    def set_contact_list(self, contact_list):
        self._contact_list = contact_list

    def set_groupings_list(self, groupings_list):
        self._groupings_list = groupings_list

    def fetch_contact_list(self):
        """TEMPORARY: Adds a bunch of fake contacts to contacts list"""
        for i in range(1, 25):
            self._contact_list.append(['MyName'+str(i), 'MyCompanyName'+str(i), 'MyJob'+str(i), 'MyEmail'+str(i), 'MyPhone'+str(i), 'MyNotes'+str(i)])

    def fetch_groupings_list(self):
        """TEMPORARY: Adds a bunch of fake groupings and contacts to groupings list"""
        for i in range(1, 25):
            grouping = list()
            for j in range(1, 5):
                grouping.append(['MyContact'+str(j), 'MyContactNotes'+str(j)])
            self._groupings_list.append(['MyGrouping'+str(i), 'MyDescription'+str(i), grouping])

'''==========================='''
'''====== FRAME CLASSES ======'''
'''==========================='''
class ContactsPage(tk.Frame):

    def __init__(self, parent, controller):
        # Tab Backend Set Up
        tk.Frame.__init__(self, parent, bg='#FFA500')
        self._controller = controller


        # Initialize Widgets
        self._search_entry = SearchEntry(self, borderwidth=1, font=('TimesNewRoman', 20), justify='center', idleText='Search Contacts')
        self._add_contact_button = tk.Button(self, text='+ Add Contact', font=('Courier', 15), width=16, height=2, command=self.add_contact_popup)
        self._select_all_button = tk.Button(self, text='Select All', command=lambda: print('CONTACTS - SELECT ALL'))

        contact_list_frame = tk.Frame(self)
        self._contacts_list_tree = ttk.Treeview(contact_list_frame, columns=('one', 'two', 'three', 'four', 'five'))
        self._y_contacts_scrollbar = ttk.Scrollbar(contact_list_frame, orient='vertical', command=self._contacts_list_tree.yview)


        # Setting up Grid
        self._search_entry.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        self._add_contact_button.grid(row=1, column=0, padx=25, pady=10, sticky='e')
        self._select_all_button.grid(row=2, column=0, padx=25, pady=5, sticky='e')

        contact_list_frame.grid(row=3, column=0, padx=25, pady=30, sticky='nsew')
        self._contacts_list_tree.grid(row=0, column=0, sticky='nsew')
        self._y_contacts_scrollbar.grid(row=0, column=1, sticky='nes')


        # Widget Post-Inialization Configuration
        self._contacts_list_tree.heading('#0', text='Name', anchor='w')
        self._contacts_list_tree.heading('one', text='Company', anchor='w')
        self._contacts_list_tree.heading('two', text='Job Title', anchor='w')
        self._contacts_list_tree.heading('three', text='Email', anchor='w')
        self._contacts_list_tree.heading('four', text='Phone', anchor='w')
        self._contacts_list_tree.heading('five', text='Notes', anchor='w')
        self._contacts_list_tree.configure(yscroll=self._y_contacts_scrollbar.set)
        self.add_contact_list_tree_elements()

        self._search_entry.linkTree(self._contacts_list_tree)


        # Grid Resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        contact_list_frame.grid_rowconfigure(0, weight=1)
        contact_list_frame.grid_columnconfigure(0, weight=1)


        # Widget Key Binding
        self._contacts_list_tree.bind('<Button-1>', self.prevent_resize)
        self._contacts_list_tree.bind('<Motion>', self.prevent_resize)

    def add_contact_list_tree_elements(self):
        """Adds elements from main_windows contact_list to the tree in contacts tab
        Also sets up so tag for evens and odds for coloring"""
        i = 0
        for contact in self._controller.get_contact_list():
            contact_refer = self._contacts_list_tree.insert('', 'end', text=contact[0], values=(contact[1], contact[2], contact[3], contact[4], contact[5]))
            if i % 2 == 0:
                self._contacts_list_tree.item(contact_refer, tags=('even',))
            else:
                self._contacts_list_tree.item(contact_refer, tags=('odd',))
            i += 1

        self._contacts_list_tree.tag_configure('odd', background='#E8E8E8')
        self._contacts_list_tree.tag_configure('even', background='#F5F5F5')

    def add_contact_popup(self):
        """CREATES FRAME ON TOP OF CONTACTS TAB
        WITH A POPUP TO ADD GROUPINGS"""
        # Initialize Widgets
        self._popup_frame = tk.Frame(self.master, width=900, height=500, bg='#FF0000', highlightthickness=2, highlightbackground='#000000')
        title_canvas = tk.Canvas(self._popup_frame, width=900, height=50, highlightthickness=0)
        import_excel_button = tk.Button(self._popup_frame, text='Import from Excel', font=('Courier', 14),
                                        command=lambda: print('CONTACTS - POPUP - IMPORT FROM EXCEL'))

        information_frame = tk.Frame(self._popup_frame)
        name_canvas = tk.Canvas(information_frame, width=100, height=30, highlightthickness=0)
        name_entry = tk.Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')
        company_canvas = tk.Canvas(information_frame, width=100, height=30, highlightthickness=0)
        company_entry = tk.Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')
        job_title_canvas = tk.Canvas(information_frame, width=100, height=30, highlightthickness=0)
        job_title_entry = tk.Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')
        email_canvas = tk.Canvas(information_frame, width=100, height=30, highlightthickness=0)
        email_entry = tk.Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')
        phone_canvas = tk.Canvas(information_frame, width=100, height=30, highlightthickness=0)
        phone_entry = tk.Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')
        notes_canvas = tk.Canvas(information_frame, width=100, height=30, highlightthickness=0)
        notes_entry = tk.Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')

        add_contact_button = tk.Button(self._popup_frame, text='Add', width=10, font=('Courier', 14),
                                       command=lambda: print('CONTACTS - POPUP - ADD BUTTON'))


        # Setting up Grid
        self._popup_frame.grid(row=0, column=0)
        title_canvas.grid(row=0, sticky='new')
        import_excel_button.grid(row=1, column=0, sticky='e', padx=20)

        information_frame.grid(row=2, column=0, sticky='nsew', pady=10)
        name_canvas.grid(row=0, column=0, sticky='w')
        name_entry.grid(row=0, column=1, sticky='ew', padx=15)
        company_canvas.grid(row=1, column=0, sticky='w')
        company_entry.grid(row=1, column=1, sticky='ew', padx=15)
        job_title_canvas.grid(row=2, column=0, sticky='w')
        job_title_entry.grid(row=2, column=1, sticky='ew', padx=15)
        email_canvas.grid(row=3, column=0, sticky='w')
        email_entry.grid(row=3, column=1, sticky='ew', padx=15)
        phone_canvas.grid(row=4, column=0, sticky='w')
        phone_entry.grid(row=4, column=1, sticky='ew', padx=15)
        notes_canvas.grid(row=5, column=0, sticky='w')
        notes_entry.grid(row=5, column=1, sticky='ew', padx=15)

        add_contact_button.grid(row=3, column=0, sticky='e', padx=20, pady=(0, 10))


        # Widget Post_Initialization Configuration
        popup_title = title_canvas.create_text(5, 5, anchor='nw')
        title_canvas.itemconfig(popup_title, font=('Helvetica', 20, 'bold', 'underline'), text=' New Contact ')
        name_title = name_canvas.create_text(10, 1, anchor='nw')
        name_canvas.itemconfig(name_title, font=('TimesNewRoman', 15), text='Name:')
        company_title = company_canvas.create_text(10, 1, anchor='nw')
        company_canvas.itemconfig(company_title, font=('TimesNewRoman', 15), text='Company:')
        job_title_title = job_title_canvas.create_text(10, 1, anchor='nw')
        job_title_canvas.itemconfig(job_title_title, font=('TimesNewRoman', 15), text='Job Title:')
        email_title = email_canvas.create_text(10, 1, anchor='nw')
        email_canvas.itemconfig(email_title, font=('TimesNewRoman', 15), text='Email:')
        phone_title = phone_canvas.create_text(10, 1, anchor='nw')
        phone_canvas.itemconfig(phone_title, font=('TimesNewRoman', 15), text='Phone:')
        notes_title = notes_canvas.create_text(10, 1, anchor='nw')
        notes_canvas.itemconfig(notes_title, font=('TimesNewRoman', 15), text='Notes:')


        # Grid Resizing
        information_frame.grid_columnconfigure(1, weight=1)


        # Widget Key Bindings
        self._delete_popup_funcid = self.master.bind_all('<Button-1>', self.delete_popup)

    def delete_popup(self, event):
        """Destroys Pop Up Frame and its binding id if Mouse 1 clicks outside frame"""
        # turning a widget into str returns the path of the widget
        # to check if widget is descendant of another widget, just check if their starting paths are equal
        if not str(self.master.winfo_containing(event.x_root, event.y_root)).startswith(str(self._popup_frame)):
            self._popup_frame.destroy()
            self.master.unbind('<Button-1>', self._delete_popup_funcid)
            del self._delete_popup_funcid

    def prevent_resize(self, event):
        """PREVENTS THE RESIZING OF COLUMNS IN contact_list_tree"""
        if self.winfo_containing(event.x_root, event.y_root).identify_region(event.x, event.y) == 'separator':
            return 'break'


class GroupingsPage(tk.Frame):

    def __init__(self, parent, controller):
        # Tab Backend Set up
        tk.Frame.__init__(self, parent, bg='#ff69b4')
        self._controller = controller


        # Initialize Widgets
        self._search_entry = SearchEntry(self, borderwidth=1, font=('TimesNewRoman', 20), justify='center', idleText='Search Groupings')
        self._add_contact_button = tk.Button(self, text='+ Add Grouping', font=('Courier', 15), width=16, height=2, command=self.add_grouping_popup)
        self._select_all_button = tk.Button(self, text='Select All', command=lambda: print('GROUPINGS - SELECT ALL'))

        groupings_list_frame = tk.Frame(self)
        self._groupings_list_tree = ttk.Treeview(groupings_list_frame, columns=('one', 'two'))
        self._y_groupings_scrollbar = ttk.Scrollbar(groupings_list_frame, orient='vertical', command=self._groupings_list_tree.yview)


        # Setting up Grid
        self._search_entry.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        self._add_contact_button.grid(row=1, column=0, padx=25, pady=10, sticky='e')
        self._select_all_button.grid(row=2, column=0, padx=25, pady=5, sticky='e')

        groupings_list_frame.grid(row=3, column=0, padx=25, pady=30, sticky='nsew')
        self._groupings_list_tree.grid(row=0, column=0, sticky='nsew')
        self._y_groupings_scrollbar.grid(row=0, column=1, sticky='nes')


        # Widget Post-Initialization Configuration
        self._groupings_list_tree.heading('#0', text='Grouping Name', anchor='w')
        self._groupings_list_tree.heading('one', text='Number of Members', anchor='w')
        self._groupings_list_tree.heading('two', text='Description', anchor='w')
        self._groupings_list_tree.configure(yscroll=self._y_groupings_scrollbar.set)
        self.add_groupings_list_elements()

        self._search_entry.linkTree(self._groupings_list_tree)


        # Grid Resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        groupings_list_frame.grid_rowconfigure(0, weight=1)
        groupings_list_frame.grid_columnconfigure(0, weight=1)


        # Widget Key Bindings
        self._groupings_list_tree.bind('<Button-1>', self.prevent_resize)
        self._groupings_list_tree.bind('<Motion>', self.prevent_resize)

    def add_groupings_list_elements(self):
        """Adds elements from main_window's groupings_list to the tree in groupings tab"""
        i = 0
        for grouping in self._controller.get_groupings_list():
            group = self._groupings_list_tree.insert('', 'end', text=grouping[0], values=(len(grouping[2]), grouping[1]))
            if i % 2 == 0:
                self._groupings_list_tree.item(group, tags=('even',))
            else:
                self._groupings_list_tree.item(group, tags=('odd',))
            for contact in grouping[2]:
                self._groupings_list_tree.insert(group, 'end', text=contact[0], values=('', contact[1]))
            i += 1

        self._groupings_list_tree.tag_configure('odd', background='#E8E8E8')
        self._groupings_list_tree.tag_configure('even', background='#F5F5F5')

    def prevent_resize(self, event):
        """PREVENTS THE RESIZING OF COLUMNS IN groupings_list_tree"""
        if self.winfo_containing(event.x_root, event.y_root).identify_region(event.x, event.y) == 'separator':
            return 'break'

    def add_grouping_popup(self):
        """CREATES A FRAME ON TOP OF GROUPINGS TAB
        WITH A POPUP TO ADD GROUPINGS"""
        # Initialize Widgets
        self._popup_frame = tk.Frame(self.master, width=900, height=500, bg='#FF0000', highlightthickness=2, highlightbackground='#000000')
        title_canvas = tk.Canvas(self._popup_frame, width=900, height=50, highlightthickness=0)

        information_frame = tk.Frame(self._popup_frame, width=900)
        name_canvas = tk.Canvas(information_frame, width=100, height=30, highlightthickness=0)
        name_entry = tk.Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')
        description_canvas = tk.Canvas(information_frame, width=220, height=30, highlightthickness=0)
        description_entry = tk.Entry(information_frame, borderwidth=1, font=('Arial', 15), relief='ridge')

        members_frame = tk.Frame(self._popup_frame, width=900)
        members_canvas = tk.Canvas(members_frame, width=900, height=50, highlightthickness=0)
        import_excel_button = tk.Button(members_frame, text='Import from Excel', font=('Courier', 14),
                                        command=lambda: print('GROUPINGS - POPUP - IMPORT FROM EXCEL'))
        search_contacts_entry = SearchEntry(members_frame, borderwidth=1, font=('TimesNewRoman', 20), justify='center', idleText='Search Contacts')

        tables_frame = tk.Frame(members_frame, width=900)
        contacts_table_canvas = tk.Canvas(tables_frame, width=900, height=30, highlightthickness=0)

        contacts_table_frame = tk.Frame(tables_frame, width=900)
        contacts_table = ttk.Treeview(contacts_table_frame, columns=('one', 'two', 'three', 'four', 'five', 'six'))
        y_contacts_scrollbar = ttk.Scrollbar(contacts_table_frame, orient='vertical', command=contacts_table.yview)
        # x_contacts_scrollbar = ttk.Scrollbar(contacts_table_frame, orient='horizontal', command=contacts_table.xview)

        members_table_canvas = tk.Canvas(tables_frame, width=900, height=30, highlightthickness=0)

        members_table_frame = tk.Frame(tables_frame, width=900)
        members_table = ttk.Treeview(members_table_frame, columns=('one', 'two', 'three', 'four', 'five', 'six'))
        y_members_scrollbar = ttk.Scrollbar(members_table_frame, orient='vertical', command=members_table.yview)
        # x_members_scrollbar = ttk.Scrollbar(members_table_frame, orient='horizontal', command=members_table.xview)

        add_new_members_button = tk.Button(self._popup_frame, text='Add', width=10, font=('Courier', 14),
                                           command=lambda: print('GROUPINGS - POPUP - ADD BUTTON'))


        # Setting up Grid
        self._popup_frame.grid(row=0, column=0)
        title_canvas.grid(row=0, sticky='new')

        information_frame.grid(row=1, column=0, sticky='ew')
        name_canvas.grid(row=0, column=0, sticky='w')
        name_entry.grid(row=0, column=1, sticky='ew', padx=15)
        description_canvas.grid(row=1, column=0, sticky='w')
        description_entry.grid(row=1, column=1, sticky='ew', padx=15)

        members_frame.grid(row=2, column=0, sticky='ew')
        members_canvas.grid(row=0, column=0, sticky='ew', pady=10)
        import_excel_button.grid(row=0, column=0, sticky='e', padx=20)
        search_contacts_entry.grid(row=1, column=0, sticky='ew', padx=20)

        tables_frame.grid(row=3, column=0, sticky='ew', pady=(0, 20))
        contacts_table_canvas.grid(row=0, column=0, sticky='ew', pady=10)

        contacts_table_frame.grid(row=1, column=0, sticky='ew', padx=40)
        contacts_table.grid(row=0, column=0, sticky='w')
        y_contacts_scrollbar.grid(row=0, column=1, sticky='nsw')
        # x_contacts_scrollbar.grid(row=1, column=0, sticky='ew')

        members_table_canvas.grid(row=2, column=0, sticky='w', pady=10)

        members_table_frame.grid(row=3, column=0, sticky='w', padx=40)
        members_table.grid(row=0, column=0, sticky='w')
        y_members_scrollbar.grid(row=0, column=1, sticky='nsw')
        # x_members_scrollbar.grid(row=1, column=0, sticky='ew')

        add_new_members_button.grid(row=3, column=0, sticky='e', padx=20, pady=(0,10))


        # Widget Post-Initialization Configuration
        popup_title = title_canvas.create_text(5, 5, anchor='nw')
        title_canvas.itemconfig(popup_title, font=('Helvetica', 20, 'bold', 'underline'), text=' New Grouping ')

        name_title = name_canvas.create_text(10, 1, anchor='nw')
        name_canvas.itemconfig(name_title, font=('TimesNewRoman', 15), text='Name:')
        description_title = description_canvas.create_text(10, 1, anchor='nw')
        description_canvas.itemconfig(description_title, font=('TimesNewRoman', 15), text='Description (Optional):')

        members_title = members_canvas.create_text(10, 20, anchor='nw')
        members_canvas.itemconfig(members_title, font=('TimesNewRoman', 18, 'underline'), text='Members:')

        contacts_table_title = contacts_table_canvas.create_text(15, 1, anchor='nw')
        contacts_table_canvas.itemconfig(contacts_table_title, font=('TimesNewRoman', 15, 'underline'), text='From Contacts:')

        contacts_table.column('#0', stretch=False, width=150) # width out of 800
        contacts_table.heading('#0', text='Name', anchor='w')
        contacts_table['height'] = 6
        for columnIndex in range(len(contacts_table['columns'])-1):
            column_name = contacts_table['columns'][columnIndex]
            text_name = ('Company', 'Job Title', 'Email', 'Phone', 'Notes')[columnIndex]
            contacts_table.column(column_name, stretch=False, width=124)
            contacts_table.heading(column_name, text=text_name, anchor='w')
        contacts_table.column('six', stretch=False, width=30)
        contacts_table.heading('six', text='Add', anchor='w')

        contacts_table.configure(yscroll=y_contacts_scrollbar.set)#, xscroll=x_contacts_scrollbar.set)

        members_table_title = members_table_canvas.create_text(15, 1, anchor='nw')
        members_table_canvas.itemconfig(members_table_title, font=('TimesNewRoman', 15, 'underline'), text='Added Members:')

        members_table.column('#0', stretch=False, width=150) # width out of 800
        members_table.heading('#0', text='Name', anchor='w')
        members_table['height'] = 6
        for columnIndex in range(len(members_table['columns'])-1):
            column_name = members_table['columns'][columnIndex]
            text_name = ('Company', 'Job Title', 'Email', 'Phone', 'Notes')[columnIndex]
            members_table.column(column_name, stretch=False, width=124)
            members_table.heading(column_name, text=text_name, anchor='w')
        members_table.column('six', stretch=False, width=30)
        members_table.heading('six', text='Remove', anchor='w')

        members_table.configure(yscroll=y_members_scrollbar.set)#, xscroll=x_members_scrollbar.set)

            # FIX ME: SEARCH ENTRY ONLY CONNECTED TO ONE TABLE
        search_contacts_entry.linkTree(contacts_table)


        # Grid Resizing
        information_frame.grid_columnconfigure(0, weight=0)
        information_frame.grid_columnconfigure(1, weight=1)


        # Widget Key Bindings
        self._delete_popup_funcid = self.master.bind_all('<Button-1>', self.delete_popup)
        contacts_table.bind('<Button-1>', self.prevent_resize)
        contacts_table.bind('<Motion>', self.prevent_resize)
        members_table.bind('<Button-1>', self.prevent_resize)
        members_table.bind('<Motion>', self.prevent_resize)

    def delete_popup(self, event):
        """Destroys Pop Up Frame and its binding id if Mouse 1 clicks outside frame"""
        # turning a widget into str returns the path of the widget
        # to check if widget is a descendant of another widget, just check if their starting paths are equal
        if not str(self.master.winfo_containing(event.x_root, event.y_root)).startswith(str(self._popup_frame)):
            self._popup_frame.destroy()
            self.master.unbind('<Button-1>', self._delete_popup_funcid)
            del self._delete_popup_funcid


class MessagingPage(tk.Frame):

    def __init__(self, parent, controller):
        # Tab backend Set up
        tk.Frame.__init__(self, parent, bg='#800080')
        self._controller = controller
        self._managing_page_visible = None
        self._chat_groupings = list()
        self._displayed_chat_groupings = None

        # Initialize Widgets
        messaging_contacts_frame = tk.Frame(self, bg='#00FFFF')
        self._messaging_managing_frame = tk.Frame(self, bg='#DAA520')

        search_groupings_entry = SearchEntry(messaging_contacts_frame, controller=self, mode='List', borderwidth=1, font=('TimesNewRoman', 20), justify='center', idleText='Search Groupings')
        groupings_list_portrait = tk.Frame(messaging_contacts_frame)

        self._groupings_list_canvas = tk.Canvas(groupings_list_portrait, bg='#0000ff')
        self._groupings_list_frame = tk.Frame(self._groupings_list_canvas, bg='#00ff00')

        groupings_list_scrollbar = ttk.Scrollbar(groupings_list_portrait, orient='vertical', command=self._groupings_list_canvas.yview)


        # Setting up Grid
        messaging_contacts_frame.grid(row=0, column=0, sticky='nsew')
        self._messaging_managing_frame.grid(row=0, column=1, sticky='nsew')
        messaging_contacts_frame.grid_propagate(False)
        self._messaging_managing_frame.grid_propagate(False)

        search_groupings_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        groupings_list_portrait.grid(row=1, column=0, sticky='nsew')

        self._groupings_list_canvas.grid(row=0, column=0, sticky='nsew')

        self._groupings_list_frame.grid(row=0, column=0, sticky='nsew')
        groupings_list_scrollbar.grid(row=0, column=1, sticky='ns')


        # Widget Post-Initialization Configuration
        self._canvas_frame = self._groupings_list_canvas.create_window(0, 0, anchor='nw', window=self._groupings_list_frame)
        self._groupings_list_canvas.configure(yscrollcommand=groupings_list_scrollbar.set)
        self.display_chat_groupings(subsection=self._displayed_chat_groupings)
        search_groupings_entry.linkList(self._chat_groupings)


        # Grid Resizing
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=7)
        self.grid_rowconfigure(0, weight=1)

        messaging_contacts_frame.grid_columnconfigure(0, weight=1)
        messaging_contacts_frame.grid_rowconfigure(1, weight=1)

        groupings_list_portrait.grid_columnconfigure(0, weight=1)
        groupings_list_portrait.grid_columnconfigure(1, weight=0)
        groupings_list_portrait.grid_rowconfigure(0, weight=1)

        self._groupings_list_canvas.grid_columnconfigure(0, weight=1)
        self._groupings_list_frame.grid_columnconfigure(0, weight=1)

        self._messaging_managing_frame.grid_rowconfigure(0, weight=1)
        self._messaging_managing_frame.grid_columnconfigure(0, weight=1)

        # Widget Key Bindings
        self._groupings_list_canvas.bind('<Enter>', self.bound_to_mousewheel)
        self._groupings_list_canvas.bind('<Leave>', self.unbound_to_mousewheel)
        self._groupings_list_canvas.bind('<Configure>', self.reset_frame_width)
        self._groupings_list_frame.bind('<Configure>', self.on_frame_configure)

    def bound_to_mousewheel(self, event):
        self._groupings_list_canvas.bind_all('<MouseWheel>', self.on_mousewheel)

    def unbound_to_mousewheel(self, event):
        self._groupings_list_canvas.unbind_all('<MouseWheel>')

    def on_mousewheel(self, event):
        self._groupings_list_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def on_frame_configure(self, event):
        self._groupings_list_canvas.configure(scrollregion=self._groupings_list_canvas.bbox('all'))

    def reset_frame_width(self, event):
        canvas_width = event.width
        self._groupings_list_canvas.itemconfig(self._canvas_frame, width=canvas_width)

    def display_managing_page(self, managing_page_reference):
        """Unmaps/Makes current managing page invisible
        Plots managing page referenced"""
        if self._managing_page_visible is not None:
            if managing_page_reference() != self._managing_page_visible:
                self._managing_page_visible.release_icon()
            self._managing_page_visible.grid_forget()
        self._managing_page_visible = managing_page_reference()
        managing_page_reference().grid(row=0, column=0, sticky='nsew')

    # def get_managing_frame(self):
    #     return self._messaging_managing_frame

    def create_managing_page(self, controller, **kwargs):
        """Creates managing page in messaging age class to avoid destruction errors (bad path)
        Returns a reference to the created page"""
        managing_page = ManagingPage(parent=self._messaging_managing_frame, controller=controller, **kwargs)
        return lambda: managing_page

    def display_chat_groupings(self, subsection=None):
        if subsection is None:
            for grouping in self._controller.get_groupings_list():
                group = ChatGrouping(self._groupings_list_frame, controller=self, bg='white', name=grouping[0])
                self._chat_groupings.append(group)
                group.grid(sticky='nsew')
            self._displayed_chat_groupings = self._chat_groupings
        else:
            if self._displayed_chat_groupings is not None:
                for chat_grouping in self._displayed_chat_groupings:
                    chat_grouping.grid_forget()
            self._displayed_chat_groupings = list()
            for chat_grouping in subsection:
                self._displayed_chat_groupings.append(chat_grouping)
                chat_grouping.grid(sticky='nsew')

    def get_chat_groupings(self):
        return self._chat_groupings

'''============================='''
'''====== WIDGET CLASSES ======='''
'''============================='''
class SearchEntry(tk.Entry):

    def __init__(self, parent, controller=None, idleText='', mode='Tree', **kwargs):

        self._stringVariable = tk.StringVar()
        tk.Entry.__init__(self, parent, textvariable=self._stringVariable, **kwargs)
        self._controller = controller

        self._idleVisible = (idleText != '')
        self._idleText = idleText
        if idleText != '':
            self.insert(0, idleText)

        self._mode = mode
        if mode != 'Tree' and mode != 'List':
            raise Exception('Invalid Mode: \'' + mode + '\'')


        self.bind('<Button-1>', self.clear_idle_on_click)

    def clear_idle_on_click(self, event):
        """Sets entry to blank string when clicked with idle text visible"""
        if self._idleVisible:
            self._stringVariable.set('')
            self._idleVisible = False
            self._entry_bind_id = get_root(self).bind('<Button-1>', self.rewrite_idle)
            self.configure(justify='left')

    def rewrite_idle(self, event):
        """Sets entry to idle text when click outside entry is detected and entry is blank"""
        if not get_root(self).winfo_containing(event.x_root, event.y_root) == self:
            get_root(self).focus()
            if not self._idleVisible and self.get() == '':
                self.master.winfo_containing(event.x_root, event.y_root).focus()
                self._idleVisible = True
                self.configure(justify='center')
                self._stringVariable.set(self._idleText)
                get_root(self).unbind('<Button-1>', self._entry_bind_id)
                del self._entry_bind_id

    def linkTree(self, linkableTree, updateTree=True):
        """Sets self._linkedTree to linkableTree and self._treeItems to a list with all items"""
        if self._mode != 'Tree':
            raise Exception('Invalid for Mode: \'' +self._mode + '\'')

        if updateTree:
            self._stringVariable.trace('w', self.update_tree)

        self._linkedTree = linkableTree
        self._treeItems = list()
        for head in linkableTree.get_children():
            #print(head, linkableTree.get_children(item=head))
            item_childen = list()
            for item in linkableTree.get_children(item=head):
                item_childen.append(linkableTree.item(item))
            self._treeItems.append([linkableTree.item(head), item_childen])

    def expose_in_linkedTree(self, items):
        """Deletes all elementes in linked tree and adds elements from items"""
        if self._mode != 'Tree':
            raise Exception('Invalid for Mode: \'' + self._mode + '\'')

        self._linkedTree.delete(*self._linkedTree.get_children())
        for parent, children in items:
            node = self._linkedTree.insert('', 'end', text=parent['text'], values=parent['values'], tags=parent['tags'])
            if len(children) != 0:
                for child in children:
                    self._linkedTree.insert(node, 'end', text=child['text'], values=child['values'], tags=child['tags'])

    def restore_linkedTree(self):
        """Deletes all elements in linked tree and adds elements from self._treeItems"""
        if self._mode != 'Tree':
            raise Exception('Invalid for Mode: \'' + self._mode + '\'')

        self._linkedTree.delete(*self._linkedTree.get_children())
        for parent, children in self._treeItems:
            node = self._linkedTree.insert('', 'end', text=parent['text'], values=parent['values'], tags=parent['tags'])
            if len(children) != 0:
                for child in children:
                    self._linkedTree.insert(node, 'end', text=child['text'], values=child['values'], tags=child['tags'])

    def update_tree(self, *args):
        """Updates tree so that only items that match with entry show"""
        matchable_string = self.get().lower()
        matchedItems = list()

        if matchable_string == '':
            self.restore_linkedTree()

        if not self._idleVisible:
            for parent, children in self._treeItems:
                skip = False
                if parent['text'].lower().startswith(matchable_string):
                    matchedItems.append([parent, children])
                    continue
                for value in parent['values']:
                    if str(value).lower().startswith(matchable_string):
                        matchedItems.append([parent, children])
                        skip = True
                        break
                if skip:
                    continue
                for child in children:
                    if child['text'].lower().startswith(matchable_string):
                        matchedItems.append([parent, children])
                        break
                    for value in child['values']:
                        if str(value).lower().startswith(matchable_string):
                            matchedItems.append([parent, children])
                            skip = True
                            break
                    if skip:
                        break

            self.expose_in_linkedTree(matchedItems)

    def linkList(self, linkableList, updateList=True):
        if self._mode != 'List':
            raise Exception('Invalid for Mode: \'' + self._mode + '\'')

        if updateList:
            self._stringVariable.trace('w', self.update_list)

        self._linkedList = linkableList

    def update_list(self, *args):
        matchable_string = self.get().lower()
        matched_items = list()

        if matchable_string == '':
            self.restore_linkedList()

        if not self._idleVisible:
            for item in self._linkedList:
                if item.get_name().lower().startswith(matchable_string):
                    matched_items.append(item)
                    continue
                if item.get_members() is not None:
                    for member in item.get_members():
                        if member.lower().startswith(matchable_string):
                            matched_items.append(item)
                            break

            self.expose_in_linkedList(matched_items)

    def restore_linkedList(self):
        if self._mode != 'List':
            raise Exception('Invalid for Mode: \'' + self._mode + '\'')

        self._controller.display_chat_groupings()

    def expose_in_linkedList(self, items):
        if self._mode != 'List':
            raise Exception('Invalid for Mode: \'' + self._mode + '\'')

        self._controller.display_chat_groupings(subsection=items)


class ChatGrouping(tk.Canvas):

    def __init__(self, parent, controller, name='Sample Name', members=None, height=70, *args, **kwargs):
        # Canvas Setup
        global chat_colors
        chat_colors = ['#0084FF', '#12CF13', '#FFC300', '#FB3C4C', '#D696BB']  # blue, green, yellow, red, purple

        tk.Canvas.__init__(self, parent, height=height, *args, **kwargs)
        self._controller = controller

        if name == '' or name is None:
            name = '[Unnamed Grouping]'
        self._name = name
        self._members = members
        self._last_message = ['', ''] # ['member_name', 'time_of_arrival']

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self._chat_color = chat_colors[alphabet.index(name.lower()[0]) % len(chat_colors)] # chat color based on the first letter of the grouping name
        self._managing_page = self._controller.create_managing_page(controller=self, bg='pink')

        # Widget Initialization
        radius = 13
        self._name_canvas = tk.Canvas(self, highlightthickness=0, height=48, bg='white') #height=60 or 50
        self._name_canvas.create_oval(10, 10, 10+2*radius, 10+2*radius, fill=self._chat_color, outline=self._chat_color) # chat color circle
        self._name_canvas.create_text(50, 15, text=self._name, anchor='nw', font=('Courier', 18, 'bold')) # grouping name

        self._last_message_canvas = tk.Canvas(self, highlightthickness=0, height=18, bg='white') #height=10 or 20
        self._last_message_canvas.create_text(10, 0, text='Last Message: {} @ {}'.format(*self._last_message), anchor='nw')


        # Setting up Grid
        self._name_canvas.grid(row=0, column=0, sticky='w', pady=(2, 0), padx=(2, 0))
        self._last_message_canvas.grid(row=1, column=0, sticky='e', pady=(0, 2))


        # Grid Resize
        self.grid_columnconfigure(0, weight=1)


        # Key Bindings
        self.bind('<Button-1>', self.select)
        self._name_canvas.bind('<Button-1>', self.select)
        self._last_message_canvas.bind('<Button-1>', self.select)

    def show_managing_page(self):
        self._controller.display_managing_page(self._managing_page)
        # print('display called')

    def select(self, event=None):
        """Changes chat_icon color and displays chat managing page"""
        self.configure(bg='#EBEBEB')
        self._name_canvas.configure(bg='#EBEBEB')
        self._last_message_canvas.configure(bg='#EBEBEB')
        self.show_managing_page()

    def release(self):
        self.configure(bg='white')
        self._name_canvas.configure(bg='white')
        self._last_message_canvas.configure(bg='white')

    def get_name(self):
        return self._name

    def get_members(self):
        return self._members


class ManagingPage(tk.Frame):

    def __init__(self, parent, controller, chat_grouping=None, **kwargs):
        # Page Setup
        tk.Frame.__init__(self, parent, **kwargs)
        self._controller = controller

        # Widget Initialization
        name_title = tk.Canvas(self, bg='#12CF13', height=80, highlightthicknes=0)

        message_template_frame = tk.Frame(self, bg='pink')
        message_template_title = tk.Canvas(message_template_frame, highlightthickness=0, height=60, bg='pink')

        template_buttons_frame = tk.Frame(message_template_frame, bg='pink')
        existing_template_button = tk.Button(template_buttons_frame, text='Use Existing Template', command=self.use_template_popup, height=1, width=25, font=('Courier', 15))
        new_template_button = tk.Button(template_buttons_frame, text='Add New Template', command=self.add_template_popup, height=1, width=25, font=('Courier', 15))

        template_file_frame = tk.Frame(message_template_frame, bg='pink')
        template_name_canvas = tk.Canvas(template_file_frame, highlightthickness=0, bg='pink', width=220, height=30)
        self._template_path_entry = tk.Entry(template_file_frame, width=20)
        template_clear_button = tk.Button(template_file_frame, text='X', command=lambda:self._template_path_entry.delete(0, 'end'))
        template_send_button = tk.Button(template_file_frame, text='Send', font=('Courier', 12), height=1, width=8, command=lambda:print('SEND TEMPLATE BUTTON'))

        message_logs_frame = tk.Frame(self, bg='pink')
        message_logs_title = tk.Canvas(message_logs_frame, highlightthickness=0, height=50, bg='pink')
        logs_frame = tk.Frame(message_logs_frame, bg='pink')
        logs_canvas = tk.Canvas(logs_frame, highlightthickness=2, bg='#F0F0F0', highlightbackground='white')
        logs_scrollbar = ttk.Scrollbar(logs_frame, orient='vertical', command=logs_canvas.yview)


        # Setting up Grid
        name_title.grid(row=0, column=0, sticky='new')

        message_template_frame.grid(row=1, column=0, sticky='new')
        message_template_title.grid(row=0, column=0, sticky='new')

        template_buttons_frame.grid(row=1, column=0, sticky='new')
        existing_template_button.grid(row=0, column=0, sticky='ne', padx=50)
        new_template_button.grid(row=0, column=1, sticky='nw', padx=50)

        template_file_frame.grid(row=2, column=0, sticky='new', pady=(20, 10))
        template_name_canvas.grid(row=0, column=0, sticky='ne')
        self._template_path_entry.grid(row=0, column=1, sticky='new', pady=(2, 0), ipady=2)
        template_clear_button.grid(row=0, column=2, sticky='nw', padx=5)
        template_send_button.grid(row=1, column=2, sticky='nw', padx=20)

        message_logs_frame.grid(row=2, column=0, sticky='nsew')
        message_logs_title.grid(row=0, column=0, sticky='new')
        logs_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=(10,20))
        logs_canvas.grid(row=0, column=0, stick='nsew')
        logs_scrollbar.grid(row=0, column=1, sticky='ns')


        # Widget Post-Initialization Configuration
        name_title.create_text(10, 10, anchor='nw', text=self._controller.get_name(), font=('Courier', 40, 'underline'))
        message_template_title.create_text(24, 10, anchor='nw', text='Message Template:', font=('Courier', 25))

        template_name_canvas.create_text(40, 0, anchor='nw', text='Template Path: ', font=('Courier', 15))

        message_logs_title.create_text(24, 10, anchor='nw', text='Log:', font=('Courier', 25))


        # Grid Resize
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        message_template_frame.grid_columnconfigure(0, weight=1)
        template_buttons_frame.grid_columnconfigure(0, weight=1)
        template_buttons_frame.grid_columnconfigure(1, weight=1)
        template_file_frame.grid_columnconfigure(0, weight=1)
        template_file_frame.grid_columnconfigure(1, weight=1)
        template_file_frame.grid_columnconfigure(2, weight=1)

        message_logs_frame.grid_columnconfigure(0, weight=1)
        message_logs_frame.grid_rowconfigure(1, weight=1)
        logs_frame.grid_columnconfigure(0, weight=1)
        logs_frame.grid_rowconfigure(0, weight=1)

    def release_icon(self):
        self._controller.release()

    def add_template_popup(self, event=None):
        self._popup_frame = tk.Frame(self.master, width=500, height=500, highlightthickness=2, highlightbackground='#000000')

        popup_title = tk.Canvas(self._popup_frame, height=50, width=80, highlightthickness=0)
        name_canvas = tk.Canvas(self._popup_frame, height=30, width=80, highlightthickness=0)
        name_entry = tk.Entry(self._popup_frame)
        message_canvas = tk.Canvas(self._popup_frame, height=30, highlightthickness=0)
        message_text_box = tk.Text(self._popup_frame)
        save_button = tk.Button(self._popup_frame, text='Save & Use', width=12, height=1, command=lambda:self.save_new_template(name=name_entry.get(), message=message_text_box.get('1.0', 'end')))

        self._popup_frame.grid(row=0, column=0)
        popup_title.grid(row=0, column=0, sticky='new', columnspan=2)
        name_canvas.grid(row=1, column=0, sticky='nw')
        name_entry.grid(row=1, column=1, sticky='new', padx=(10, 20), ipady=2)
        message_canvas.grid(row=2, column=0, sticky='new', columnspan=2)
        message_text_box.grid(row=3, column=0, sticky='nsew', columnspan=2, padx=20)
        save_button.grid(row=4, column=1, sticky='ne', padx=(0, 20), pady=(5, 10))

        popup_title.create_text(10, 10, anchor='nw', text='Add New Message Template', font=('Helvetica', 20, 'underline'))
        name_canvas.create_text(20, 0, anchor='nw', text='Name: ', font=('TimesNewRoman', 15))
        message_canvas.create_text(20, 5, anchor='nw', text='Message: ', font=('TimesNewRoman', 15))

        self._popup_frame.grid_columnconfigure(0, weight=0)
        self._popup_frame.grid_columnconfigure(1, weight=1)
        self._popup_frame.grid_rowconfigure(3, weight=1)

        self._delete_popup_funcid = self.master.bind_all('<Button-1>', self.delete_popup)

    def delete_popup(self, event):
        """Destroys Pop Up Frame and its binding id if Mouse 1 clicks outside frame"""
        # turning a widget into str returns the path of the widget
        # to check if widget is a descendant of another widget, just check if their starting paths are equal
        if not str(self.master.winfo_containing(event.x_root, event.y_root)).startswith(str(self._popup_frame)):
            self._popup_frame.destroy()
            self.master.unbind('<Button-1>', self._delete_popup_funcid)
            del self._delete_popup_funcid

    def save_new_template(self, name, message):
        invalid_chars = ['<', '>', ':', '\"', '/', '\\', '|', '?', '*']
        for character in invalid_chars:
            if character in name:
                print('The following characters are invalid in the Name: \'<\', \'>\', \':\', \'\"\', \'/\', \'\\\', \'|\', \'?\', \'*\'')
                return "break"

        print('now we save')
        # add open save_window with the default directory for templates

        template_file_path = 'TEMPLATE PATH HERE'
        self._template_path_entry.delete(0, 'end')
        self._template_path_entry.insert(0, template_file_path)

        self._popup_frame.destroy()
        self.master.unbind('<Button-1>', self._delete_popup_funcid)
        del self._delete_popup_funcid

    def use_template_popup(self, event=None):
        self._popup_frame = tk.Frame(self.master, width=500, height=500, highlightthickness=2, highlightbackground='#000000')

        popup_title = tk.Canvas(self._popup_frame, height=50, highlightthickness=0)
        preview_canvas = tk.Canvas(self._popup_frame, height=30, highlightthickness=0)
        message_text_box = tk.Text(self._popup_frame, state='disabled')
        apply_button = tk.Button(self._popup_frame, text='Apply', width=12, height=1,
                                command=lambda: self.apply_template('TEMPLATE PATH HERE'))

        self._popup_frame.grid(row=0, column=0)
        popup_title.grid(row=0, column=0, sticky='new')
        preview_canvas.grid(row=1, column=0, sticky='new')
        message_text_box.grid(row=2, column=0, sticky='nsew', padx=20)
        apply_button.grid(row=3, column=0, sticky='ne', padx=(0, 20), pady=(5, 10))

        popup_title.create_text(10, 10, anchor='nw', text='Use Existing Message Template',
                                font=('Helvetica', 20, 'underline'))
        preview_canvas.create_text(20, 0, anchor='nw', text='Preview Message: ', font=('TimesNewRoman', 15))

        self._popup_frame.grid_columnconfigure(0, weight=0)
        self._popup_frame.grid_rowconfigure(2, weight=1)

        self._delete_popup_funcid = self.master.bind_all('<Button-1>', self.delete_popup)

    def apply_template(self, path):
        self._template_path_entry.delete(0, 'end')
        self._template_path_entry.insert(0, path)

        self._popup_frame.destroy()
        self.master.unbind('<Button-1>', self._delete_popup_funcid)
        del self._delete_popup_funcid

'''============================='''
'''====== MAIN AND GLOBAL ======'''
'''######## DO NOT TOUCH #######'''
'''============================='''
def get_root(widget):
    if str(widget) == '.':
        return widget
    return get_root(widget.master)


if __name__ == '__main__':
    root = tk.Tk()
    window = MainWindow(root)
    root.mainloop()
