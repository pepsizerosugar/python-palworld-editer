from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.labels.banner_label import BannerLabel
from gui.widgets.browse_widget import BrowseWidget


class InitializeUI:
    def __init__(self):
        DataElements.translation_code = "ko"
        DataElements.is_first_load = True

        UIElements.main_window.setGeometry(300, 300, 460, 230)
        UIElements.main_window.setWindowTitle('PalWorld Advanced Server Settings Helper')

        BannerLabel.__init__(self)
        BrowseWidget().__init__()
