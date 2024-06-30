import sys
import threading
import pyautogui
import subprocess
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QLabel, QPushButton, QLineEdit, QComboBox, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QPixmap, QIcon
from PyQt5.QtCore import QSize

from scr.screens.create_user import Create_User_Window
from scr.screens.users_menu import Users_Menu
from scr.screens.log_in_pwd import Log_in_pwd
from scr.screens.settings import Settings
from scr.screens.home import Home

from scr.scripts.control_cursor import init_control_cursor

from DataAdmin import query_db, create_UserDb, checkpwd, getValueDb, update_valueDb

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.user_selected = None
        self.init_ui()

    def init_ui(self):
        screen_size = pyautogui.size()
        #int((screen_size.width)/5.69), int((screen_size.height)/5.9)
        self.setWindowTitle('Absolute Control')
        self.setWindowIcon(QIcon("assets\static\images\icon_app.png"))
        self.setGeometry(500, 200, 500, 500)

        # Establecer el fondo negro usando hoja de estilo
        self.setStyleSheet("background-color: black; color: white;")
        
        # Pantallas
        self.window_Create_User_Window = Create_User_Window(self)
        self.window_Users_Menu = Users_Menu(self)
        
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        
        self.ix_window_Users_Menu = self.stack.addWidget(self.window_Users_Menu)
        self.ix_window_Create_User_Window = self.stack.addWidget(self.window_Create_User_Window)

        self.window_Create_User_Window.button_create_user.clicked.connect(self.create_user)
        self.window_Users_Menu.button_new_user.clicked.connect(lambda: self.stack.setCurrentIndex(self.ix_window_Create_User_Window))

        # Back buttons
        self.window_Create_User_Window.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(self.ix_window_Users_Menu))


    def create_user(self):
        if self.window_Create_User_Window.check_pwd.isChecked():
            username = self.window_Create_User_Window.username_edit.text()
            password = None
        else:
            username = self.window_Create_User_Window.username_edit.text()
            password = self.window_Create_User_Window.password_edit.text()

        create_UserDb(username, password)
        self.stack.setCurrentIndex(self.ix_window_Home)
        self.home()
    
    def log_in(self):
        password_to_check = self.window_Log_in_pwd.password_edit.text()
        if checkpwd(self.user_selected, password_to_check):
            self.user_checked = self.user_selected
            
            self.setStyleSheet("background-color: white; color: black;")
            self.stack.setCurrentIndex(self.ix_window_Home)
            self.home()
        else:
            self.window_Log_in_pwd.label_warning.setText("Incorrect password")

    def set_user_selected(self, user):
        self.user_selected = user

        if query_db('''SELECT Password FROM users WHERE Username = ?''', (user,)) != None:
            self.window_Log_in_pwd = Log_in_pwd(username=self.user_selected)
            self.ix_window_Log_in_pwd = self.stack.addWidget(self.window_Log_in_pwd)
            
            self.window_Home = Home(username=self.user_selected)
            self.ix_window_Home = self.stack.addWidget(self.window_Home)

            self.stack.setCurrentIndex(self.ix_window_Log_in_pwd)
            self.window_Log_in_pwd.button_log_in.clicked.connect(self.log_in)
            self.window_Log_in_pwd.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(self.ix_window_Users_Menu))
        else:
            self.stack.setCurrentIndex(self.ix_window_Home)
            self.home()
    
    def home(self):
        # Get the value of dark mode in user's db
        if getValueDb(f"settings_{self.user_selected}", "Service", "dark_mode", "State") == True:
            self.dark_mode_state = True
            self.setStyleSheet("background-color: black; color: white;")
            self.window_Home.dark_mode_button.setIcon(QIcon("assets\static\images\light.png"))
            self.window_Home.dark_mode_button.setIconSize(QSize(24, 24))
        elif getValueDb(f"settings_{self.user_selected}", "Service", "dark_mode", "State") == False:
            self.dark_mode_state = False
            self.setStyleSheet("background-color: white; color: black;")
            self.window_Home.dark_mode_button.setIcon(QIcon("assets\static\images\dark.png"))
            self.window_Home.dark_mode_button.setIconSize(QSize(24, 24))

        # Nav bar buttons
        self.window_Home.dark_mode_button.clicked.connect(self.dark_mode)
        self.window_Home.home_button.clicked.connect(lambda: self.stack.setCurrentIndex(self.ix_window_Home))
        self.window_Home.settings_button.clicked.connect(lambda: self.stack.setCurrentIndex(self.ix_window_Home))###
        self.window_Home.help_button.clicked.connect(lambda: self.stack.setCurrentIndex(self.ix_window_Home))####
        self.window_Home.logout_button.clicked.connect(self.log_out)

    def dark_mode(self):
        if self.dark_mode_state == True:
            self.dark_mode_state = False

            self.setStyleSheet("background-color: white; color: black;")
            self.window_Home.dark_mode_button.setIcon(QIcon("assets\static\images\dark.png"))
            self.window_Home.dark_mode_button.setIconSize(QSize(24, 24))
        elif self.dark_mode_state == False:
            self.dark_mode_state = True

            self.setStyleSheet("background-color: black; color: white;")
            self.window_Home.dark_mode_button.setIcon(QIcon("assets\static\images\light.png"))
            self.window_Home.dark_mode_button.setIconSize(QSize(24, 24))
    
    def settings(self):
        self.window_Settings = Settings()
        self.ix_window_Settings = self.stack.addWidget(self.window_Settings)

        self.window_Settings.save_button.clicked.connect(self.save_settings)

    def save_settings(self):
        update_valueDb(f"settings_{self.user_selected}", "Service", "voice", self.voice_checkbox.isChecked())
        update_valueDb(f"settings_{self.user_selected}", "Service", "sound", self.window_Settings.sound_checkbox.isChecked())
        update_valueDb(f"settings_{self.user_selected}", "Service", "volumen_user", self.window_Settings.volumen_user_spinbox.value())
        update_valueDb(f"settings_{self.user_selected}", "Service", "writing_speed", self.window_Settings.writing_speed_spinbox.value())
        update_valueDb(f"settings_{self.user_selected}", "Service", "speech_recognation", self.window_Settings.speech_recognition_lang_combo.currentText())
        update_valueDb(f"settings_{self.user_selected}", "Service", "", self.window_Settings.currentText())
        update_valueDb(f"settings_{self.user_selected}", "Service", "shutdown_time", self.window_Settings.shutdown_time_edit.text())
        update_valueDb(f"settings_{self.user_selected}", "Service", "scroll_up", self.window_Settings.scroll_up_spinbox.value())
        update_valueDb(f"settings_{self.user_selected}", "Service", "scroll_down", self.window_Settings.scroll_down_spinbox.value())
        update_valueDb(f"settings_{self.user_selected}", "Service", "text_to_speach_assistant_model", self.window_Settings.text_to_speech_assistant_model_edit.text())
        update_valueDb(f"settings_{self.user_selected}", "Service", "dark_mode", self.window_Settings.dark_mode_checkbox.isChecked())


    def log_out(self):
        self.stack.setCurrentIndex(self.ix_window_Users_Menu)
        self.user_selected = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
