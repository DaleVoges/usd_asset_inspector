# inspector/app.py

from PySide6 import QtWidgets
from view.main_window import MainWindow
from controller.inspector_controller import InspectorController

def main():
    app = QtWidgets.QApplication([])

    view = MainWindow()
    controller = InspectorController(view)

    view.show()
    app.exec()

if __name__ == "__main__":
    main()
