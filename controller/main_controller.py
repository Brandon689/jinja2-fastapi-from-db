import os
from PySide6.QtWidgets import QFileDialog, QMessageBox

class MainController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.generated_files = {}
        self.connect_signals()

    def connect_signals(self):
        self.view.browse_button.clicked.connect(self.browse_db)
        self.view.generate_button.clicked.connect(self.generate_code)
        self.view.save_button.clicked.connect(self.save_generated_code)

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
            self.generated_files = self.model.generate_code(db_path)
            self.display_generated_files()
        except Exception as e:
            self.view.set_output_text(f"Error: {str(e)}")

    def display_generated_files(self):
        output = "Generated files:\n\n"
        for filename, content in self.generated_files.items():
            output += f"--- {filename} ---\n{content}\n\n"
        self.view.set_output_text(output)

    def save_generated_code(self):
        if not self.generated_files:
            QMessageBox.warning(self.view, "No Generated Code", "Please generate code before saving.")
            return

        save_dir = QFileDialog.getExistingDirectory(self.view, "Select Directory to Save Generated Code")
        if save_dir:
            try:
                for filename, content in self.generated_files.items():
                    file_path = os.path.join(save_dir, filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'w') as f:
                        f.write(content)
                QMessageBox.information(self.view, "Save Successful", "Generated code has been saved successfully.")
            except Exception as e:
                QMessageBox.critical(self.view, "Save Error", f"An error occurred while saving: {str(e)}")