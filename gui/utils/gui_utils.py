from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QSlider, QLineEdit, QRadioButton, QButtonGroup, QTableWidgetItem, QLabel, \
    QWidget, QHBoxLayout, QDesktopWidget

from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.messageboxs.message_boxs import if_error_when_update_settings, if_update_settings_finished
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


def set_table_widget_data():
    DataElements.palworld_options.pop("OptionSettings")
    DataElements.options_translations = convert_translation_list_to_dict(DataElements.options_translations)

    # 첫 파일 로드 시는 데이터 삽입
    if DataElements.is_first_load:
        for option, value in DataElements.palworld_options.items():
            create_widget_for_value_widget(option, value)
    else:
        exist_options = {}

        for row in range(UIElements.settings_table_widget.rowCount()):
            exist_options.update({UIElements.settings_table_widget.item(row, 0).text(): row})

        for option in DataElements.palworld_options.keys():
            if option in exist_options:
                update_settings(exist_options[option], option, DataElements.palworld_options[option])
            else:
                create_widget_for_value_widget(option, DataElements.palworld_options[option])

        if_update_settings_finished()

    UIElements.settings_table_widget.resizeColumnsToContents()


def create_widget_for_value_widget(option, value):
    settings_value_widget = create_widget_for_option_value(
        value) if option not in DataElements.special_palworld_options else QLineEdit(str(value))
    add_row_to_table(option, settings_value_widget)


def update_settings(row_index, option, value):
    """
        글자형(텍스트 입력) = QTableWidgetItem
        숫자형(슬라이더 + 숫자 입력), 선택형(라디오 버튼) = QWidget
    """
    exist_item = UIElements.settings_table_widget.item(row_index, 2)
    if exist_item:
        update_settings_to_table_with_qtable_item(exist_item, value)
    else:
        exist_widget = UIElements.settings_table_widget.cellWidget(row_index, 2)
        update_settings_to_table_with_qtable_widget(exist_widget, option, value)


def refine_value_for_slider(value):
    DataElements.input_value = float(value)
    slider_value = int(DataElements.input_value * 10)
    slider_value = max(0, min(slider_value, 1000))
    return slider_value


def create_widget_for_option_value(value):
    if isinstance(value, (int, float)):
        value_slider = QSlider(Qt.Horizontal)
        value_slider.setRange(0, 1000)
        value_slider.setTickInterval(10)
        value_slider.setValue(refine_value_for_slider(value))
        DataElements.input_value = None

        def update_slider(val):
            # update_line_edit를 통해 slider 값이 변경되어 update_slider가 호출되는 경우의 if 조건
            if DataElements.input_value is not None:
                input_value = max(0, min(DataElements.input_value, 100))
                value_line_edit.setText(f"{input_value}")
                DataElements.input_value = None
            # 실제 slider 값이 변경되어 update_slider가 호출되는 경우의 if 조건
            else:
                float_value = val / 10
                value_line_edit.setText(f"{float_value}")

        def update_line_edit(text):
            if text:
                DataElements.input_value = float(text)
                slider_value = int(DataElements.input_value * 10)
                slider_value = max(0, min(slider_value, 1000))
                value_slider.setValue(slider_value)

        value_slider.valueChanged.connect(update_slider)

        value_line_edit = QLineEdit(f"{value}")
        validator = QDoubleValidator()
        value_line_edit.setValidator(validator)
        value_line_edit.editingFinished.connect(lambda: update_line_edit(value_line_edit.text()))
        value_line_edit.returnPressed.connect(lambda: update_line_edit(value_line_edit.text()))

        return value_slider, value_line_edit

    if isinstance(value, str) and value.lower() in ['true', 'false']:
        value = str_bool_to_bool(value)
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

    return QLineEdit(str(value))


# 이 메소드로 넘어온 item 속 데이터는 QLineEdit이다.
def update_settings_to_table_with_qtable_item(item, new_value):
    # QLineEdit의 text() 메소드로 데이터를 가져올 수 있다.
    # 가져온 데이터를 기존 설정 항목의 설정 값으로 갱신한다.
    item.setText(str(new_value))


# 이 메소드로 넘어온 widget은 QWidget이다.
def update_settings_to_table_with_qtable_widget(widget, option, new_value):
    children = widget.children()
    """
    숫자(소숫점): [0] QHBoxLayout [1] QSlider [2] QLineEdit
    선택형(라디오 버튼): [0] QHBoxLayout [1] QRadioButton(True) [2] QRadioButton(False)
    """
    if isinstance(children[1], QRadioButton):
        new_value = str_bool_to_bool(new_value)
        value_radio_true = widget.children()[1]
        value_radio_false = widget.children()[2]
        if new_value:
            value_radio_true.setChecked(True)
            value_radio_false.setChecked(False)
        else:
            value_radio_true.setChecked(False)
            value_radio_false.setChecked(True)
    elif isinstance(children[2], QLineEdit):
        value_slider = widget.children()[1]
        value_line_edit = widget.children()[2]
        if new_value:
            value_slider.setValue(refine_value_for_slider(new_value))
            value_line_edit.setText(f"{new_value}.0" if isinstance(new_value, int) else f"{new_value}")
        else:
            value_line_edit.setText(f"{0.0}")
    else:
        if_error_when_update_settings(option, new_value)


def load_settings_from_table():
    # 이 메소드에서는 기존 테이블의 데이터를 가져와서 설정 파일을 갱신한다.
    # 바로 처리하지 않고 임시 변수에 저장한 후, 파일 저장 시에 한꺼번에 처리한다.
    palworld_options_to_save = {}

    for row_index in range(UIElements.settings_table_widget.rowCount()):
        # 기존 설정 항목 가져오기
        option_str = UIElements.settings_table_widget.item(row_index, 0).text()

        # 기존 설정 항목의 설정 값 아이템을 가져온다
        """
        글자형(텍스트 입력) = QTableWidgetItem
        숫자형(슬라이더 + 숫자 입력), 선택형(라디오 버튼) = QWidget
        """
        value_item = UIElements.settings_table_widget.item(row_index, 2)
        if value_item:
            # 글자형
            palworld_options_to_save[option_str] = value_item.text()
        else:
            # 숫자형, 선택형
            value_widget = UIElements.settings_table_widget.cellWidget(row_index, 2)
            children = value_widget.children()
            if isinstance(children[1], QRadioButton):
                # 선택형
                palworld_options_to_save[option_str] = children[1].isChecked()
            elif isinstance(children[2], QLineEdit):
                # 숫자형
                palworld_options_to_save[option_str] = children[2].text()

    return palworld_options_to_save


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


def str_bool_to_bool(str_bool):
    return True if str_bool.lower() == 'true' else False
