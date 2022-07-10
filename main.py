from Implementation.GUI import GUI
from Implementation.Logic import AcrossReader

if __name__ == '__main__':

    gui_impl = GUI.GUI()
    across_reader_impl = AcrossReader.AcrossReader()

    gui_impl.start_application(across_reader_impl)

