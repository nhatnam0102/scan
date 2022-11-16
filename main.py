import sys

from PyQt5.QtWidgets import QApplication
from upc.widgets.main_widget import Main
from upc.common import style_sheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet.MainWindowStyle())
    window = Main()
    window.showMaximized()

    sys.exit(app.exec())
