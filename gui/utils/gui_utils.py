from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QSlider, QLineEdit, QRadioButton, QButtonGroup, QTableWidgetItem, QLabel, \
    QWidget, QHBoxLayout, QDesktopWidget

from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from utils.translation_utils import convert_translation_list_to_dict


def move_center(window):
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())


def resize_windows():
    total_width = 65
    for column in range(UIElements.settings_table_widget.columnCount()):
        total_width += UIElements.settings_table_widget.columnWidth(column)
    total_height = QDesktopWidget().availableGeometry().height() * 0.8
    UIElements.settings_window.resize(total_width, int(total_height))


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


def set_table_widget_data():
    DataElements.palworld_options.pop("OptionSettings")
    DataElements.options_translations = convert_translation_list_to_dict(DataElements.options_translations)

    # 첫 파일 로드 시는 데이터 삽입
    if DataElements.is_first_load:
        for option, value in DataElements.palworld_options.items():
            UIElements.settings_value_widget = create_widget_for_option(value)
            add_row_to_table(option, UIElements.settings_value_widget)
    else:
        # 이후 파일 로드 시는 기존 테이블 데이터 갱신
        # 갱신 기준은 설정 항목이 있는 경우만, 없으면 해당 설정 항목 삭제
        for row in range(UIElements.settings_table_widget.rowCount()):
            # 기존 설정 항목 가져오기
            exist_option = UIElements.settings_table_widget.item(row, 0).text()

            # 기존 설정 항목이 새로 불러온 설정 항목에도 존재하는 경우
            if exist_option in DataElements.palworld_options:
                # 기존 설정 항목의 설정 값 아이템을 가져온다
                # TODO: item과 widget의 조건에 따라 처리 필요:wq
                exist_item = UIElements.settings_table_widget.item(row, 2)
                if exist_item:
                    # 어떤 아이템 타입인지 확인
                    if isinstance(exist_item, QTableWidgetItem):
                        print(type(exist_item), exist_option, DataElements.palworld_options[exist_option],
                              exist_item.text())
                        pass
                    else:
                        print(type(exist_item), exist_option, DataElements.palworld_options[exist_option],
                              exist_item.text())
                        pass
                else:
                    exist_widget = UIElements.settings_table_widget.cellWidget(row, 2)
                    print(type(exist_widget), exist_option, DataElements.palworld_options[exist_option], exist_widget)
                    pass
            else:
                # 기존 설정 항목이 새로 불러온 설정 항목에는 존재하지 않는 경우
                # 기존 설정 항목을 테이블에서 삭제
                print("delete", exist_option)
                UIElements.settings_table_widget.removeRow(row)

    UIElements.settings_table_widget.resizeColumnsToContents()


def add_row_to_table(option, widgets):
    # 테이블에 행 추가
    row_position = UIElements.settings_table_widget.rowCount()
    UIElements.settings_table_widget.insertRow(row_position)

    # 설정 항목 열 추가
    item_option = QTableWidgetItem(option)
    item_option.setFlags(Qt.ItemIsEnabled)
    UIElements.settings_table_widget.setItem(row_position, 0, item_option)

    # 번역 열 추가
    translation_label = QLabel(
        DataElements.options_translations.get(option, {}).get(DataElements.translation_code, option))
    UIElements.settings_table_widget.setCellWidget(row_position, 1, translation_label)

    cell_item = create_table_cell_widget(widgets)

    if isinstance(widgets, tuple):
        UIElements.settings_table_widget.setCellWidget(row_position, 2, cell_item)
    else:
        UIElements.settings_table_widget.setItem(row_position, 2, cell_item)

    UIElements.settings_table_widget.setRowHeight(row_position, 35)


def create_table_cell_widget(widgets):
    if isinstance(widgets, tuple):
        widget_container = QWidget()
        h_layout = QHBoxLayout(widget_container)

        for widget in widgets:
            h_layout.addWidget(widget)

        return widget_container
    else:
        return QTableWidgetItem(str(widgets.text()))
