from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.labels.banner_label import BannerLabel
from gui.utils.gui_utils import move_center
from gui.window.browse_window import BrowseWindow
from gui.window.editor_window import EditorWindow
from utils.file_utils import init_file_utils


class InitializeUI:
    def __init__(self):
        init_file_utils()

        DataElements.translation_code = "ko"
        DataElements.is_first_load = True

        UIElements.browse_window.setGeometry(300, 300, 460, 230)
        UIElements.browse_window.setWindowTitle(DataElements.metadata.get("title"))

        BannerLabel()
        BrowseWindow()
        UIElements.editor_window = EditorWindow()
        UIElements.editor_window.setWindowTitle(DataElements.metadata.get("title"))
        move_center(UIElements.browse_window)
