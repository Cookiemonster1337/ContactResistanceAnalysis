import tkinter.filedialog
import tkinter as tk
from gui_doc import import_data


def get_file():
    filename = \
        tk.filedialog.askopenfilename(initialdir="C:/Users/Kapp/Desktop/CR/",
                                      title="Select file",
                                      filetypes=(("Text files", "*.txt"),
                                                 ("all files", "*.*")))
    import_data(filename)

