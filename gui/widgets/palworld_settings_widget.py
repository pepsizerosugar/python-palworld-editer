from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QAction

from gui.labels.banner_label import BannerLabel
from gui.utils.gui_utils import center_on_screen, resize_windows
from gui.widgets.browse_widget import BrowseWidget
from utils.file_utils import load_settings_file, save_settings_file


class PalWorldSettingsWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 초기화
        self.translation_code = "ko"
        self.central_widget = None
        self.options = None
        self.translations = None
        self.table_widget = None
        self.total_width = None
        self.init_ui()

    def init_ui(self):
        # 이미지 배너 삽입
        banner_label = BannerLabel(self)

        # 번역 코드 표시 라벨, 번역 코드 선택 콤보 박스, 설정 파일 불러오기 버튼
        browse_widgets = BrowseWidget(self)

        # UI 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(banner_label)
        layout.addSpacing(10)  # 간격 추가
        layout.addLayout(browse_widgets.get_layout())

        # 브라우저의 Central Widget 설정
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 창 설정
        self.setGeometry(300, 300, 460, 230)
        self.setWindowTitle('PalWorld Settings GUI')
        self.show()
        center_on_screen(self)

    def init_central_widget(self):
        # 위젯 생성
        self.central_widget = QWidget()
        layout = QVBoxLayout(self.central_widget)

        # 메뉴 바 생성
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # 메뉴 액션 생성
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
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["설정 항목", "번역", "설정 UI"])

        # 테이블 위젯을 레이아웃에 추가
        layout.addWidget(self.table_widget)
        self.setCentralWidget(self.central_widget)
