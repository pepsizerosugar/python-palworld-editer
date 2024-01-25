from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout

from utils.file_utils import load_settings_file
from utils.translation_utils import change_translation_code


class BrowseWidget:
    def __init__(self, parent=None):
        self.translation_label = QLabel(parent)
        self.translation_label.setText("Translation code")

        self.translation_combo = QComboBox(parent)
        self.translation_combo.addItems(["ko", "en", "jp"])
        self.translation_combo.currentIndexChanged.connect(lambda index: change_translation_code(parent, index))

        self.load_button = QPushButton(parent)
        self.load_button.setText('Load Settings File')
        self.load_button.clicked.connect(lambda: load_settings_file(parent))

    def get_layout(self):
        layout = QVBoxLayout()
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.translation_label)
        hbox_layout.addWidget(self.translation_combo)
        layout.addLayout(hbox_layout)
        layout.addWidget(self.load_button)
        return layout
