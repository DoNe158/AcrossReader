import os
import re


class AcrossReader:

    def __init__(self, segment_id, source, translation):
        self.id = segment_id
        self.source = source
        self.translation = translation

    @classmethod
    def read_htm_file(cls, htm_file):
        """
        Reads a file in htm format that is generated by Across and converts the text into a csv file that contains
        the segment id, the source text, and the translated text. "§" is used as a separator.
        """

        file_to_store = cls.__generate_destination_file__(htm_file)

        with open(htm_file, "r", encoding="utf-8") as file_to_be_read:
            lines = file_to_be_read.readlines()
            counter = 1
            translations = list()
            source = ''

            for entry in lines:
                if entry.startswith("<DIV id=contents"):
                    tmp = re.sub("<DIV id=contents.*?<SPAN class=atom>", "", entry)

                    if counter == 2:
                        source = re.sub("</SPAN></PRE></DIV></TD>", "", tmp)[:-1]
                        source = cls.__remove_nbsp_tag__(source)
                        source = cls.__remove_tags_inline(source)
                        counter += 1

                    elif counter == 3:
                        translation = re.sub("</SPAN></PRE></DIV></TD>", "", tmp)
                        translation = re.sub("</TR>", "", translation)
                        translation = cls.__remove_nbsp_tag__(translation)
                        translation = cls.__remove_tags_inline(translation)
                        counter = 1
                        translation_entry = AcrossReader(segment_id, source, translation)
                        translations.append(translation_entry)

                if 'inactiveNumbering" width=' in entry and counter == 1:
                    segment_id = re.sub('<TD.*?MARGIN: 2px 0px 0px"><SPAN class=atom>', "", entry)
                    segment_id = re.sub("</SPAN></PRE></TD>", "", segment_id)[:-1]
                    counter += 1

            all_translations_to_store = cls.__remove_duplicates__(translations)

            with open(file_to_store, "w", encoding="utf-8") as file:
                file.write(all_translations_to_store)

    @classmethod
    def __remove_duplicates__(cls, translation_list):
        """
        Removes entries that occur multiple times in a given list containing translation entries (consist segment id,
        source text, and translation.

        :param translation_list: list containing all translations of the text. The entries are instances of the class
        AcrossReader.
        :return: list holding translations without duplicates.
        """

        list_without_duplicates = list()
        translation_entry = ''
        list_without_duplicates.append(AcrossReader("ID", "Ausgangstext", "Übersetzung\n"))

        for entry in translation_list:
            exists = False
            for entry_without_duplicates in list_without_duplicates:
                if entry_without_duplicates.source == entry.source:
                    exists = True
                    break

            if exists is False:
                list_without_duplicates.append(entry)

        for entry in list_without_duplicates:
            translation_entry += entry.id + "§" + entry.source + "§" + entry.translation

        return translation_entry

    @classmethod
    def __remove_tags_inline(cls, line):
        """
        Removes tags that occur within the text and removes them or replaces them with <TAG>.

        :param line: one segment holding the source text or the translation.
        :return: line without any specific tags.
        """

        line_cleaned = re.sub("<WBR><IMG.*?<SPAN class=atom>", "<TAG>", line)
        line_cleaned = re.sub("</SPAN>", "", line_cleaned)
        line_cleaned = re.sub("<WBR>", "", line_cleaned)
        line_cleaned = re.sub("</PRE>", "", line_cleaned)
        line_cleaned = re.sub("</DIV>", "", line_cleaned)
        line_cleaned = re.sub("</TD>", "", line_cleaned)
        line_cleaned = re.sub('<IMG id.*?png">', "", line_cleaned)
        line_cleaned = re.sub('&nbsp;', " ", line_cleaned)

        return line_cleaned

    @classmethod
    def __remove_nbsp_tag__(cls, translation_string):
        """
        Removes nbsp tags within the translation.

        :param translation_string: one segment holding the source text or the translation.
        :return: segment without any nbsp tags
        """

        if 'class=field alt=&amp;nbsp; src=' in translation_string:
            tmp = re.sub('</SPAN>.*?<SPAN class=atom>', ' ', translation_string)
            return tmp
        else:
            return translation_string

    @classmethod
    def __generate_destination_file__(cls, path):
        """
        Creates the path of the file where the processed file is to be stored. The suffix '_translated' will be added
        to the destination file automatically.

        :param path: path of the source file.
        :return: path of the destination file.
        """

        directory_name = os.path.dirname(path) + "/"
        file_name = os.path.basename(path)
        file_name = file_name.split('.')[0]
        file_name_translation = file_name + "_translated.txt"
        path_translation = directory_name + file_name_translation

        return path_translation
