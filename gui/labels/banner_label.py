from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtWidgets import QLabel

from gui.messageboxs.message_boxs import if_error_when_load_banner_image


class BannerLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.load_banner()

    def load_banner(self):
        self.setAlignment(Qt.AlignCenter)
        banner_path = 'resources/banner.jpg'
        if QImageReader(banner_path).size().width() > 0:  # 이미지가 존재하는지 확인
            pixmap = QPixmap(banner_path)
            self.setPixmap(pixmap)
        else:
            if_error_when_load_banner_image(e)
