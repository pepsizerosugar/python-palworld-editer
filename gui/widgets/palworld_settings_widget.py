import qtmodern.styles
import qtmodern.windows
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QMainWindow

from gui.dataclass.ui_elements import UIElements


class PalWorldSettingsWidget:
    def __init__(self):
        UIElements.settings_window = QMainWindow()
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

        save_action.setShortcut('Ctrl+S')
        load_action.setShortcut('Ctrl+D')
        save_as_action.setShortcut('Ctrl+Shift+A')
        exit_action.setShortcut('Ctrl+Q')

        # load_action.triggered.connect(lambda: load_settings_file())
        # save_action.triggered.connect(lambda: save_settings_file(self))
        # save_as_action.triggered.connect(lambda: save_settings_file(self))
        exit_action.triggered.connect(UIElements.settings_window.close)

        # 테이블 위젯 생성
        UIElements.settings_table_widget = QTableWidget()
        UIElements.settings_table_widget.setColumnCount(3)
        UIElements.settings_table_widget.setHorizontalHeaderLabels(["설정 항목", "번역", "설정 UI"])

        # 테이블 위젯을 레이아웃에 추가
        UIElements.settings_box_layout.addWidget(UIElements.settings_table_widget)
        UIElements.settings_window.setCentralWidget(UIElements.settings_central_widget)

        UIElements.settings_window = qtmodern.windows.ModernWindow(UIElements.settings_window)
        UIElements.settings_window.show()
