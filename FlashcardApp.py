import tkinter as tk
from tkinter import DISABLED, END, NORMAL, StringVar, ttk, messagebox
import json
import os

LARGEFONT = ("Times", 24)

class Database():
    """Class designed to work with the .txt files that contain the flashcard
    data by using json dump and loads"""
    def __init__(self):
        """Constructor class - yet to add"""
        pass

    def create_set(self, temp, title):
        """Creates a .txt file using user input on the title of the class. The
        data is then stored using json"""
        with open(str(title)+'.txt', 'w') as f:
            f.write(json.dumps(temp))
        f.close()

class FlashcardApp(tk.Tk):
    """Main Class for the application that holds the different frames in a container
    and will display them when called in the event-driven program"""

    def __init__(self, *args, **kwargs):
        """Constructor - Creates the container and different frames of 
        the program"""

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creates containers
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # different frames in program
        self.frames = {}

        # sets up frames
        for f in (MainMenu, StudyMenu, EditMenu, NewMenu, ActiveStudying, EditingWindow):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # calls the first frame - MainMenu
        self.show_frame(MainMenu)

    def show_frame(self, cont):
        """When called it displayed the proper frame to the user"""
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[cont]
        frame.grid()
        #frame.tkraise()
    
    def refresh(self):
        """Destroys the root, then calls it again. Forces the program to refresh 
        in order to have updated data"""
        self.destroy()
        self.__init__()

class MainMenu(tk.Frame):
    """Main Menu - displays to the user four different options to choose from:
    study, edit, create set, or exit the program"""

    def __init__(self, parent, controller):
        """Constructor - Creates the labels and buttons for the main menu"""

        # inheritance
        tk.Frame.__init__(self, parent)

        # Label - creates and displays "Flashcards Menu"
        title_label = ttk.Label(self, text="Flashcards Menu", font = LARGEFONT)
        title_label.grid(row=0, column=1, sticky="N", padx=10, pady=10)

        # Creates four separate buttons
        study_button = ttk.Button(self, text="Study", command=lambda:controller.show_frame(StudyMenu))
        edit_button = ttk.Button(self, text="Edit", command=lambda:controller.show_frame(EditMenu))
        new_button = ttk.Button(self, text="Create Set", command=lambda:controller.show_frame(NewMenu))
        exit_button = ttk.Button(self, text="Exit", command=self.quit)

        # Displays the buttons
        study_button.grid(row=1, column=1, padx=10, pady=10)
        edit_button.grid(row=2, column=1, padx=10, pady=10)
        new_button.grid(row=3, column=1, padx=10, pady=10)
        exit_button.grid(row=4, column=1, padx=10, pady=10)

class StudyMenu(tk.Frame):
    """Study Menu - Displays the frame that allows the user to choose a flashcard set to study"""

    def __init__(self, parent, controller):
        """Constructor - creates the labels and radiobuttons for study menu"""

        #inheritance
        tk.Frame.__init__(self, parent)

        # Label - creates and displays the title
        title_label = ttk.Label(self, text="Choose Set to Study:", font = LARGEFONT)
        title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        # Radiobuttons - creates a list of files and creates an option for those that are a flashcard set
        v = tk.StringVar()
        counter = 1
        for item in os.listdir():
            if item.endswith(".txt"):
                file_button = ttk.Radiobutton(self, text=item[:-4], variable=v, value=item, command=lambda:self.update_state(next_button, item))
                file_button.grid(row=counter+1, column=1, sticky="W")
                counter += 1
                
        #self.file = v.get()
        # Currently working to get v.get() data into another class to use

        # Button - creates and displays the back button (to Main Menu)
        back_button = ttk.Button(self, text="Back", command = lambda : controller.show_frame(MainMenu))
        back_button.grid(row=20, column=0, sticky="SW", padx=10, pady=10)
   
        # Button - creates and displays the next button (to Active Studying)
        next_button = ttk.Button(self, text="Next", state=DISABLED, command = lambda : self.next(controller, v.get()))
        next_button.grid(row=20, column=3, sticky="SE", padx=10, pady=10)

    def update_state(self, next_button, file):
        """Updates the state of the next_button. The button cannot be used until a radiobutton is
        chosen"""
        next_button['state'] = NORMAL

    def next(self, controller, value):
        """Called when the next button is pressed"""
        controller.show_frame(ActiveStudying)
        #value


class ActiveStudying(StudyMenu, tk.Frame):
    """Active Studying - displays the card by card of the set chosen to study """

    def __init__(self, parent, controller):
        """Constructor - displays the labels and buttons for the Active Studying Menu"""

        # inheritance
        StudyMenu.__init__(self, parent, controller)
        tk.Frame.__init__(self, parent)

        # Label - Creates and displays title
        title_label = ttk.Label(self, text="", font = LARGEFONT)
        title_label.grid(row=0, column=1, sticky="N", padx=10, pady=10)

        # Button - Takes user back to the Study Menu
        back_button = ttk.Button(self, text="Back", command = lambda : controller.show_frame(StudyMenu))
        back_button.grid(row=1, column=1, sticky="SW", padx=10, pady=10)

        # Take in v.get()

