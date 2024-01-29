from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from utils.file_utils import load_settings_file
from utils.translation_utils import change_translation_code


class BrowseWindow:
    def __init__(self):
        UIElements.browse_translation_label = QLabel()
        UIElements.browse_translation_label.setText("Translation code")

        UIElements.browse_translation_combo = QComboBox()
        UIElements.browse_translation_combo.addItems(DataElements.translation_code_list)
        UIElements.browse_translation_combo.currentIndexChanged.connect(
            lambda index: change_translation_code(index))

        UIElements.browse_load_file_button = QPushButton()
        UIElements.browse_load_file_button.setText('Load Settings File')
        UIElements.browse_load_file_button.clicked.connect(lambda: load_settings_file(UIElements.browse_window))

        UIElements.browse_interaction_layout = QVBoxLayout()
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(UIElements.browse_translation_label)
        hbox_layout.addWidget(UIElements.browse_translation_combo)
        UIElements.browse_interaction_layout.addLayout(hbox_layout)
        UIElements.browse_interaction_layout.addWidget(UIElements.browse_load_file_button)

        UIElements.browse_box_layout = QVBoxLayout()
        UIElements.browse_box_layout.addWidget(UIElements.banner_label)
        UIElements.browse_box_layout.addSpacing(10)
        UIElements.browse_box_layout.addLayout(UIElements.browse_interaction_layout)

        UIElements.browse_central_widget = QWidget()
        UIElements.browse_central_widget.setLayout(UIElements.browse_box_layout)
        UIElements.browse_window.setCentralWidget(UIElements.browse_central_widget)
