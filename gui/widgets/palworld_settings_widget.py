from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, \
    QAction

from gui.labels.banner_label import BannerLabel
from gui.utils.gui_utils import center_on_screen, create_widget_for_option, resize_windows
from gui.widgets.browse_widget import BrowseWidget
from utils.file_utils import load_settings_file, save_settings_file
from utils.translation_utils import convert_translation_list_to_dict


class PalWorldSettingsWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 초기화
        self.table_widget = None
        self.total_width = None
        self.translation_code = None
        self.central_widget = None
        self.options = None
        self.translations = None
        self.init_ui()

    def init_ui(self):
        # 기본 번역 코드 설정
        self.translation_code = "ko"

        # 이미지 배너 삽입
        banner_label = BannerLabel(self)

        # 번역 코드 표시 라벨, 번역 코드 선택 콤보 박스, 설정 파일 불러오기 버튼
        browse_widgets = BrowseWidget(self)

        # UI 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(banner_label)
        layout.addSpacing(10)  # 간격 추가
        layout.addLayout(browse_widgets.get_layout())

        # Central Widget 설정
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 창 설정
        self.setGeometry(300, 300, 460, 230)  # 가로 460, 세로 230으로 설정
        self.setWindowTitle('PalWorld Settings GUI')
        self.show()
        center_on_screen(self)

    def change_translation_code(self, index):
        self.translation_code = ["ko", "en"][index]
        # TODO: 현재 설정된 번역 코드로 UI 업데이트

    def show_settings_ui(self):
        self.central_widget = QWidget()
        layout = QVBoxLayout(self.central_widget)
        self.options.pop("OptionSettings")
        self.translations = convert_translation_list_to_dict(self.translations)

        # 메뉴 바 생성
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # 액션 생성
        load_action = QAction('Load', self)
        load_action.setShortcut('Ctrl+D')
        load_action.triggered.connect(lambda: load_settings_file(self))

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(lambda: save_settings_file(self))

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        # 액션 메뉴에 추가
        file_menu.addAction(load_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        # 메뉴 바를 레이아웃에 추가
        layout.setMenuBar(menubar)

        # 테이블 위젯 생성
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)  # 열 개수 설정
        self.table_widget.setHorizontalHeaderLabels(["설정 항목", "번역", "설정 UI"])

        for option, value in self.options.items():
            widgets = create_widget_for_option(option, value)
            self.add_row_to_table(self.table_widget, option, widgets)

        # 테이블 열의 크기를 열의 내용에 맞게 동적으로 조절
        self.table_widget.resizeColumnsToContents()

        # 창 크기 조절은 첫 한 번 만 실행
        if not self.total_width:
            resize_windows(self)

        # 테이블 위젯을 레이아웃에 추가
        layout.addWidget(self.table_widget)
        self.setCentralWidget(self.central_widget)
        center_on_screen(self)

    def add_row_to_table(self, table_widget, option, widgets):
        # 테이블에 행 추가
        row_position = table_widget.rowCount()
        table_widget.insertRow(row_position)

        # 설정 항목 열 추가
        item_option = QTableWidgetItem(option)
        item_option.setFlags(Qt.ItemIsEnabled)
        table_widget.setItem(row_position, 0, item_option)

        # 번역 열 추가
        translation_label = QLabel(self.translations.get(option, {}).get(self.translation_code, option))
        table_widget.setCellWidget(row_position, 1, translation_label)

        # 설정 UI 열 추가
        if isinstance(widgets, tuple):
            widget_container = QWidget()
            h_layout = QHBoxLayout(widget_container)

            for widget in widgets:
                h_layout.addWidget(widget)

            table_widget.setCellWidget(row_position, 2, widget_container)
        else:
            table_widget.setItem(row_position, 2, QTableWidgetItem(str(widgets.text())))

        table_widget.setRowHeight(row_position, 35)
