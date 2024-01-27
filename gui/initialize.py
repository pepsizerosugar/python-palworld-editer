from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.labels.banner_label import BannerLabel
from gui.utils.gui_utils import move_center
from gui.widgets.browse_widget import BrowseWidget
from gui.widgets.palworld_settings_widget import PalWorldSettingsWidget


class InitializeUI:
    def __init__(self):
        DataElements.translation_code = "ko"
        DataElements.is_first_load = True

        UIElements.browse_window.setGeometry(300, 300, 460, 230)
        UIElements.browse_window.setWindowTitle('PalWorld Advanced Server Settings Helper')

        BannerLabel()
        BrowseWidget()
        UIElements.settings_window = PalWorldSettingsWidget()
        move_center(UIElements.browse_window)
