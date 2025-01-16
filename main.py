 
import sys
import json
import keyboard
import pyperclip
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QScrollArea, QLabel, QComboBox, QLineEdit, QMessageBox, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "language": "farsi",
    "key_mappings": {
        "farsi": {
            'ض': 'q', 'ص': 'w', 'ث': 'e', 'ق': 'r', 'ف': 't',
            'ج': '[', 'چ': ']', 'گ': "'", '؟': '?', 'ژ': 'c',
            'غ': 'y', 'ع': 'u', 'ه': 'i', 'خ': 'o', 'ح': 'p',
            'ش': 'a', 'س': 's', 'ی': 'd', 'ب': 'f', 'ل': 'g',
            'ا': 'h', 'ت': 'j', 'ن': 'k', 'م': 'l', 'ک': ';',
            'ظ': 'z', 'ط': 'x', 'ز': 'c', 'ر': 'v', 'ذ': 'b',
            'د': 'n', 'پ': '\\', 'و': ',', '.': '.', '/': '/',
            ' ': ' ', "ئ": "m"
        },
        "english": {
            'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف',
            'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
            'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل',
            'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م', ';': 'ک',
            'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ',
            'n': 'د', 'm': 'م', ',': 'و', '.': '.', '/': '/',
            ' ': ' ', "'": 'گ', '[': 'ج', ']': 'چ', '\\': 'پ',
            '?': '؟'
        }
    }
}

def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return DEFAULT_SETTINGS

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.tray_icon = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("برنامه تبدیل متن")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon('./image/logo.png'))  # اضافه کردن آیکون به پنجره

        font = QFont()
        font.setBold(True)

        self.start_button = QPushButton("اغاز برنامه", self)
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.start_button.clicked.connect(self.start_program)

        self.change_keys_button = QPushButton("تغییر کلید", self)
        self.change_keys_button.setFont(font)
        self.change_keys_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.change_keys_button.clicked.connect(self.show_change_keys)

        self.help_button = QPushButton("راهنما", self)
        self.help_button.setFont(font)
        self.help_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.help_button.clicked.connect(self.show_help)

        self.about_button = QPushButton("درباره سازنده", self)
        self.about_button.setFont(font)
        self.about_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.about_button.clicked.connect(self.show_about)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.change_keys_button)
        layout.addWidget(self.help_button)
        layout.addWidget(self.about_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_program(self):
        self.hide()
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./image/logo.png"))  

        tray_menu = QMenu()
        show_action = QAction("نمایش برنامه", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        exit_action = QAction("خروج", self)
        exit_action.triggered.connect(self.close_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.tray_icon.showMessage("برنامه تبدیل متن", "برنامه فعال شد و در System Tray قرار گرفت.", QSystemTrayIcon.Information, 2000)

        keyboard.add_hotkey('ctrl+alt+p', self.on_hotkey_english_to_farsi)
        keyboard.add_hotkey('ctrl+alt+e', self.on_hotkey_farsi_to_english)

    def close_app(self):
        self.tray_icon.hide()
        keyboard.unhook_all()
        QApplication.quit()

    def on_hotkey_english_to_farsi(self):
        try:
            time.sleep(0.1)
            original_text = pyperclip.paste()
            if not original_text.strip():
                print("Clipboard is empty or contains only whitespace.")
                return
            
            if not any(char in self.settings["key_mappings"]["english"] for char in original_text):
                print("No English characters found in clipboard.")
                return

            translated_text = self.translate_english_to_farsi(original_text)
            pyperclip.copy(translated_text)

            print(f"Original: {original_text} -> Translated (English to Farsi): {translated_text}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def on_hotkey_farsi_to_english(self):
        try:
            time.sleep(0.1)
            original_text = pyperclip.paste()
            if not original_text.strip():
                print("Clipboard is empty or contains only whitespace.")
                return
            
            if not any(char in self.settings["key_mappings"]["farsi"] for char in original_text):
                print("No Persian characters found in clipboard.")
                return

            translated_text = self.translate_farsi_to_english(original_text)
            pyperclip.copy(translated_text)

            print(f"Original: {original_text} -> Translated (Farsi to English): {translated_text}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def translate_english_to_farsi(self, text):
        return ''.join([self.settings["key_mappings"]["english"].get(char, char) for char in text])

    def translate_farsi_to_english(self, text):
        return ''.join([self.settings["key_mappings"]["farsi"].get(char, char) for char in text])

    def show_change_keys(self):
        self.change_keys_window = ChangeKeysWindow(self.settings, self)
        self.change_keys_window.show()

    def show_help(self):
        help_text = """
        ابتدا متن مورد نظر را با دکمه Ctrl + X کات کنید
        سپس برای تغییر متن از فارسی به اینگلیسی از شورتکات Ctrl + Alt + P
        و برای بلعکس از کلید Ctrl + Alt + E استفاده کنید.
        """
        QMessageBox.information(self, "راهنما", help_text)

    def show_about(self):
        about_text = """
        سازنده: مهرداد حسن زاده

        اینستاگرام: <a href='https://www.instagram.com/1mehrdad0'>Instagram</a>
        تلگرام: <a href='https://t.me/hitwithit'>Telegram</a>
        سایت: <a href='https://www.medofile.ir'>Website</a>
        گیت‌هاب: <a href='https://github.com/mtgama'>GitHub</a>
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("درباره سازنده")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(about_text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

class ChangeKeysWindow(QMainWindow):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("تغییر کلیدها")
        self.setGeometry(150, 150, 400, 300)

        self.language_combo = QComboBox(self)
        self.language_combo.addItem("فارسی")
        self.language_combo.addItem("انگلیسی")
        self.language_combo.setCurrentText("فارسی" if self.settings["language"] == "farsi" else "انگلیسی")
        self.language_combo.currentTextChanged.connect(self.update_key_mappings)

        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()

        self.key_inputs = {}
        self.update_key_mappings()

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.save_button = QPushButton("ذخیره تغییرات", self)
        self.save_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.save_button.clicked.connect(self.save_changes)

        layout = QVBoxLayout()
        layout.addWidget(self.language_combo)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_key_mappings(self):
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        language = "farsi" if self.language_combo.currentText() == "فارسی" else "english"
        key_mappings = self.settings["key_mappings"][language]

        self.key_inputs = {}
        for key, value in key_mappings.items():
            label = QLabel(f"{key} -> {value}", self)
            input_field = QLineEdit(self)
            input_field.setPlaceholderText("مقدار جدید")
            self.scroll_layout.addWidget(label)
            self.scroll_layout.addWidget(input_field)
            self.key_inputs[key] = input_field

    def save_changes(self):
        language = "farsi" if self.language_combo.currentText() == "فارسی" else "english"
        key_mappings = self.settings["key_mappings"][language]

        for key, input_field in self.key_inputs.items():
            new_value = input_field.text()
            if new_value:
                key_mappings[key] = new_value

        save_settings(self.settings)
        QMessageBox.information(self, "ذخیره شد", "تغییرات با موفقیت ذخیره شدند.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())