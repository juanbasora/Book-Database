from tkinter import *
from tkinter.ttk import *
from backend import Database
from tkinter import messagebox


class Inventory:

    def __init__(self, master):
        self.database = Database()
        self.master = master      
        self.master.title("Book Database")
        self.master.resizable(False, False)

        # Creating a scrollbar and a frame
        self.frame = LabelFrame(self.master, text="Book", borderwidth=6)
        self.scrollbar = Scrollbar(self.frame, orient='vertical')

        # creating the listbox and adding the scrollbar to it
        self.list_box = Listbox(self.frame, height=20, yscrollcommand=self.scrollbar.set)

        # Configuring the scrollbar and packing everything.
        self.scrollbar.config(command=self.list_box.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.list_box.pack()
        self.frame.grid(row=0, column=0, padx=15, pady=10)
        
        
        # Creating another frame so that the text box
        # does not merge with the list box.
        self.other_frame = LabelFrame(self.master, text="Description", borderwidth=6)

        self.description_output = Text(self.other_frame, height=20, width=40)
        self.description_output.pack()

        self.other_frame.grid(row=0, column=1, padx=15, pady=10)


        # Checking to see what is selected.
        self.list_box.bind('<<ListboxSelect>>', self.show_description)

        # Adding menubar.
        menubar = Menu(self.master)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Refresh", command=self.fill_listbox)
        file_menu.add_command(label="Close", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Add new book", command=self.add_window)
        edit_menu.add_command(label="Edit selected", command=self.edit_selected)
        edit_menu.add_command(label="Delete Selected", command=self.delete_selected)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About...", command=self.version)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=menubar)

        # Fill the listbox once everything is created.
        self.fill_listbox()

    def show_description(self, event):
        self.description_output.configure(state='normal')
        self.description_output.delete(1.0, 'end')
        self.selected_tuple = self.list_box.get(ANCHOR)

        stuff = self.database.search(self.selected_tuple.split(',')[0])

        for row in stuff:
            self.description_output.insert(END, f"Title: {row[1]}\n\n")
            self.description_output.insert(END, f"Author: {row[2]}\n\n")
            self.description_output.insert(END, f"Year: {row[3]}\n\n")
            self.description_output.insert(END, f"Description: {row[4]}")

        self.description_output.configure(state='disabled')

    def fill_listbox(self):
        self.list_box.delete(0, END)
        for row in self.database.view_all():
            self.list_box.insert(END,str(row[0]) + ", " + row[1])

    def delete_selected(self):
        try:
            self.database.delete(self.selected_tuple.split(",")[0])
            self.fill_listbox()
        except AttributeError:
            messagebox.showinfo("Error", "No book selected")

    def add_window(self):
        add_item_window(self.master)

    def edit_selected(self):
        try:
            ID = self.selected_tuple.split(',')[0]
            add_item_window(self.master, ID)
        except AttributeError:
            messagebox.showinfo("Error", "No book selected")

    def version(self):
        messagebox.showinfo("Version", "1.0")

class add_item_window:

    def __init__(self, new_master, ID=""):

        self.ID = ID
        self.database = Database()

        # Set this new window as the master window.
        self.new_master = Toplevel(new_master)

        # Disables top window till child window is closed.
        self.new_master.grab_set() 

        # Keeps the second window in front at all times.
        self.new_master.attributes("-topmost", True)
        self.new_master.geometry("250x330")
        self.new_master.resizable(False, False)

        # Labels with input boxes
        self.title_text = StringVar()
        self.title_label = Label(self.new_master, text='Title: ')
        self.title_label.grid(row=0, column=0, pady=5, sticky='w')
        self.title_entry = Entry(self.new_master, textvariable=self.title_text)
        self.title_entry.grid(row=0, column=1, pady=5)

        self.author_text = StringVar()
        self.author_label = Label(self.new_master, text="Author: ")
        self.author_label.grid(row=1, column=0, pady=5, sticky='w')
        self.author_entry = Entry(self.new_master, textvariable=self.author_text)
        self.author_entry.grid(row=1, column=1, pady=5)

        self.year_text = StringVar()
        self.year_label = Label(self.new_master, text="Year: ")
        self.year_label.grid(row=2, column=0, pady=5, sticky='w')
        self.year_entry = Entry(self.new_master, textvariable=self.year_text)
        self.year_entry.grid(row=2, column=1, pady=5)

        self.description_label = Label(self.new_master, text="Description: ")
        self.description_label.grid(row=3, column=0, pady=5, sticky='w')
        self.description_entry = Text(self.new_master, height=10, width=20)
        self.description_entry.grid(row=3, column=1, pady=5)

        
        self.button_text = StringVar()

        if self.ID == "":
            self.button_text.set('ADD')
            self.new_master.title("Add Book")
        else:
            self.new_master.title("Update Book")
            self.button_text.set('Update')
            self.fill_boxes()


        self.add_button = Button(self.new_master, textvariable=self.button_text, command=self.add_to_db)
        self.add_button.grid(row=4, column=1, pady=5)

    def fill_boxes(self):
        book_info = self.database.search(self.ID)

        self.title_entry.insert(END, book_info[0][1])
        self.author_entry.insert(END, book_info[0][2])
        self.year_entry.insert(END, book_info[0][3])
        self.description_entry.insert(END, book_info[0][4])

    def add_to_db(self):
        if self.ID == "":
            self.database.add_entry(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.description_entry.get(1.0, 'end-1c'))
            print("Book added")
        else:
            self.database.update(self.ID, self.title_text.get(), self.author_text.get(), self.year_text.get(), self.description_entry.get(1.0, 'end-1c'))
            print("book updated")

    def __del__(self):
        self.new_master.destroy()

if __name__ == "__main__":
    WINDOW = Tk()
    Inventory(WINDOW)
    WINDOW.mainloop()