class EditMenu(tk.Frame):
    """Menu that allows the user to choose a set to edit"""

    def __init__(self, parent, controller):
        """Constructor - displays the labels and radiobuttons for EditMenu"""

        # inheritance
        tk.Frame.__init__(self, parent)

        # Label - creates and displays the title
        title_label = ttk.Label(self, text="Choose Set to edit:", font=LARGEFONT)
        title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        # Radiobuttons - creates a list of files and creates an option for those that are a flashcard set
        r = StringVar()
        counter = 1

        for item in os.listdir():
            if item.endswith(".txt"):
                file_button = ttk.Radiobutton(self, text=item[:-4], variable=r, value=item)
                file_button.grid(row=counter+1, column=1, sticky="W")
                counter += 1

        # Button - takes user back to the Main Menu
        back_button = ttk.Button(self, text="Back", command = lambda : controller.show_frame(MainMenu))
        back_button.grid(row=20, column=0, sticky="SW", padx=10, pady=10)

        # Button - takes user to the Editing Window
        next_button = ttk.Button(self, text="Next", command = lambda : controller.show_frame(EditingWindow))
        next_button.grid(row=20, column=3, sticky="SE", padx=10, pady=10)

class EditingWindow(tk.Frame):
    """Menu that allows the user to edit a set of cards that already exist"""

    def __init__(self, parent, controller):
        """Cosnstructor - displays the labels and buttons for EditingWindow"""

        #inheritance
        tk.Frame.__init__(self, parent)

        # Label - creates and displays the title
        title_label = ttk.Label(self, text="Editing...", font=LARGEFONT)
        title_label.grid(row=0, column=1, padx=10, pady=10)

        # Button - takes user back to the EditMenu 
        back_button = ttk.Button(self, text="Back", command = lambda : controller.show_frame(EditMenu))
        back_button.grid(row=1, column=1, sticky="SW", padx=10, pady=10)

class NewMenu(Database, tk.Frame):
    """Menu that allows a user to create a new set of flashcards"""

    def __init__(self, parent, controller):
        """Constructor - creates the labels, buttons, and entries for the NewMenu"""

        #inheritance
        Database.__init__(self)
        tk.Frame.__init__(self, parent)

        # Label - creates and displays the title
        title_label = ttk.Label(self, text="Create A New Set", font=LARGEFONT)
        title_label.grid(row=0, column=1, columnspan=2, sticky="EW", padx=10, pady=10)

        # Button - calls the back_button function 
        back_button = ttk.Button(self, text="Back", command = lambda : self.back_button(controller))
        back_button.grid(row=6, column=0, sticky="SW", padx=10, pady=10)

        # Label/Entry - tells the user to enter the title of the flashcard set
        name_label = ttk.Label(self, text="Enter Title:")
        name_label.grid(row=1, column=1, sticky="W")
        self.name_entry = ttk.Entry(self, width=40)
        self.name_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        # Creates a dictionary for the flashcard set
        self.temp = {}
        self.counter = 1

        # counter to display what card number the user is on
        counter_label = ttk.Label(self, text="Card " + str(self.counter) + ":")
        counter_label.grid(row=3, column=1, sticky="W")

        # Label/Entry - tells the user to enter the term of the card
        term_label = ttk.Label(self, text="Term:")
        term_label.grid(row=4, column=1, sticky="W")
        self.term_entry = ttk.Entry(self, width=40)
        self.term_entry.grid(row=4, column=2, padx=10, pady=10)

        # Label/Entry - tells the user to enter the definition of the card
        def_label = ttk.Label(self, text="Definition:")
        def_label.grid(row=5, column=1, sticky="W")
        self.def_entry = ttk.Entry(self, width=40)
        self.def_entry.grid(row=5, column=2, padx=10, pady=10)

        # Button - calls the add_card function
        add_card_button = ttk.Button(self, text="Add Card", command=lambda:self.add_card(self.term_entry.get(), self.def_entry.get()))
        add_card_button.grid(row=6, column=2)

        # Button - calls the save_set function
        save_button = ttk.Button(self, text="Save Set", command=lambda:self.save_set(controller))
        save_button.grid(row=6, column=3, sticky="SE", padx=10, pady=10)


    def add_card(self, term, defin):
        """Adds the card the dictionary, changes the card counter, and deletes the
        entries that the user has inputted"""

        self.counter += 1
        self.temp[term] = defin

        counter_label = ttk.Label(self, text="Card " + str(self.counter) + ":")
        counter_label.grid(row=3, column=1, sticky="W")

        self.term_entry.delete(0, END)
        self.def_entry.delete(0, END)


    def save_set(self, controller):
        """Sends the dictionary to the database for a .txt file to be created, deletes the 
        flashcard title entry, restarts the counter, displays a messagebox to show the set saved,
        refreshs the frame for the new data and returns the user back to the main menu"""
        #title = self.name_entry.get()

        super().create_set(self.temp, self.name_entry.get())

        self.name_entry.delete(0, END)

        self.counter = 1
        counter_label = ttk.Label(self, text="Card " + str(self.counter) + ":")
        counter_label.grid(row=3, column=1, sticky="W")

        messagebox.showinfo("Flashcard App", "Flashcard set saved!")

        controller.refresh()
        controller.show_frame(MainMenu)

    def back_button(self, controller):
        """Resets the card counter, clear the entries, and return the user back to the
        main menu"""
        self.counter = 1
        counter_label = ttk.Label(self, text="Card " + str(self.counter) + ":")
        counter_label.grid(row=3, column=1, sticky="W")

        self.name_entry.delete(0, END)
        self.term_entry.delete(0, END)
        self.def_entry.delete(0, END)

        controller.show_frame(MainMenu)

# Main Program:
f = FlashcardApp()
f.mainloop()