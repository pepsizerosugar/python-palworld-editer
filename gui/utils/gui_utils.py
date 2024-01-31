from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLineEdit, QRadioButton, QButtonGroup, QTableWidgetItem, QLabel, \
    QWidget, QHBoxLayout, QDesktopWidget

from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.messageboxs.message_boxs import if_error_when_update_settings, if_update_settings_finished


def move_center(window):
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())


def resize_windows():
    total_width = 65
    for column in range(UIElements.editor_table_widget.columnCount()):
        total_width += UIElements.editor_table_widget.columnWidth(column)
    total_height = QDesktopWidget().availableGeometry().height() * 0.8
    UIElements.editor_window.resize(total_width, int(total_height))


def set_editor_table_widget_data():
    if "OptionSettings" in DataElements.palworld_options:
        DataElements.palworld_options.pop("OptionSettings")
    # DataElements.options_translations = convert_translation_list_to_dict(DataElements.options_translations)

    if DataElements.is_first_load:
        set_editor_table_header_with_translation()
        for option, value in DataElements.palworld_options.items():
            create_widget_for_value_widget(option, value)
    else:
        exist_options = {}

        for row in range(UIElements.editor_table_widget.rowCount()):
            exist_options.update({UIElements.editor_table_widget.item(row, 0).text(): row})

        for option in DataElements.palworld_options.keys():
            if option in exist_options:
                update_settings_value(exist_options[option], option, DataElements.palworld_options[option])
            else:
                create_widget_for_value_widget(option, DataElements.palworld_options[option])

        if_update_settings_finished()

    UIElements.editor_table_widget.resizeColumnsToContents()


def set_editor_table_header_with_translation():
    header = DataElements.menu_translations.get(
        "default" if DataElements.translation_code == "en" else DataElements.translation_code)
    UIElements.editor_table_widget.setHorizontalHeaderLabels(
        [header.get("parameter"), header.get("description"), header.get("value")])


def create_widget_for_value_widget(option, value):
    settings_value_widget = create_widget_for_option_value(option, value)
    add_row_to_editor_table(option, settings_value_widget)


def create_widget_for_option_value(option, value):
    option_type = DataElements.palworld_options_type.get(option, None)
    if option_type:
        match option_type:
            case "str":
                if value:
                    return QLineEdit(str(value))
                else:
                    return QLineEdit("None" if value is None else "")
            case "int":
                return QLineEdit(str(value))
            case "float":
                return create_widget_for_float_type(value)
            case "bool":
                return create_widget_for_bool_type(value)
            case _:
                return QLineEdit(str(value))
    else:
        return QLineEdit(str(value))


def create_widget_for_float_type(value):
    value_slider = QSlider(Qt.Horizontal)
    value_slider.setRange(0, 1000)
    value_slider.setTickInterval(10)
    value_slider.setValue(refine_value_for_slider(value))
    DataElements.input_value = None

    def if_is_not_numeric_include_dot(text):
        return text.find(",") == -1 and (text.isdigit() or text.replace(".", "", 1).isdigit())

    def update_slider(val):
        if DataElements.input_value is not None:
            input_value = max(0, min(DataElements.input_value, 100))
            value_line_edit.setText(f"{input_value}")
            DataElements.input_value = None
        else:
            float_value = val / 10
            value_line_edit.setText(f"{float_value}")

    def update_line_edit(text):
        if text and if_is_not_numeric_include_dot(text):
            DataElements.input_value = float(text)
            slider_value = int(DataElements.input_value * 10)
            slider_value = max(0, min(slider_value, 1000))
            value_slider.setValue(slider_value)
        else:
            value_line_edit.setText(f"{0.0}")

    value_slider.valueChanged.connect(update_slider)

    value_line_edit = QLineEdit(f"{value}")
    value_line_edit.editingFinished.connect(lambda: update_line_edit(value_line_edit.text()))
    value_line_edit.returnPressed.connect(lambda: update_line_edit(value_line_edit.text()))

    return value_slider, value_line_edit


def create_widget_for_bool_type(value):
    value = str_bool_to_bool(value)
    value_radio_true = QRadioButton("True")
    value_radio_false = QRadioButton("False")

    radio_button_group = QButtonGroup()
    radio_button_group.addButton(value_radio_true)
    radio_button_group.addButton(value_radio_false)

    value_radio_true.setChecked(value)
    value_radio_false.setChecked(not value)

    def update_radio_button():
        if value_radio_true.isChecked():
            value_radio_false.setChecked(False)
        else:
            value_radio_true.setChecked(False)

    value_radio_true.toggled.connect(lambda: update_radio_button())
    value_radio_false.toggled.connect(lambda: update_radio_button())

    return value_radio_true, value_radio_false


def add_row_to_editor_table(option, widgets):
    row_position = UIElements.editor_table_widget.rowCount()
    UIElements.editor_table_widget.insertRow(row_position)

    item_option = QTableWidgetItem(option)
    item_option.setFlags(Qt.ItemIsEnabled)
    UIElements.editor_table_widget.setItem(row_position, 0, item_option)

    translation_label = QLabel(
        DataElements.options_translations.get(option, {}).get(DataElements.translation_code, option))
    UIElements.editor_table_widget.setCellWidget(row_position, 1, translation_label)

    cell_item = create_table_cell_widget(widgets)

    if isinstance(widgets, tuple):
        UIElements.editor_table_widget.setCellWidget(row_position, 2, cell_item)
    else:
        UIElements.editor_table_widget.setItem(row_position, 2, cell_item)

    UIElements.editor_table_widget.setRowHeight(row_position, 35)


def update_settings_value(row_index, option, value):
    exist_item = UIElements.editor_table_widget.item(row_index, 2)
    if exist_item:
        update_settings_to_table_with_qtable_item(exist_item, value)
    else:
        exist_widget = UIElements.editor_table_widget.cellWidget(row_index, 2)
        update_settings_to_table_with_qtable_widget(exist_widget, option, value)


def update_settings_to_table_with_qtable_item(item, new_value):
    item.setText(str(new_value))


def update_settings_to_table_with_qtable_widget(widget, option, new_value):
    children = widget.children()
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


def create_table_cell_widget(widgets):
    if isinstance(widgets, tuple):
        widget_container = QWidget()
        h_layout = QHBoxLayout(widget_container)

        for widget in widgets:
            h_layout.addWidget(widget)

        return widget_container
    else:
        return QTableWidgetItem(str(widgets.text()))


def load_settings_from_table():
    palworld_options_to_save = {}

    for row_index in range(UIElements.editor_table_widget.rowCount()):
        option_str = UIElements.editor_table_widget.item(row_index, 0).text()
        value_item = UIElements.editor_table_widget.item(row_index, 2)
        if value_item:
            palworld_options_to_save[option_str] = value_item.text()
        else:
            value_widget = UIElements.editor_table_widget.cellWidget(row_index, 2)
            children = value_widget.children()
            if isinstance(children[1], QRadioButton):
                palworld_options_to_save[option_str] = children[1].isChecked() if children[1].isChecked() else False
            elif isinstance(children[2], QLineEdit):
                palworld_options_to_save[option_str] = children[2].text()
    return palworld_options_to_save


def refine_value_for_slider(value):
    DataElements.input_value = float(value)
    slider_value = int(DataElements.input_value * 10)
    slider_value = max(0, min(slider_value, 1000))
    return slider_value


def str_bool_to_bool(str_bool):
    return True if str_bool.lower() == 'true' else False
