import sys
from PySide6 import QtWidgets
from view.main_window import MainWindow
from controller.controller import Controller

# ---- Main entry point ----

def main(argv):
    app = QtWidgets.QApplication(argv)
    # Create the view and pass it to the controller
    controller = Controller()
    main_window = MainWindow(controller=controller)  # We pass None temporarily

    main_window.show()

    # # Try to open a file passed in argv
    # if len(argv) > 1:
    #     path = argv[1]
    #     if os.path.exists(path):
    #         controller.load_stage(path)
    #     else:
    #         QtWidgets.QMessageBox.warning(main_window, 'File not found', f"Path '{path}' not found — starting with mock stage.")
    #         controller.load_stage(None)
    # else:
    #     # No path provided — open in-memory stage
    #     controller.load_stage(None)

    sys.exit(app.exec())


if __name__ == '__main__':
    main(sys.argv)