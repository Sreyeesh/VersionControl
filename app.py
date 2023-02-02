import os
import sys
import dropbox
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog


class VersionTrackingApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_project = None

        self.setWindowTitle("Version Tracking App")

        self.select_project_button = QtWidgets.QPushButton("Select Project")
        self.select_project_button.clicked.connect(self.select_project)

        self.publish_file_button = QtWidgets.QPushButton("Publish")
        self.publish_file_button.clicked.connect(self.publish_file)
        self.publish_file_button.setEnabled(False)

        self.approve_file_button = QtWidgets.QPushButton("Approve")
        self.approve_file_button.clicked.connect(self.approve_file) #try lambda function with this 
        self.approve_file_button.setEnabled(False)

        self.set_latest_file_button = QtWidgets.QPushButton("Current")
        self.set_latest_file_button.clicked.connect(self.set_latest_file)
        self.set_latest_file_button.setEnabled(False)

        self.files_display = QtWidgets.QPlainTextEdit()
        self.files_display.setReadOnly(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.select_project_button)
        self.layout.addWidget(self.publish_file_button)
        self.layout.addWidget(self.approve_file_button)
        self.layout.addWidget(self.set_latest_file_button)
        self.layout.addWidget(self.files_display)

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def select_project(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.current_project = QFileDialog.getExistingDirectory(self, "Select Project", options=options)
        if self.current_project:
            self.publish_file_button.setEnabled(True)
            self.approve_file_button.setEnabled(True)
            self.set_latest_file_button.setEnabled(True)
            self.files_display.setPlainText("\n".join(os.listdir(self.current_project)))

    def publish_file(self):
        selected_file = self.files_display.textCursor().selectedText()
        if selected_file:
            os.rename(os.path.join(self.current_project, selected_file),
                      os.path.join(self.current_project, "published", selected_file))
            self.files_display.setPlainText("\n".join(os.listdir(self.current_project)))

    #TODO: This is same peace of code as publish file this needs to be different
    def approve_file(self):
        selected_file = self.files_display.textCursor().selectedText()
        if selected_file:
            os.rename(os.path.join(self.current_project, selected_file),
                      os.path.join(self.current_project, "approved", selected_file))
            self.files_display.setPlainText("\n".join(os.listdir(self.current_project)))

    def set_latest_file(self):
        selected_file = self.files_display.textCursor().selectedText().strip()
        if selected_file:
            if '\n' in selected_file:
                self.files_display.setPlainText("Error: invalid file name")
                return
            os.rename(os.path.join(self.current_project, selected_file),
                      os.path.join(self.current_project, "latest", selected_file))
            self.files_display.setPlainText("\n".join(os.listdir(self.current_project)))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VersionTrackingApp()
    window.show()
    sys.exit(app.exec())
