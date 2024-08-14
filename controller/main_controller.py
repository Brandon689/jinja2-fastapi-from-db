from PySide6.QtWidgets import QFileDialog

class MainController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.connect_signals()

    def connect_signals(self):
        self.view.browse_button.clicked.connect(self.browse_db)
        self.view.generate_button.clicked.connect(self.generate_code)

    def browse_db(self):
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Open SQLite Database", "", "SQLite Database (*.db *.sqlite)")
        if file_name:
            self.view.set_db_path(file_name)

    def generate_code(self):
        db_path = self.view.get_db_path()
        if not db_path:
            self.view.set_output_text("Please select a database file.")
            return

        try:
            generated_code = self.model.generate_code(db_path)
            self.view.set_output_text(generated_code)
        except Exception as e:
            self.view.set_output_text(f"Error: {str(e)}")
