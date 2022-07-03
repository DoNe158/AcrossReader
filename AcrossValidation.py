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
            raise BaseException("Es handelt sich nicht um eine Across-spezifische Druckversion der Übersetzung!")
