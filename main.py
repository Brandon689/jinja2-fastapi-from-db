import sys
from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.main_controller import MainController
from model.code_generator import CodeGenerator

def main():
    app = QApplication(sys.argv)
    
    code_generator = CodeGenerator()
    main_window = MainWindow()
    controller = MainController(main_window, code_generator)
    
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
