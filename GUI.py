import os
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
import AcrossReader


class GUI:

    @classmethod
    def start_application(cls):
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showinfo("Datei wählen", "Wählen Sie bitte die Datei im htm-Format aus, welche Sie in das "
                                               "csv-Format übertragen möchten.")
        htm_file = filedialog.askopenfilename()

        if not htm_file:
            return

        AcrossReader.AcrossReader.read_htm_file(htm_file)

        file_name = os.path.basename(htm_file)[:-4] + "_translated"

        tk.messagebox.showinfo("Erfolgreich übertragen", "Die Datei wurde erfolgreich in das csv-Format übertragen. Die"
                                                         " Datei befindet sich im Ausgangsordner und trägt den Namen: "
                               + file_name + ".")
