import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

sys.path.append("C:")
from DataAdmin import *

class Users_Menu(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.main_window = main_window
        self.label_title = QLabel("Choose a User")
        self.label_title.setStyleSheet("font-size: 25px; margin-bottom: 20px; text-align: center;")
        self.label_title.setAlignment(Qt.AlignCenter)

        '''self.label_image = QLabel("h")
        pixmap = QPixmap("assets\\static\\images\\user.png")
        self.label_image.setPixmap(pixmap)
        self.label_image.setAlignment(Qt.AlignCenter)

        ruta_user_image = 'assets\\static\\images\\user.png'
        self.button_user = QPushButton("User1")
        self.button_user.setStyleSheet(f"background-image: url({ruta_user_image});")'''

        h_layout = QHBoxLayout()
        h2_layout = QHBoxLayout()
        h3_layout = QHBoxLayout()

        users_db = query_db("SELECT Username FROM users")
        for user, num_user in zip(users_db, range(len(users_db))) :
            user = user[0]
            button = QPushButton(user)
            button.setStyleSheet("background-color: rgb(66, 36, 171); color: white; font-size: 12px; border-radius: 10px; padding: 12px 30px;")
            button.clicked.connect(lambda checked, user=user: self.get_user_selected(user))
            if num_user > 2:
                if num_user > 5:
                    h3_layout.addWidget(button)
                else:
                    h2_layout.addWidget(button)
            else:
                h_layout.addWidget(button)

        self.button_new_user = QPushButton('New User')
        self.button_new_user.setStyleSheet("background-color: #1594cb; color: white; font-size: 12px; border-radius: 10px; padding: 12px 30px;")

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_title)

        v_layout.addLayout(h_layout)
        v_layout.addLayout(h2_layout)
        v_layout.addLayout(h3_layout)

        v_layout.addWidget(self.button_new_user)

        
        v_layout.setContentsMargins(100, 0, 100, 50)

        # Establecer el diseño principal de la ventana
        self.setLayout(v_layout)
    
    def get_user_selected(self, user):
        """Get the user chosen"""
        self.user_selected = user
        self.main_window.set_user_selected(user)
