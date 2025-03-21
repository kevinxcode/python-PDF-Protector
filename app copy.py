import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit, QSpacerItem, QSizePolicy
from PyPDF2 import PdfReader, PdfWriter

class PDFProtectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("PDF Protector")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Select a PDF to protect:")
        layout.addWidget(self.label)
        
        self.btn_upload = QPushButton("Upload PDF")
        self.btn_upload.clicked.connect(self.upload_pdf)
        layout.addWidget(self.btn_upload)
        
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.password_label = QLabel("Enter Owner Password:")
        layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)  # Show text instead of hiding
        layout.addWidget(self.password_input)
        
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.btn_protect = QPushButton("Protect & Save PDF")
        self.btn_protect.setEnabled(False)
        self.btn_protect.clicked.connect(self.protect_pdf)
        layout.addWidget(self.btn_protect)
        
        self.setLayout(layout)
    
    def upload_pdf(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)", options=options)
        
        if file_path:
            self.input_path = file_path
            self.label.setText(f"Selected: {os.path.basename(file_path)}")
            self.btn_protect.setEnabled(True)
    
    def protect_pdf(self):
        owner_password = self.password_input.text()
        if not owner_password:
            QMessageBox.warning(self, "Warning", "Please enter an owner password.")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Protected PDF", "protected.pdf", "PDF Files (*.pdf)")
        
        if output_path:
            reader = PdfReader(self.input_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(
                user_password="",
                owner_password=owner_password,
                permissions_flag=4
            )
            
            with open(output_path, "wb") as f:
                writer.write(f)
            
            QMessageBox.information(self, "Success", "PDF has been protected successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFProtectorApp()
    window.show()
    sys.exit(app.exec())
