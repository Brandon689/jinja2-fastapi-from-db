import os
from PySide6.QtWidgets import QFileDialog, QMessageBox

class MainController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.generated_files = {}
        self.db_name = ""
        self.connect_signals()

    def connect_signals(self):
        self.view.browse_button.clicked.connect(self.browse_db)
        self.view.generate_button.clicked.connect(self.generate_code)
        self.view.save_button.clicked.connect(self.save_generated_code)

    def browse_db(self):
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Open SQLite Database", "", "SQLite Database (*.db *.sqlite)")
        if file_name:
            self.view.set_db_path(file_name)
            self.db_name = os.path.splitext(os.path.basename(file_name))[0]

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

        if not self.db_name:
            QMessageBox.warning(self.view, "No Database Selected", "Please select a database before saving.")
            return

        # Create the parent folder in the current working directory
        parent_folder = "GeneratedCode"
        parent_path = os.path.join(os.getcwd(), parent_folder)
        os.makedirs(parent_path, exist_ok=True)

        # Create the database-specific subfolder
        db_specific_dir = os.path.join(parent_path, self.db_name)
        os.makedirs(db_specific_dir, exist_ok=True)

        # Open save dialog with the path set to the database-specific folder
        save_path = QFileDialog.getExistingDirectory(self.view, "Select Directory to Save Generated Code", db_specific_dir)

        if save_path:
            # Ensure we're using the db-specific directory if the user didn't change it
            if save_path == parent_path:
                save_path = db_specific_dir

            try:
                for filename, content in self.generated_files.items():
                    file_path = os.path.join(save_path, filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'w') as f:
                        f.write(content)
                QMessageBox.information(self.view, "Save Successful", f"Generated code has been saved successfully in:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self.view, "Save Error", f"An error occurred while saving: {str(e)}")