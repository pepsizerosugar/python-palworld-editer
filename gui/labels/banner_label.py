"""Banner label that attempts to show the application header image."""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImageReader, QPixmap
from PyQt5.QtWidgets import QLabel

from gui.dataclass.ui_elements import UIElements
from gui.messageboxs.message_boxs import if_error_when_load_banner_image


class BannerLabel:
    """Create and attach a banner image label to the UI registry."""

    def __init__(self) -> None:
        """Load the banner image, falling back to text when missing."""

        UIElements.banner_label = QLabel()
        UIElements.banner_label.setAlignment(Qt.AlignCenter)
        banner_path = "resources/img/banner.jpg"
        try:
            if QImageReader(banner_path).size().width() > 0:
                pixmap = QPixmap(banner_path)
                UIElements.banner_label.setPixmap(pixmap)
            else:
                raise Exception
        except Exception as error:  # pylint: disable=broad-except
            if_error_when_load_banner_image(error)
            UIElements.banner_label.setText("Banner Image Not Found")
