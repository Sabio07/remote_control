from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QPixmap


class Log_in_pwd(QWidget):
    def __init__(self, username, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.back_button = QPushButton("<")
        self.back_button.setFixedSize(20, 20)
        self.back_button.setStyleSheet("background-color: red;")

        self.label_title = QLabel(f"Iniciar sesión  -  {username}")
        self.label_title.setStyleSheet("font-size: 25px; margin-bottom: 30px; text-align: center;")
        self.label_title.setAlignment(Qt.AlignCenter)

        self.label_image = QLabel("h")
        pixmap = QPixmap("assets\\static\\images\\user.png")
        self.label_image.setPixmap(pixmap)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.label_password = QLabel("Password:")
        self.label_password.setContentsMargins(300, 0, 300, 0)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setContentsMargins(300, 0, 300, 0)

        self.label_warning = QLabel("")
        self.label_warning.setAlignment(Qt.AlignCenter)
        self.label_warning.setStyleSheet("color: red;")

        self.button_log_in = QPushButton('Log in')
        self.button_log_in.setStyleSheet("background-color: #1594cb; color: white; font-size: 12px; border-radius: 10px; padding: 12px 30px; margin: 20px 200px;")

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.back_button)
        h_layout.setAlignment(Qt.AlignLeft)

        v_layout = QVBoxLayout()

        v_layout.addLayout(h_layout)

        v_layout.addWidget(self.label_title)
        v_layout.addWidget(self.label_image)
        v_layout.addWidget(self.label_password)
        v_layout.addWidget(self.password_edit)
        v_layout.addWidget(self.label_warning)
        v_layout.addWidget(self.button_log_in)

        # Establecer el diseño principal de la ventana
        self.setLayout(v_layout)