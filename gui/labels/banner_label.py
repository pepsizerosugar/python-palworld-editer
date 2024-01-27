from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtWidgets import QLabel

from gui.dataclass.ui_elements import UIElements
from gui.messageboxs.message_boxs import if_error_when_load_banner_image


class BannerLabel:
    def __init__(self):
        UIElements.banner_label = QLabel()
        UIElements.banner_label.setAlignment(Qt.AlignCenter)
        banner_path = 'resources/img/banner.jpg'
        try:
            if QImageReader(banner_path).size().width() > 0:
                pixmap = QPixmap(banner_path)
                UIElements.banner_label.setPixmap(pixmap)
            else:
                raise Exception
        except Exception as e:
            if_error_when_load_banner_image(e)
            UIElements.banner_label.setText("Banner Image Not Found")
