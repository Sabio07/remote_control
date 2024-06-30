import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class Home(QWidget):
    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.setGeometry(100, 100, 800, 600)

        # Crear el layout principal
        self.main_layout = QVBoxLayout()
        
        # Crear la barra de navegación
        self.nav_bar = self.create_nav_bar()
        self.main_layout.addWidget(self.nav_bar)
        
        # Crear el cuerpo principal
        self.body = self.create_body()
        self.main_layout.addLayout(self.body)

        # Crear el pie de página
        self.footer = self.create_footer()
        self.main_layout.addWidget(self.footer)

        # Establecer el layout principal
        self.setLayout(self.main_layout)
        
    def create_nav_bar(self):
        self.nav_bar = QFrame()
        self.nav_bar_layout = QHBoxLayout()

        self.dark_mode_button = QPushButton('')
        self.home_button = QPushButton("Home")
        self.settings_button = QPushButton("Settings")
        self.help_button = QPushButton("Help")
        self.logout_button = QPushButton("Log out")

        # Agregar icono al botón de inicio
        self.dark_mode_button.setIcon(QIcon("assets/static/images/dark.png"))
        self.dark_mode_button.setIconSize(QSize(24, 24))

        buttons = [self.dark_mode_button, self.home_button, self.settings_button, self.help_button, self.logout_button]

        for button in buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.nav_bar_layout.addWidget(button)

        self.nav_bar.setLayout(self.nav_bar_layout)
        self.nav_bar.setFrameShape(QFrame.Box)
        self.nav_bar.setFixedHeight(50)

        return self.nav_bar

    def create_body(self):
        self.body_layout = QVBoxLayout()

        self.welcome_label = QLabel(f"Welcome, {self.username}")
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.body_layout.addWidget(self.welcome_label)

        # Panel de funcionalidades principales
        self.functionalities_layout = QHBoxLayout()
        
        self.assitant_button = self.create_icon_button("Start Assistant", "assets\\static\\images\\microfone.png")
        self.mouse_button = self.create_icon_button("Start Remote Mouse", "assets\\static\\images\\camera.png")
        self.all_button = self.create_icon_button("Start all", "assets\\static\\images\\arrow.png")
        
        self.functionalities_layout.addWidget(self.assitant_button)
        self.functionalities_layout.addWidget(self.mouse_button)
        self.functionalities_layout.addWidget(self.all_button)

        self.functionalities_layout.setContentsMargins(300, 0, 300, 0)
        
        self.body_layout.addLayout(self.functionalities_layout)

        # Panel de actividades recientes
        self.recent_activities = QLabel("Recent Activities")
        self.recent_activities.setStyleSheet("font-size: 18px; margin-top: 20px;")
        self.body_layout.addWidget(self.recent_activities)

        # Panel informativo
        self.info_panel = QLabel("Panel Informativo")
        self.info_panel.setStyleSheet("font-size: 18px; margin-top: 20px;")
        self.body_layout.addWidget(self.info_panel)

        return self.body_layout

    def create_footer(self):
        self.footer = QFrame()
        self.footer_layout = QHBoxLayout()

        self.contact_info = QLabel("Contacto: soporte@empresa.com")
        self.terms_link = QLabel('<a href="#">Términos de Servicio</a>')
        self.privacy_link = QLabel('<a href="#">Política de Privacidad</a>')

        self.footer_layout.addWidget(self.contact_info)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.terms_link)
        self.footer_layout.addWidget(self.privacy_link)

        self.footer.setLayout(self.footer_layout)
        self.footer.setFrameShape(QFrame.Box)

        return self.footer

    def create_icon_button(self, text, icon_path):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(40, 40))  # Uso de QSize para establecer el tamaño del icono
        button.setStyleSheet("padding: 10px; font-size: 16px;")
        return button

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Home("Usuario")
    window.show()
    sys.exit(app.exec_())
