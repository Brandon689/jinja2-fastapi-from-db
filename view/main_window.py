from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("FastAPI SQLite Code Generator")
        self.resize(800, 600)

        main_layout = QVBoxLayout(self)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("Database File:"))
        self.db_input = QLineEdit()
        db_layout.addWidget(self.db_input)
        self.browse_button = QPushButton("Browse")
        db_layout.addWidget(self.browse_button)
        scroll_layout.addLayout(db_layout)

        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate")
        button_layout.addWidget(self.generate_button)
        self.save_button = QPushButton("Save")
        button_layout.addWidget(self.save_button)
        scroll_layout.addLayout(button_layout)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        scroll_layout.addWidget(self.output_text)

        scroll_area.setWidget(scroll_content)

    def set_db_path(self, path):
        self.db_input.setText(path)

    def get_db_path(self):
        return self.db_input.text()

    def set_output_text(self, text):
        self.output_text.setPlainText(text)

    def get_output_text(self):
        return self.output_text.toPlainText()