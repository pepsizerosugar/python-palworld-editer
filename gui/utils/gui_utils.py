from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QSlider, QLineEdit, QRadioButton, QButtonGroup


def center_on_screen(widget):
    # 현재 스크린의 중앙 좌표를 구함
    screen_rect = QApplication.desktop().screenGeometry()
    x = (screen_rect.width() - widget.width()) // 2
    y = (screen_rect.height() - widget.height()) // 2

    # 위젯을 중앙 좌표로 이동
    widget.move(x, y)


def create_widget_for_option(option, value):
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
                print(f"Option: {option}, Value: True")
            else:
                value_radio_true.setChecked(False)
                print(f"Option: {option}, Value: False")

        value_radio_true.toggled.connect(lambda: update_radio_button())
        value_radio_false.toggled.connect(lambda: update_radio_button())

        return value_radio_true, value_radio_false

    if isinstance(value, (int, float)):
        value_slider = QSlider(Qt.Horizontal)
        value_slider.setRange(0, 100)
        value_slider.setValue(float(value))

        def update_slider(val):
            value_line_edit.setText(f"{val}")
            value_slider.setValue(val)

        def update_line_edit(text):
            if text:
                value_slider.setValue(float(text))

        value_slider.valueChanged.connect(update_slider)

        value_line_edit = QLineEdit(f"{value}")
        validator = QDoubleValidator()
        value_line_edit.setValidator(validator)
        value_line_edit.textChanged.connect(lambda text: update_line_edit(text))

        return value_slider, value_line_edit
    else:
        value_line_edit = QLineEdit(str(value))
        value_line_edit.textChanged.connect(lambda text: print(f"Option: {option}, Value: {text}"))

        return value_line_edit


def resize_windows(self):
    self.total_width = sum(self.table_widget.columnWidth(col) for col in range(self.table_widget.columnCount()))
    self.resize(self.total_width + 65, self.size().height() + 800)
