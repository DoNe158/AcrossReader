import abc
from abc import ABC, ABCMeta


class IAcrossReader(ABC):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def read_htm_file(self, htm_file, tag_file) -> bool:
        """
        Reads an htm file that is printed by Across.

        :param htm_file: htm file to be read.
        :param tag_file: tag file containing translation specific tags.
        :return: Boolean whether the transaction was successful (True) or not (False).
        """
        pass

    @abc.abstractmethod
    def save_to_tag_file(self, tag_list, tag_file) -> bool:
        """
        Saves a new tag entry to an existing tag file.

        :param tag_list: information of the tag (name, opening tag, closing tag, to be shown or not) in a list.
        :param tag_file: json file where the tag is to be stored.
        :return: Boolean whether the transaction was successful (True) or not (False).
        """
        pass

    @staticmethod
    def create_new_tag_file(tag_file_path):
        """
        Creates an empty json file with the basic structure (dictionary with data: []).

        :param tag_file_path: path of the json file that is to be created.
        """
        pass

    @staticmethod
    def show_tags(tag_file) -> list:
        """
        Shows all tags with their information that are stored in the given json file that contains the tags.

        :param tag_file: json file that contains the tags.
        :return: list with tags and their specific information (name, to be shown, opening tag, closing tag.
        """
        pass

    @abc.abstractmethod
    def delete_tag(self, tag_file, tag_to_be_deleted) -> bool:
        """
        Deletes the given tag in the given json tag file.

        :param tag_file: json file that contains the tags.
        :param tag_to_be_deleted: tag that is to be deleted.
        :return: Boolean whether the transaction was successful (True) or not (False)
        """
        pass

    @classmethod
    def write_file_to_docx(cls, translation_list_with_AcrossReader, document_name):
        """
        Takes a list with AcrossEntry stored in a AcrossReader instance and stores all entries in a docx document
        with the given document name.

        :param translation_list_with_AcrossReader: list of instances of AcrossEntry.
        :param document_name: name of the document where the translation should be saved.
        """
        pass
