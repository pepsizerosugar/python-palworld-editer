"""Editor window that presents the settings table and actions."""

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QVBoxLayout, QWidget

from gui.dataclass.ui_elements import UIElements
from utils.file_utils import load_settings_file, save_as_settings_file, save_settings_file


class EditorWindow(QMainWindow):
    """Main editing surface for Palworld server options."""

    def __init__(self) -> None:
        """Build menu actions and the editable settings table."""

        super().__init__()
        UIElements.editor_window = self
        UIElements.editor_window.setDisabled(True)
        UIElements.editor_central_widget = QWidget()
        UIElements.editor_box_layout = QVBoxLayout(UIElements.editor_central_widget)

        UIElements.editor_menu_bar = UIElements.editor_window.menuBar()
        UIElements.editor_menu_bar.setNativeMenuBar(False)
        UIElements.editor_menu_bar.addSeparator()
        UIElements.editor_menu_bar_file = UIElements.editor_menu_bar.addMenu("File")

        load_action = UIElements.editor_menu_bar_file.addAction("Load")
        save_action = UIElements.editor_menu_bar_file.addAction("Save")
        save_as_action = UIElements.editor_menu_bar_file.addAction("Save As")
        exit_action = UIElements.editor_menu_bar_file.addAction("Exit")

        load_action.setShortcut("Ctrl+D")
        save_action.setShortcut("Ctrl+S")
        save_as_action.setShortcut("Ctrl+Shift+S")
        exit_action.setShortcut("Ctrl+Q")

        load_action.triggered.connect(lambda: load_settings_file(UIElements.editor_window))
        save_action.triggered.connect(lambda: save_settings_file())
        save_as_action.triggered.connect(lambda: save_as_settings_file())
        exit_action.triggered.connect(UIElements.editor_window.close)

        UIElements.editor_table_widget = QTableWidget()
        UIElements.editor_table_widget.setColumnCount(3)
        UIElements.editor_table_widget.setHorizontalHeaderLabels(["Option", "Value", "Description"])

        UIElements.editor_box_layout.addWidget(UIElements.editor_table_widget)
        UIElements.editor_window.setCentralWidget(UIElements.editor_central_widget)
