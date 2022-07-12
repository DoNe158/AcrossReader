import abc
from abc import ABC, ABCMeta


class IGUI(ABC):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def start_application(self, across_reader):
        """
        Starts the application.

        :param across_reader: instance of the AcrossReader class.
        """
        pass

    @abc.abstractmethod
    def read_htm(self, across_reader):
        """
        Opens dialog for reading the htm file and the json tag file.

        :param across_reader: instance of the AcrossReader class.
        """
        pass

    @abc.abstractmethod
    def create_new_tag_file(self, across_reader):
        """
        Opens dialog for creating a new empty tag file.

        :param across_reader: instance of the AcrossReader class.
        """
        pass

    @abc.abstractmethod
    def open_file(self, tag_file, across_reader):
        """
        Opens the dialog for adding and deleting tags in the given tag file.

        :param tag_file: json file that contains tags (or empty dictionary).
        :param across_reader: instance of the AcrossReader class.

        """
        pass

    @abc.abstractmethod
    def delete_tag(self, tag_file, tag_to_be_deleted, window, across_reader):
        """
        Handling the deletion of the given tag in the given tag file if existing.

        :param tag_file: json file that contains tags (or at least an empty dictionary in the correct format).
        :param tag_to_be_deleted: tag that is to be deleted.
        :param window: tkinter window.
        :param across_reader: instance of the AcrossReader class.
        """
        pass

    @abc.abstractmethod
    def save_to_tag_file(self, tag_list, tag_file, window, across_reader):
        """
        Handles the storing process of a new tag to the given tag file.

        :param tag_list: list containing the information of the new tag that is to be stored.
        :param tag_file: json file that contains tags (or at least an empty dictionary in the correct format).
        :param window: tkinter window.
        :param across_reader: instance of the AcrossReader class.
        """
        pass

