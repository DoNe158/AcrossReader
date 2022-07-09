import json
import re
import AcrossReader
import AcrossValidation
import tkinter as tk
from tkinter import filedialog, RIGHT, Y, END, LEFT, BOTH
from tkinter.messagebox import showinfo


class GUI:

    @classmethod
    def start_application(cls):
        """
        Starts the application with the main window.
        """

        root = tk.Tk()
        cls.__set_center__(root)

        root.title("AcrossReader")

        label1 = tk.Label(root, text="Herzlich Willkommen", height=2, width=30, font=("Arial", 25)).pack(
            anchor="center", pady=10)
        button_1 = tk.Button(root, text="Lesen einer htm-Datei", width="25", command=cls.__read_htm__).pack(
            anchor="center", pady=5)
        button_2 = tk.Button(root, text="Tag-Liste bearbeiten", width="25", command=lambda: cls.__ask_for_file__()).pack(
            anchor="center", pady=5)
        button_3 = tk.Button(root, text="Neue Tag-Liste anlegen", width="25", command=cls.__create_new_tag_file__).pack(
            anchor="center", pady=5)
        button_4 = tk.Button(root, text="Beenden", width="25", command=root.destroy).pack(anchor="center", pady=5)

        root.mainloop()

    @classmethod
    def __read_htm__(cls):
        """
        Reads a htm file that is chosen within the window that will open.
        """

        across_validator = AcrossValidation.AcrossValidation()

        tk.messagebox.showinfo("Datei wählen", "Wählen Sie bitte die Datei im htm-Format aus, welche Sie in eine "
                                               "docx-Datei übertragen möchten.")
        htm_file = filedialog.askopenfilename()

        try:
            across_validator.validate_file_existence(htm_file)
            tk.messagebox.showinfo("Datei wählen", "Wählen Sie bitte eine Datei im json-Format aus, welche die text-"
                                                   "spezifischen Tags enthält. Möchten Sie ohne Tag-Ersetzung fortfahren, "
                                                   "wählen Sie bitte eine leere Tag-Datei. Diese können Sie über 'Neue Tag-Liste anlegen' "
                                                   "erstellen.")
            tag_file = filedialog.askopenfilename()
            across_validator.validate_file_existence(tag_file)

            try:
                AcrossReader.AcrossReader.read_htm_file(htm_file, tag_file)

                tk.messagebox.showinfo("Erfolgreich übertragen",
                                       "Die Datei wurde erfolgreich in eine docx-Datei übertragen. Die"
                                       " Datei befindet sich im Ausgangsordner.")

            except ValueError as error:
                tk.messagebox.showerror("Fehler", str(error))

        except OSError:
            tk.messagebox.showerror("Fehler", "Sie haben nicht alle notwendigen Dateien ausgewählt!")
            return

    @classmethod
    def __ask_for_file__(cls):
        """
        Asks for a json file that contains tags.
        """

        across_validator = AcrossValidation.AcrossValidation()

        try:
            tk.messagebox.showinfo("Datei wählen",
                                   "Wählen Sie bitte die Datei aus, welche projektspezifische Tags enthält.")
            tag_file = filedialog.askopenfilename()

            # Validation of the tag file
            across_validator.validate_file_existence(tag_file)
            across_validator.check_tag_file(tag_file)

            with open(tag_file, "r", encoding="utf-8") as file:
                all_tags = json.load(file)
            if not across_validator.validate_json_schema(all_tags):
                return False

            cls.__open_file__(tag_file)

        except (OSError, ValueError) as error:
            tk.messagebox.showerror("Fehler", str(error))

    @classmethod
    def __create_new_tag_file__(cls):
        """
        Creates an empty json file for storing tags. Replaces the file ending with .json automatically.
        """

        window = tk.Toplevel()
        window.grab_set()

        cls.__set_center__(window)

        tk.messagebox.showinfo("Speicherort wählen", "Bitte wählen Sie den Speicherort für die neue Datei und "
                                                     "vergeben Sie einen Namen.")
        tag_file = filedialog.asksaveasfilename()

        if tag_file != '':
            tag_file = re.sub('\\..*\n?', '.json', tag_file)
            AcrossReader.AcrossReader.__create_new_tag_file__(tag_file)
            tk.messagebox.showinfo("Erfolgreich angelegt", "Die von Ihnen gewünschte Datei wurde erfolgreich angelegt.")
            window.destroy()
            cls.__open_file__(tag_file)

        else:
            window.destroy()

    @classmethod
    def __open_file__(cls, tag_file):
        """
        Opens the dialogue for adding and deleting tags in an existing list of tags.

        :param tag_file: json file that contains at least an empty dictionary.
        """

        window = tk.Toplevel()
        window.grab_set()
        cls.__set_center__(window)

        label_1 = tk.Label(window, text="Aktuelle Tags in der Datei", font=('Arial', 20)).pack(anchor="w", padx=(10, 0))

        # frame that contains the scrollbar
        frame = tk.Frame(window)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        tag_list = AcrossReader.AcrossReader.__show_tags__(tag_file)
        tag_list_gui = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=75, height=5)

        for entry in tag_list:
            tag_list_gui.insert(END, entry)

        tag_list_gui.pack(side=LEFT, fill=BOTH, anchor="w")
        scrollbar.config(command=tag_list_gui.yview)
        frame.pack()

        # single labels and buttons
        label3 = tk.Label(window, text="Füllen Sie die folgenden Informationen aus.",
                          padx=10, pady=10, font=('Arial', 14)).pack(anchor="w")
        l1 = tk.Label(window, text=(
            "*Wenn Sie einen Tag löschen möchten, geben Sie unter 'Name des Tags' den Namen des Tags ein "
            "und bestätigen Sie mit 'Löschen'."), wraplength=450, justify="left").pack(anchor="w", pady=5, padx=(5, 40))

        label_entry_1 = tk.StringVar()
        label_entry_1.set("Name des Tags (*Pflichtfeld)")
        label_dir = tk.Label(window, textvariable=label_entry_1, font='Arial 10 bold')
        label_dir.pack(anchor="w", padx=10)

        entry_1 = tk.StringVar(None)
        dir_name = tk.Entry(window, textvariable=entry_1, width=50)
        dir_name.pack(anchor="w", padx=10)

        label_entry_2 = tk.StringVar()
        label_entry_2.set("Öffnender Tag (*Pflichtfeld)")
        label_dir_2 = tk.Label(window, textvariable=label_entry_2, font='Arial 10 bold')
        label_dir_2.pack(anchor="w", padx=10)

        entry_2 = tk.StringVar(None)
        dir_name_2 = tk.Entry(window, textvariable=entry_2, width=50)
        dir_name_2.pack(anchor="w", padx=10)

        label_entry_3 = tk.StringVar()
        label_entry_3.set("Schließender Tag (leer, falls nicht vorhanden)")
        label_dir_3 = tk.Label(window, textvariable=label_entry_3, font='Arial 10 bold')
        label_dir_3.pack(anchor="w", padx=10)

        entry_3 = tk.StringVar(None)
        dir_name_3 = tk.Entry(window, textvariable=entry_3, width=50)
        dir_name_3.pack(anchor="w", padx=10)

        label_entry_4 = tk.StringVar()
        label_entry_4.set("Soll der Tag in der neuen Datei als Tag angezeigt werden? (*Pflichtfeld)")
        label_dir_4 = tk.Label(window, textvariable=label_entry_4, font='Arial 10 bold')
        label_dir_4.pack(anchor="w", padx=10)

        v = tk.BooleanVar(value=True)
        tk.Radiobutton(window, text="Ja", padx=10, variable=v, value=True).pack(anchor="w")
        tk.Radiobutton(window, text="Nein", padx=10, variable=v, value=False).pack(anchor="w")

        tmp_list = [entry_1, entry_2, entry_3, v]

        button_try = tk.Button(window, text="Hinzufügen",
                               command=lambda: cls.__save_to_tag_file__(tmp_list, tag_file, window), width="15").pack(
            anchor="e",
            padx=(0, 40))

        button_delete = tk.Button(window, text="Löschen",
                                  command=lambda: cls.__delete_tag__(tag_file, tmp_list[0], window), width="15").pack(
            anchor="e", padx=(0, 40), pady=5)
        button_back = tk.Button(window, text="Zurück", command=window.destroy, width="15").pack(anchor="e",
                                                                                                padx=(0, 40))

    @classmethod
    def __delete_tag__(cls, tag_file, tag_to_be_deleted, window):
        """
        Deletes the given tag in the given json file if existing. Closes the window at the end.

        :param tag_file: json file that contains at least an empty dictionary.
        :param tag_to_be_deleted: tag that needs to be deleted.
        :param window: window that is shown.
        """

        res = AcrossReader.AcrossReader.__delete_tag__(tag_file, tag_to_be_deleted)
        window.destroy()
        tk.messagebox.showinfo(res[0], res[1])
        cls.__open_file__(tag_file)

    @classmethod
    def __save_to_tag_file__(cls, tag_list, tag_file, window):
        """
        Saves the new tag to the given json file containing the tags.

        :param tag_list: list containing the information of the new tag that is to be stored.
        :param tag_file: json file that contains at least an empty dictionary.
        :param window: window that is shown.
        """

        across_validator = AcrossValidation.AcrossValidation()

        try:
            across_validator.check_empty_string(tag_list[0].get())
            across_validator.check_empty_string(tag_list[1].get())

            res = AcrossReader.AcrossReader.__save_to_tag_file__(tag_list, tag_file)
            window.destroy()
            tk.messagebox.showinfo(res[0], res[1])
            cls.__open_file__(tag_file)

        except ValueError as error:
            tk.messagebox.showerror("Fehler", str(error))

    @classmethod
    def __set_center__(cls, root):
        # Thanks to Sandeep Prasad Kushwaha for this method (source: stackoverflow)
        root.resizable(False, False)  # This code helps to disable windows from resizing

        window_height = 550
        window_width = 500

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
