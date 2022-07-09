from jsonschema import validate
import jsonschema
import json
import os.path


class AcrossValidation(BaseException):

    @staticmethod
    def check_file_ending(htm_file):
        if not htm_file.lower().endswith('.htm'):
            raise FileExistsError("Falscher Dateityp! Es muss eine Datei mit der Endung .htm gewählt werden!")

    @staticmethod
    def check_across_htm_file(htm_file):
        with open(htm_file, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.startswith('<HTML><HEAD>\n<META content="text/html; charset=UTF-8" http-equiv=Content-Type>'):
            raise ValueError("Es handelt sich nicht um eine Across-spezifische Druckversion der Übersetzung!")

    @staticmethod
    def check_tag_file(tag_file):
        if not tag_file.endswith(".json"):
            raise ValueError("Fehler! Bei der ausgewählten Datei handelt es sich nicht um eine json-Datei!")

    @staticmethod
    def validate_json_schema(tag_file):

        with open("tag_schema.json", "r", encoding="utf-8") as file:
            schema = json.load(file)

        try:
            validate(instance=tag_file, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError:
            raise ValueError("Die ausgewählte json-Datei besitzt kein gültiges Format.")

    @staticmethod
    def validate_file_existence(file):
        if not os.path.exists(file):
            raise OSError("Die angegebene Datei existiert nicht!")

    @staticmethod
    def check_empty_string(string):
        if string == '':
            raise ValueError("Ein oder mehrere Pflichtfelder sind nicht ausgefüllt!")
