import sys
from PyQt5.QtWidgets import QApplication
from gui.widgets.palworld_settings_widget import PalWorldSettingsWidget
from qtmodern.styles import dark

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = PalWorldSettingsWidget()

    dark(app)

    gui.show()
    sys.exit(app.exec_())
