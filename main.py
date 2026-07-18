
import os
import sys
import requests

from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

API_URL = "http://127.0.0.1:8000/detect"


class EggInspectionWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), "egg_inspection.ui")
        uic.loadUi(ui_path, self)

        self.image_path = None

        self.progressBar.setValue(0)
        self.detectButton.setEnabled(False)
        self.statusbar.showMessage("Select an image to begin")

        self.browseButton.clicked.connect(self.browse_image)
        self.detectButton.clicked.connect(self.detect_image)

    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Egg Tray Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not file_name:
            return

        self.image_path = file_name
        self.detectButton.setEnabled(True)

        self.show_image(self.originalImage, file_name)

        self.resultImage.clear()
        self.resultImage.setText("Awaiting detection")

        self.card1Value.setText("25")
        self.card2Value.setText("0")
        self.card3Value.setText("0")
        self.card4Value.setText("PENDING")
        self.card4Value.setStyleSheet("color:#2f7df5;font-size:24px;font-weight:bold;")

        self.progressBar.setValue(0)
        self.statusbar.showMessage("Image loaded successfully")

    def detect_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "Please select an image first.")
            return

        self.progressBar.setValue(20)
        self.statusbar.showMessage("Running inspection...")

        try:
            with open(self.image_path, "rb") as f:
                response = requests.post(
                    API_URL,
                    files={"file": f},
                    timeout=60
                )

            self.progressBar.setValue(70)

            if response.status_code != 200:
                try:
                    msg = response.json().get("detail", response.text)
                except Exception:
                    msg = response.text

                QMessageBox.critical(self, "API Error", msg)
                self.progressBar.setValue(0)
                return

            data = response.json()

            self.card1Value.setText(str(data["expected_eggs"]))
            self.card2Value.setText(str(data["detected_eggs"]))
            self.card3Value.setText(str(data["missing_eggs"]))
            self.card4Value.setText(data["status"])

            if data["status"] == "PASS":
                self.card4Value.setStyleSheet(
                    "color:green;font-size:24px;font-weight:bold;"
                )
            else:
                self.card4Value.setStyleSheet(
                    "color:red;font-size:24px;font-weight:bold;"
                )

            image_url = data["result_image"]

            image_response = requests.get(image_url, timeout=30)

            if image_response.status_code == 200:
                temp_path = os.path.join(os.path.dirname(__file__), "result.jpg")
                with open(temp_path, "wb") as out:
                    out.write(image_response.content)
                self.show_image(self.resultImage, temp_path)

            self.progressBar.setValue(100)
            self.statusbar.showMessage("Inspection completed successfully")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.progressBar.setValue(0)
            self.statusbar.showMessage("Inspection failed")

    def show_image(self, label, path):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            return

        pixmap = pixmap.scaled(
            label.width(),
            label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EggInspectionWindow()
    window.show()
    sys.exit(app.exec_())
