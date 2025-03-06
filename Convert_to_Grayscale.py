from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PIL import Image
import sys
import io

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(714, 477)
        
        # Layout vertikal
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        # Label judul
        self.label_2 = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        # Tombol load gambar
        self.btn_load = QtWidgets.QPushButton(parent=Form)
        self.btn_load.setObjectName("btn_load")
        self.verticalLayout.addWidget(self.btn_load)

        # Tombol konversi ke grayscale
        self.btn_grayscale = QtWidgets.QPushButton(parent=Form)
        self.btn_grayscale.setObjectName("btn_grayscale")
        self.verticalLayout.addWidget(self.btn_grayscale)

        # Tombol simpan gambar
        self.btn_save = QtWidgets.QPushButton(parent=Form)
        self.btn_save.setObjectName("btn_save")
        self.verticalLayout.addWidget(self.btn_save)

        # QLabel untuk menampilkan gambar
        self.image_label = QtWidgets.QLabel(parent=Form)
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)

        # Progress Bar
        self.progressBar = QtWidgets.QProgressBar(parent=Form)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        # Connect buttons to functions
        self.btn_load.clicked.connect(self.load_image)
        self.btn_grayscale.clicked.connect(self.convert_to_grayscale)
        self.btn_save.clicked.connect(self.save_image)

        # Filepath untuk menyimpan gambar yang dimuat
        self.image_path = ""
        self.grayscale_image = None

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Grayscale Converter"))
        self.label_2.setText(_translate("Form", "Grayscale Converter"))
        self.btn_load.setText(_translate("Form", "Load Image"))
        self.btn_grayscale.setText(_translate("Form", "Convert to Grayscale"))
        self.btn_save.setText(_translate("Form", "Save Image"))

    def load_image(self):
        """Load image from file and display it in QLabel."""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)

        # Menunggu sampai pengguna memilih file
        if file_dialog.exec():
            self.image_path = file_dialog.selectedFiles()[0]
            self.display_image(self.image_path)
    
    def display_image(self, image_path):
        """Display the selected image in QLabel."""
        pixmap = QtGui.QPixmap(image_path)
        if pixmap.isNull():
            QMessageBox.warning(None, "Image Load Error", "Failed to load image.")
            return
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)

    def convert_to_grayscale(self):
        """Convert the loaded image to grayscale."""
        if not self.image_path:
            QMessageBox.warning(None, "No Image", "Please load an image first.")
            return

        # Load image using Pillow
        image = Image.open(self.image_path)
        self.grayscale_image = image.convert('L')  # Convert to grayscale

        # Update progress bar
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)
        
        # Display the grayscale image
        grayscale_path = self.image_path.replace(".", "_grayscale.")
        self.display_image_from_pil(self.grayscale_image)

    def display_image_from_pil(self, pil_image):
        """Display a PIL image in QLabel."""
        image_bytes = io.BytesIO()
        pil_image.save(image_bytes, format="PNG")
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image_bytes.getvalue())
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)

    def save_image(self):
        """Save the grayscale image."""
        if self.grayscale_image is None:
            QMessageBox.warning(None, "No Grayscale Image", "Please convert the image to grayscale first.")
            return
        
        # Open file dialog for saving image
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        
        if file_dialog.exec():
            save_path = file_dialog.selectedFiles()[0]
            # Ensure that the file has a valid extension if none provided
            if not save_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                save_path += '.png'
            # Save grayscale image to the chosen file path
            self.grayscale_image.save(save_path)
            QMessageBox.information(None, "Image Saved", f"Image saved as {save_path}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())