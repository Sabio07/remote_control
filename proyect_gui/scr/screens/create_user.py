import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QPixmap

from DataAdmin import create_UserDb

class Create_User_Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.back_button = QPushButton("<")
        self.back_button.setFixedSize(20, 20)
        self.back_button.setStyleSheet("background-color: red;")

        self.label_title = QLabel("Create new user")
        self.label_title.setStyleSheet("font-size: 25px; margin-bottom: 30px; text-align: center;")
        self.label_title.setAlignment(Qt.AlignCenter)

        self.label_image = QLabel("h")
        pixmap = QPixmap("assets\\static\\images\\user.png")
        self.label_image.setPixmap(pixmap)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.label_username = QLabel("Username:")
        self.username_edit = QLineEdit()
        self.label_password = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.check_pwd = QCheckBox("I won't use password")
        self.check_pwd.stateChanged.connect(self.checkbox_changed)

        self.button_create_user = QPushButton('Crear')
        self.button_create_user.setStyleSheet("background-color: #1594cb; color: white; font-size: 12px; border-radius: 10px; padding: 12px 30px; margin: 20px 200px;")

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.back_button)
        h_layout.setAlignment(Qt.AlignLeft)

        h2_layout = QHBoxLayout()
        h2_layout.addWidget(self.check_pwd)

        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(h_layout)
        self.v_layout.addWidget(self.label_title)
        self.v_layout.addWidget(self.label_image)
        self.v_layout.addWidget(self.label_username)
        self.v_layout.addWidget(self.username_edit)
        self.v_layout.addWidget(self.label_password)
        self.v_layout.addWidget(self.password_edit)
        self.v_layout.addWidget(self.check_pwd)
        self.v_layout.addWidget(self.button_create_user)

        # Establecer el diseño principal de la ventana
        self.setLayout(self.v_layout)
    
    def checkbox_changed(self, state):
        if state == 2:  # 2 means Qt.Checked 
            self.label_password.hide()
            self.password_edit.hide()
        else:
            self.label_password.show()
            self.password_edit.show()
