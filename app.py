import sys
import os
import subprocess

# Automatically install missing modules
required_modules = ["PyQt6", "PyPDF2"]
for module in required_modules:
    try:
        __import__(module)
    except ModuleNotFoundError:
        print(f"Module '{module}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        os.execv(sys.executable, [sys.executable] + sys.argv)  # Restart script after installation

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, 
    QLineEdit, QCheckBox, QSpacerItem, QSizePolicy, QGroupBox
)
from PyPDF2 import PdfReader, PdfWriter
from PyQt6.QtGui import QIcon

class PDFProtectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("PDF Protector")
        self.setGeometry(100, 100, 480, 480)
        
        layout = QVBoxLayout()

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.label = QLabel("Select a PDF to protect:")
        layout.addWidget(self.label)
        
        self.btn_upload = QPushButton("Upload PDF")
        self.btn_upload.setStyleSheet("font-size: 30px;")
        self.btn_upload.clicked.connect(self.upload_pdf)
        layout.addWidget(self.btn_upload)
        
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Information Box
        info_box = QGroupBox("Password Information")
        info_layout = QVBoxLayout()
        info_label = QLabel("• **User Password**: Required to open the document.\n"
                            "• **Owner Password**: Required to change permissions or remove protection.")
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        info_box.setLayout(info_layout)
        layout.addWidget(info_box)

        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # User password
        self.user_checkbox = QCheckBox("Set User Password")
        self.user_checkbox.stateChanged.connect(self.toggle_user_password)
        layout.addWidget(self.user_checkbox)
        
        self.user_password_label = QLabel("Enter User Password:")
        self.user_password_label.setVisible(False)
        layout.addWidget(self.user_password_label)
        
        self.user_password_input = QLineEdit()
        self.user_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        self.user_password_input.setVisible(False)
        self.user_password_input.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.user_password_input)
        
        # Owner password
        self.owner_checkbox = QCheckBox("Set Owner Password")
        self.owner_checkbox.setChecked(True)
        self.owner_checkbox.stateChanged.connect(self.toggle_owner_password)
        layout.addWidget(self.owner_checkbox)
        
        self.owner_password_label = QLabel("Enter Owner Password:")
        layout.addWidget(self.owner_password_label)
        
        self.owner_password_input = QLineEdit()
        self.owner_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        self.owner_password_input.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.owner_password_input)
        
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.btn_protect = QPushButton("Protect & Save PDF")
        self.btn_protect.setEnabled(False)
        self.btn_protect.setStyleSheet("font-size: 20px;")
        self.btn_protect.clicked.connect(self.protect_pdf)
        layout.addWidget(self.btn_protect)

        # Add copyright label
        self.copyright_label = QLabel("© 2025. All rights reserved.")
        self.copyright_label.setStyleSheet("font-size: 14px; color: gray;")
        layout.addWidget(self.copyright_label)

        
        
        self.setLayout(layout)
    
    def upload_pdf(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)", options=options)
        
        if file_path:
            self.input_path = file_path
            self.label.setText(f"Selected: {os.path.basename(file_path)}")
            self.btn_protect.setEnabled(True)
    
    def toggle_user_password(self):
        visible = self.user_checkbox.isChecked()
        self.user_password_label.setVisible(visible)
        self.user_password_input.setVisible(visible)
    
    def toggle_owner_password(self):
        visible = self.owner_checkbox.isChecked()
        self.owner_password_label.setVisible(visible)
        self.owner_password_input.setVisible(visible)
    
    def protect_pdf(self):
        user_password = self.user_password_input.text() if self.user_checkbox.isChecked() else ""
        owner_password = self.owner_password_input.text() if self.owner_checkbox.isChecked() else ""
        
        if not user_password and not owner_password:
            QMessageBox.warning(self, "Warning", "Please set at least one password.")
            return
        
        input_filename = os.path.basename(self.input_path)
        name, ext = os.path.splitext(input_filename)
        output_filename = f"{name}-protected{ext}"

        output_path, _ = QFileDialog.getSaveFileName(self, "Save Protected PDF", output_filename, "PDF Files (*.pdf)")
        
        if output_path:
            reader = PdfReader(self.input_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(user_password=user_password, owner_password=owner_password, permissions_flag=4)
            
            with open(output_path, "wb") as f:
                writer.write(f)
            
            QMessageBox.information(self, "Success", "PDF has been protected successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))  # Set application icon globally
    window = PDFProtectorApp()
    window.show()
    sys.exit(app.exec())
