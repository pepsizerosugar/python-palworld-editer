import qtmodern.styles
import qtmodern.windows
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QAction, QMenuBar, QMainWindow

from gui.dataclass.ui_elements import UIElements
from gui.utils.gui_utils import resize_windows


class PalWorldSettingsWidget:
    def __init__(self):
        UIElements.settings_window = QMainWindow()
        # 위젯 생성
        UIElements.settings_central_widget = QWidget()
        UIElements.settings_box_layout = QVBoxLayout(UIElements.settings_central_widget)

        # 메뉴 바 생성
        UIElements.settings_menu_bar = QMenuBar()
        UIElements.settings_menu_bar_file = UIElements.settings_menu_bar.addMenu('File')

        # 메뉴 액션 생성
        load_action = QAction('Load')
        load_action.setShortcut('Ctrl+D')
        # load_action.triggered.connect(lambda: load_settings_file(self))

        save_action = QAction('Save')
        save_action.setShortcut('Ctrl+S')
        # save_action.triggered.connect(lambda: save_settings_file(self))

        exit_action = QAction('Exit')
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(UIElements.browse_window.close)

        # 액션 메뉴에 추가
        UIElements.settings_menu_bar_file.addAction(load_action)
        UIElements.settings_menu_bar_file.addAction(save_action)
        UIElements.settings_menu_bar_file.addAction(exit_action)

        # 메뉴 바를 레이아웃에 추가
        UIElements.settings_box_layout.setMenuBar(UIElements.settings_menu_bar)

        # 테이블 위젯 생성
        UIElements.settings_table_widget = QTableWidget()
        UIElements.settings_table_widget.setColumnCount(3)
        UIElements.settings_table_widget.setHorizontalHeaderLabels(["설정 항목", "번역", "설정 UI"])

        # 테이블 위젯을 레이아웃에 추가
        UIElements.settings_box_layout.addWidget(UIElements.settings_table_widget)
        UIElements.settings_window.setCentralWidget(UIElements.settings_central_widget)

        resize_windows()
        UIElements.settings_window = qtmodern.windows.ModernWindow(UIElements.settings_window)
        UIElements.settings_window.show()
