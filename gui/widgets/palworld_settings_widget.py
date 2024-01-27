from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QMainWindow

from gui.dataclass.ui_elements import UIElements
from utils.file_utils import load_settings_file, save_settings_file, save_as_settings_file


class PalWorldSettingsWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        UIElements.settings_window = self
        UIElements.settings_window.setDisabled(True)
        # 위젯 생성
        UIElements.settings_central_widget = QWidget()
        UIElements.settings_box_layout = QVBoxLayout(UIElements.settings_central_widget)

        # 메뉴 바 생성
        UIElements.settings_menu_bar = UIElements.settings_window.menuBar()
        UIElements.settings_menu_bar.setNativeMenuBar(False)
        UIElements.settings_menu_bar.addSeparator()
        UIElements.settings_menu_bar_file = UIElements.settings_menu_bar.addMenu('File')

        # 메뉴 액션 생성
        load_action = UIElements.settings_menu_bar_file.addAction('Load')
        save_action = UIElements.settings_menu_bar_file.addAction('Save')
        save_as_action = UIElements.settings_menu_bar_file.addAction('Save As')
        exit_action = UIElements.settings_menu_bar_file.addAction('Exit')

        load_action.setShortcut('Ctrl+D')
        save_action.setShortcut('Ctrl+S')
        save_as_action.setShortcut('Ctrl+Shift+S')
        exit_action.setShortcut('Ctrl+Q')

        load_action.triggered.connect(lambda: load_settings_file(UIElements.settings_window))
        save_action.triggered.connect(lambda: save_settings_file())
        save_as_action.triggered.connect(lambda: save_as_settings_file())
        exit_action.triggered.connect(UIElements.settings_window.close)

        # 테이블 위젯 생성
        UIElements.settings_table_widget = QTableWidget()
        UIElements.settings_table_widget.setColumnCount(3)
        UIElements.settings_table_widget.setHorizontalHeaderLabels(["설정 항목", "번역", "설정 UI"])

        # 테이블 위젯을 레이아웃에 추가
        UIElements.settings_box_layout.addWidget(UIElements.settings_table_widget)
        UIElements.settings_window.setCentralWidget(UIElements.settings_central_widget)
