import json
import re
from Implementation.Logic import AcrossReader
import tkinter as tk
from tkinter import filedialog, RIGHT, Y, END, LEFT, BOTH
from tkinter.messagebox import showinfo
from Abstract.IGUI import IGUI


class GUI(IGUI):

    def start_application(self, across_reader):
        """
        Starts the application with the main window.

        :param across_reader: instance of the AcrossReader class.
        """

        root = tk.Tk()
        self.__set_center(root)

        root.title("AcrossReader")

        label_welcome = tk.Label(root, text="Herzlich Willkommen", height=2, width=30, font=("Arial", 25)).pack(
            anchor="center", pady=10)

        button_read_htm_file = tk.Button(root, text="Lesen einer htm-Datei", width="25", command=lambda: self.read_htm_file(across_reader)).pack(
            anchor="center", pady=5)

        button_edit_tag_file = tk.Button(root, text="Tag-Datei bearbeiten", width="25", command=lambda: self.ask_for_file(across_reader)).pack(
            anchor="center", pady=5)
        button_create_new_tag_file = tk.Button(root, text="Neue Tag-Liste anlegen", width="25", command=lambda: self.create_new_tag_file(across_reader)).pack(
            anchor="center", pady=5)
        button_exit = tk.Button(root, text="Beenden", width="25", command=root.destroy).pack(anchor="center", pady=5)

        root.mainloop()

    def read_htm_file(self, across_reader):
        """
        Reads a htm file that is chosen within the window that will open.

        :param across_reader: instance of the AcrossReader class.
        """

        tk.messagebox.showinfo("Datei wählen", "Wählen Sie bitte die Datei im htm-Format aus, welche Sie in eine "
                                               "docx-Datei übertragen möchten.")
        htm_file = filedialog.askopenfilename()

        try:
            across_reader.across_validator.validate_file_existence(htm_file)
            tk.messagebox.showinfo("Datei wählen", "Wählen Sie bitte eine Datei im json-Format aus, welche die text-"
                                                   "spezifischen Tags enthält. Möchten Sie ohne Tag-Ersetzung fortfahren, "
                                                   "wählen Sie bitte eine leere Tag-Datei. Diese können Sie über 'Neue Tag-Liste anlegen' "
                                                   "erstellen.")
            tag_file = filedialog.askopenfilename()
            across_reader.across_validator.validate_file_existence(tag_file)

            try:
                across_reader.read_htm_file(htm_file, tag_file)

                tk.messagebox.showinfo("Erfolgreich übertragen",
                                       "Die Datei wurde erfolgreich in eine docx-Datei übertragen. Die"
                                       " Datei befindet sich im Ausgangsordner.")

            except ValueError as error:
                tk.messagebox.showerror("Fehler", str(error))

        except OSError:
            tk.messagebox.showerror("Fehler", "Sie haben nicht alle notwendigen Dateien ausgewählt!")
            return

    def ask_for_file(self, across_reader):
        """
        Asks for a json file that contains tags.

        :param across_reader: instance of the AcrossReader class.
        """

        try:
            tk.messagebox.showinfo("Datei wählen", "Wählen Sie bitte die Datei aus, welche projektspezifische Tags enthält.")
            tag_file = filedialog.askopenfilename()

            # Validation of the tag file
            across_reader.across_validator.validate_file_existence(tag_file)
            across_reader.across_validator.check_tag_file(tag_file)

            with open(tag_file, "r", encoding="utf-8") as file:
                all_tags = json.load(file)
            if not across_reader.across_validator.validate_json_schema(all_tags):
                return False

            self.edit_tag_file(tag_file, across_reader)

        except (OSError, ValueError) as error:
            tk.messagebox.showerror("Fehler", str(error))

    def create_new_tag_file(self, across_reader):
        """
        Creates an empty json file for storing tags. Replaces the file ending with .json automatically.

        :param across_reader: instance of the AcrossReader class.
        """

        window = tk.Toplevel()
        window.grab_set()

        self.__set_center(window)

        tk.messagebox.showinfo("Speicherort wählen", "Bitte wählen Sie den Speicherort für die neue Datei und "
                                                     "vergeben Sie einen Namen.")
        tag_file = filedialog.asksaveasfilename()

        if tag_file != '':
            tag_file = re.sub('\\..*\n?', '.json', tag_file)
            if '.' not in tag_file:
                tag_file = tag_file + ".json"
            across_reader.create_new_tag_file(tag_file)
            tk.messagebox.showinfo("Erfolgreich angelegt", "Die von Ihnen gewünschte Datei wurde erfolgreich angelegt.")
            window.destroy()
            self.edit_tag_file(tag_file, across_reader)

        else:
            window.destroy()

    def edit_tag_file(self, tag_file, across_reader):
        """
        Opens the dialogue for adding and deleting tags in an existing list of tags.

        :param tag_file: json file that contains at least an empty dictionary.
        :param across_reader: instance of the AcrossReader class.
        """

        window = tk.Toplevel()
        window.grab_set()
        self.__set_center(window)

        label_tags_in_file = tk.Label(window, text="Aktuelle Tags in der Datei", font=('Arial', 20)).pack(anchor="w", padx=(10, 0))

        # frame that contains the scrollbar
        frame = tk.Frame(window)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 10))
        tag_list = AcrossReader.AcrossReader.show_tags(tag_file)
        tag_list_gui = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=75, height=5)

        for tag in tag_list:
            tag_list_gui.insert(END, tag)

        tag_list_gui.pack(side=LEFT, fill=BOTH, anchor="w", padx=(10, 0))
        scrollbar.config(command=tag_list_gui.yview)
        frame.pack()

        # single labels and buttons
        label_user_input = tk.Label(window, text="Füllen Sie die folgenden Informationen aus.",
                           font=('Arial', 14)).pack(anchor="w", padx=10, pady=10)
        label_additional_info_for_deleting_tags = tk.Label(window, text=(
            "*Wenn Sie einen Tag löschen möchten, geben Sie unter 'Name des Tags' den Namen des Tags ein "
            "und bestätigen Sie mit 'Löschen'."), wraplength=450, justify="left").pack(anchor="w", pady=5, padx=(10, 40))

        label_tag_name = tk.StringVar()
        label_tag_name.set("Name des Tags (*Pflichtfeld)")
        label_tag_name_dir = tk.Label(window, textvariable=label_tag_name, font='Arial 10 bold')
        label_tag_name_dir.pack(anchor="w", padx=10)

        label_tag_name_input = tk.StringVar(None)
        label_tag_name_input_dir = tk.Entry(window, textvariable=label_tag_name_input, width=50)
        label_tag_name_input_dir.pack(anchor="w", padx=10)

        label_opening_tag = tk.StringVar()
        label_opening_tag.set("Öffnender Tag (*Pflichtfeld)")
        label_opening_tag_dir = tk.Label(window, textvariable=label_opening_tag, font='Arial 10 bold')
        label_opening_tag_dir.pack(anchor="w", padx=10)

        label_opening_tag_input = tk.StringVar(None)
        label_opening_tag_input_dir = tk.Entry(window, textvariable=label_opening_tag_input, width=50)
        label_opening_tag_input_dir.pack(anchor="w", padx=10)

        label_closing_tag = tk.StringVar()
        label_closing_tag.set("Schließender Tag (leer, falls nicht vorhanden)")
        label_closing_tag_dir = tk.Label(window, textvariable=label_closing_tag, font='Arial 10 bold')
        label_closing_tag_dir.pack(anchor="w", padx=10)

        label_closing_tag_input = tk.StringVar(None)
        label_closing_tag_input_dir = tk.Entry(window, textvariable=label_closing_tag_input, width=50)
        label_closing_tag_input_dir.pack(anchor="w", padx=10)

        label_show_tag = tk.StringVar()
        label_show_tag.set("Soll der Tag in der neuen Datei als Tag angezeigt werden? (*Pflichtfeld)")
        label_show_tag_dir = tk.Label(window, textvariable=label_show_tag, font='Arial 10 bold')
        label_show_tag_dir.pack(anchor="w", padx=10)

        label_show_tag_input = tk.BooleanVar(value=True)
        tk.Radiobutton(window, text="Ja", padx=10, variable=label_show_tag_input, value=True).pack(anchor="w", padx=10)
        tk.Radiobutton(window, text="Nein", padx=10, variable=label_show_tag_input, value=False).pack(anchor="w", padx=10)

        user_input_list = [label_tag_name_input, label_opening_tag_input, label_closing_tag_input, label_show_tag_input]

        button_add_tag = tk.Button(window, text="Hinzufügen",
                               command=lambda: self.save_to_tag_file(user_input_list, tag_file, window, across_reader), width="15").pack(
            anchor="e",
            padx=(0, 40))

        button_delete_tag = tk.Button(window, text="Löschen",
                                  command=lambda: self.delete_tag(tag_file, user_input_list[0], window, across_reader), width="15").pack(
            anchor="e", padx=(0, 40), pady=5)
        button_go_back = tk.Button(window, text="Zurück", command=window.destroy, width="15").pack(anchor="e",
                                                                                                padx=(0, 40))

    def delete_tag(self, tag_file, tag_to_be_deleted, window, across_reader):
        """
        Deletes the given tag in the given json file if existing. Closes the window at the end.

        :param tag_file: json file that contains at least an empty dictionary.
        :param tag_to_be_deleted: tag that needs to be deleted.
        :param window: window that is shown.
        :param across_reader: instance of the AcrossReader class.
        """

        result = across_reader.delete_tag(tag_file, tag_to_be_deleted)
        window.destroy()

        if result:
            tk.messagebox.showinfo("Erfolgreich gelöscht", "Der von Ihnen gewählte Tag wurde erfolgreich aus der angegebenen Datei gelöscht.")
        else:
            tk.messagebox.showerror("Fehler", "Der von Ihnen gewählte Tag konnte nicht gelöscht werden, da ein solcher "
                                              "Tag nicht in der angegebenen Datei existiert.")
        self.edit_tag_file(tag_file, across_reader)

    def save_to_tag_file(self, tag_list, tag_file, window, across_reader):
        """
        Saves the new tag to the given json file containing the tags.

        :param tag_list: list containing the information of the new tag that is to be stored.
        :param tag_file: json file that contains at least an empty dictionary.
        :param window: window that is shown.
        :param across_reader: instance of the AcrossReader class.
        """

        try:
            across_reader.across_validator.check_empty_string(tag_list[0].get())
            across_reader.across_validator.check_empty_string(tag_list[1].get())

            result = across_reader.save_to_tag_file(tag_list, tag_file)

            window.destroy()

            if result:
                tk.messagebox.showinfo("Erfolgreich gespeichert", "Der von Ihnen gewünschte Tag wurde erfolgreich hinzugefügt.")
            else:
                tk.messagebox.showerror("Fehler", "Der von Ihnen gewünschte Tag konnte nicht hinzugefügt werden, da "
                                                  "er bereits in der ausgewählten Datei existiert.")
            self.edit_tag_file(tag_file, across_reader)

        except ValueError as error:
            tk.messagebox.showerror("Fehler", str(error))

    @staticmethod
    def __set_center(root):
        # Thanks to Sandeep Prasad Kushwaha for this method (source: stackoverflow)
        root.resizable(False, False)  # This code helps to disable windows from resizing

        window_height = 550
        window_width = 500

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
