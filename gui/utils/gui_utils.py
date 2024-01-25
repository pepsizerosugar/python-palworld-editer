from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QSlider, QLineEdit, QRadioButton, QButtonGroup, QTableWidgetItem, QLabel, \
    QWidget, QHBoxLayout

from utils.translation_utils import convert_translation_list_to_dict


def center_on_screen(widget):
    # 현재 스크린의 중앙 좌표를 구함
    screen_rect = QApplication.desktop().screenGeometry()
    x = (screen_rect.width() - widget.width()) // 2
    y = (screen_rect.height() - widget.height()) // 2

    # 위젯을 중앙 좌표로 이동
    widget.move(x, y)


def create_widget_for_option(value):
    if isinstance(value, str) and value.lower() in ['true', 'false']:
        value = value.lower() == 'true'

    if isinstance(value, bool):
        value_radio_true = QRadioButton("True")
        value_radio_false = QRadioButton("False")

        radio_button_group = QButtonGroup()
        radio_button_group.addButton(value_radio_true)
        radio_button_group.addButton(value_radio_false)

        value_radio_true.setChecked(value)
        value_radio_false.setChecked(not value)

        # 라디오 버튼 핸들링
        def update_radio_button():
            if value_radio_true.isChecked():
                value_radio_false.setChecked(False)
            else:
                value_radio_true.setChecked(False)

        value_radio_true.toggled.connect(lambda: update_radio_button())
        value_radio_false.toggled.connect(lambda: update_radio_button())

        return value_radio_true, value_radio_false

    if isinstance(value, (int, float)):
        value_slider = QSlider(Qt.Horizontal)
        value_slider.setRange(0, 100)
        value_slider.setValue(int(value))

        def update_slider(val):
            value_line_edit.setText(f"{val}")
            value_slider.setValue(val)

        def update_line_edit(text):
            if text:
                value_slider.setValue(int(float(text)))

        value_slider.valueChanged.connect(update_slider)

        value_line_edit = QLineEdit(f"{value}")
        validator = QDoubleValidator()
        value_line_edit.setValidator(validator)
        value_line_edit.textChanged.connect(lambda text: update_line_edit(text))

        return value_slider, value_line_edit
    else:
        value_line_edit = QLineEdit(str(value))

        return value_line_edit


def resize_windows(self):
    self.total_width = sum(self.table_widget.columnWidth(col) for col in range(self.table_widget.columnCount()))
    self.resize(self.total_width + 65, self.size().height() + 800)


def set_table_widget_data(self, is_first_load):
    self.options.pop("OptionSettings")
    self.translations = convert_translation_list_to_dict(self.translations)

    # 첫 파일 로드 시는 데이터 삽입
    if is_first_load:
        for option, value in self.options.items():
            widgets = create_widget_for_option(value)
            add_row_to_table(self, option, widgets)
    else:
        # 이후 파일 로드 시는 기존 테이블 데이터 갱신
        # 갱신 기준은 설정 항목
        for row in range(self.table_widget.rowCount()):
            # 기존 설정 항목 가져오기
            exist_option = self.table_widget.item(row, 0).text()

            # 기존 설정 항목이 새로 불러온 설정 항목에도 존재하는 경우
            if exist_option in self.options:
                # 기존 설정 항목의 아이템을 가져온다
                # TODO: item과 widget의 조건에 따라 처리 필요:wq
                exist_item = self.table_widget.item(row, 2)
                if exist_item:
                    pass
                else:
                    exist_item = self.table_widget.cellWidget(row, 2)
                    pass
            else:
                # 기존 설정 항목이 새로 불러온 설정 항목에는 존재하지 않는 경우
                # 기존 설정 항목을 테이블에서 삭제
                self.table_widget.removeRow(row)

    self.table_widget.resizeColumnsToContents()
    resize_windows(self)
    center_on_screen(self)


def create_table_cell_widget(widgets):
    if isinstance(widgets, tuple):
        widget_container = QWidget()
        h_layout = QHBoxLayout(widget_container)

        for widget in widgets:
            h_layout.addWidget(widget)

        return widget_container
    else:
        return QTableWidgetItem(str(widgets.text()))


def add_row_to_table(self, option, widgets):
    # 테이블에 행 추가
    row_position = self.table_widget.rowCount()
    self.table_widget.insertRow(row_position)

    # 설정 항목 열 추가
    item_option = QTableWidgetItem(option)
    item_option.setFlags(Qt.ItemIsEnabled)
    self.table_widget.setItem(row_position, 0, item_option)

    # 번역 열 추가
    translation_label = QLabel(self.translations.get(option, {}).get(self.translation_code, option))
    self.table_widget.setCellWidget(row_position, 1, translation_label)

    cell_item = create_table_cell_widget(widgets)

    if isinstance(widgets, tuple):
        self.table_widget.setCellWidget(row_position, 2, cell_item)
    else:
        self.table_widget.setItem(row_position, 2, cell_item)

    self.table_widget.setRowHeight(row_position, 35)
