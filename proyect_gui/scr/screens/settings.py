import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

sys.path.append("C:")
from DataAdmin import *

class Settings(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)        
        layout = QVBoxLayout()

        SETTINGS = "settings.json"
        with open(SETTINGS, 'r') as file_json:
            data = json.load(file_json)

        self.settings = []

        for key, value in data.items():
            self.settings.append((key, value))

        # Voice
        self.voice_checkbox = QCheckBox('Voice')
        self.voice_checkbox.setChecked(self.settings[0][1])
        layout.addWidget(self.voice_checkbox)
        
        # Sound
        self.sound_checkbox = QCheckBox('Sound')
        self.sound_checkbox.setChecked(self.settings[1][1])
        layout.addWidget(self.sound_checkbox)
        
        # Volumen User
        self.volumen_user_spinbox = QDoubleSpinBox()
        self.volumen_user_spinbox.setValue(self.settings[2][1])
        self.volumen_user_spinbox.setRange(0.0, 10.0)
        self.volumen_user_spinbox.setSingleStep(0.1)
        layout.addWidget(QLabel('Volumen User'))
        layout.addWidget(self.volumen_user_spinbox)
        
        # Writing Speed
        self.writing_speed_spinbox = QDoubleSpinBox()
        self.writing_speed_spinbox.setValue(self.settings[3][1])
        self.writing_speed_spinbox.setRange(0.0, 1.0)
        self.writing_speed_spinbox.setSingleStep(0.01)
        layout.addWidget(QLabel('Writing Speed'))
        layout.addWidget(self.writing_speed_spinbox)
        
        # Speech Recognition Language
        self.speech_recognition_lang_combo = QComboBox()
        self.speech_recognition_lang_combo.addItem("es-ES")
        self.speech_recognition_lang_combo.addItem("en-US")
        self.speech_recognition_lang_combo.setCurrentText(self.settings[4][1])
        layout.addWidget(QLabel('Speech Recognition Language'))
        layout.addWidget(self.speech_recognition_lang_combo)
        
        # Voice Models
        self.voice_models = QComboBox()
        for item in self.settings[5][1]:
            self.voice_models.addItem(item)
        self.voice_models.setCurrentText(self.settings[5][1])
        layout.addWidget(QLabel('Select the voice model in your computer'))
        layout.addWidget(self.voice_models)
        
        # Shutdown Time
        self.shutdown_time_edit = QLineEdit(self.settings[6][1])
        layout.addWidget(QLabel('Shutdown Time'))
        layout.addWidget(self.shutdown_time_edit)
        
        # Scroll Up
        self.scroll_up_spinbox = QSpinBox()
        self.scroll_up_spinbox.setValue(self.settings[7][1])
        self.scroll_up_spinbox.setRange(-1000, 1000)
        layout.addWidget(QLabel('Scroll Up'))
        layout.addWidget(self.scroll_up_spinbox)
        
        # Scroll Down
        self.scroll_down_spinbox = QSpinBox()
        self.scroll_down_spinbox.setValue(self.settings[8][1])
        self.scroll_down_spinbox.setRange(-1000, 1000)
        layout.addWidget(QLabel('Scroll Down'))
        layout.addWidget(self.scroll_down_spinbox)
        
        # Text to Speech Assistant Model
        self.text_to_speech_assistant_model_edit = QLineEdit()
        if self.settings[8][1]:
            self.text_to_speech_assistant_model_edit.setText(self.settings[9][1])
        layout.addWidget(QLabel('Text to Speech Assistant Model'))
        layout.addWidget(self.text_to_speech_assistant_model_edit)
        
        # Dark Mode
        self.dark_mode_checkbox = QCheckBox('Dark Mode')
        self.dark_mode_checkbox.setChecked(self.settings[10][1])
        layout.addWidget(self.dark_mode_checkbox)
        
        # Save button
        self.save_button = QPushButton('Save')
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Settings()
    window.show()
    sys.exit(app.exec_())
