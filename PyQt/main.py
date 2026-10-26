import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)




# Zakładka 1: wyświetlanie obrazu
class ImageTab(QWidget):
    FILE_FILTER = "Obrazy (*.png *.jpg *.jpeg *.bmp *.gif)"

    def __init__(self):
        super().__init__()

        self.image_label = QLabel("Wybierz obraz z menu: Task 1 -> Open")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pixmap = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Otwórz obraz", "", self.FILE_FILTER
        )
        if not path:
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.image_label.setText("Nie udało się wczytać obrazu.")
            return

        self.pixmap = pixmap
        self.show_scaled_image()

    def show_scaled_image(self):
        if self.pixmap is None:
            return
        scaled = self.pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.show_scaled_image()




# Zakładka 2: notatnik
class NotepadTab(QWidget):
    FILE_FILTER = "Pliki tekstowe (*.txt);;Wszystkie pliki (*)"

    def __init__(self):
        super().__init__()

        self.file_path = ""

        self.editor = QPlainTextEdit()

        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)

    def clear(self):
        self.editor.clear()
        self.file_path = ""

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Otwórz plik", "", self.FILE_FILTER
        )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            self.editor.setPlainText(f.read())
        self.file_path = path

    def save(self):
        if not self.file_path:
            self.save_as()
        else:
            self._write(self.file_path)

    def save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Zapisz plik", "", self.FILE_FILTER
        )
        if not path:
            return

        self.file_path = path
        self._write(path)

    def _write(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.editor.toPlainText())





# Zakładka 3: trzy pola i ich złączenie
class FieldsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.field_a = QLineEdit()  # pole tekstowe
        self.field_b = QLineEdit()  # pole tekstowe
        self.field_c = QSpinBox()  # pole numeryczne
        self.field_c.setRange(-1000000, 1000000)

        self.field_result = QLineEdit()  # wynik A + B + C
        self.field_result.setReadOnly(True)

        layout = QFormLayout(self)
        layout.addRow("Pole A:", self.field_a)
        layout.addRow("Pole B:", self.field_b)
        layout.addRow("Pole C:", self.field_c)
        layout.addRow("Pole A + B + C:", self.field_result)

        self.field_a.textChanged.connect(self.update_result)
        self.field_b.textChanged.connect(self.update_result)
        self.field_c.valueChanged.connect(self.update_result)

        self.update_result()

    def update_result(self):
        self.field_result.setText(
            f"{self.field_a.text()}{self.field_b.text()}{self.field_c.value()}"
        )

    def clear(self):
        self.field_a.clear()
        self.field_b.clear()
        self.field_c.setValue(0)





# Okno główne
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt")
        self.resize(700, 500)

        # Zakładki
        self.image_tab = ImageTab()
        self.notepad_tab = NotepadTab()
        self.fields_tab = FieldsTab()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.image_tab, "Task 1 - Obraz")
        self.tabs.addTab(self.notepad_tab, "Task 2 - Notatnik")
        self.tabs.addTab(self.fields_tab, "Task 3 - Pola")
        self.setCentralWidget(self.tabs)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        # File
        file_menu = menu_bar.addMenu("&File")
        self.add_action(file_menu, "&Exit", "Ctrl+Q", self.close)

        # Task 1
        task1_menu = menu_bar.addMenu("Task &1")
        self.add_action(task1_menu, "&Open", "Ctrl+I", self.task1_open)

        # Task 2
        task2_menu = menu_bar.addMenu("Task &2")
        self.add_action(task2_menu, "&Clear", "Ctrl+Shift+N", self.task2_clear)
        self.add_action(task2_menu, "&Open", "Ctrl+O", self.task2_open)
        self.add_action(task2_menu, "&Save", "Ctrl+S", self.task2_save)
        self.add_action(task2_menu, "Save &as", "Ctrl+Shift+S", self.task2_save_as)

        # Task 3
        task3_menu = menu_bar.addMenu("Task &3")
        self.add_action(task3_menu, "&Clear", "Ctrl+L", self.task3_clear)

    def add_action(self, menu, text, shortcut, handler):
        action = QAction(text, self)
        action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(handler)
        menu.addAction(action)

    def task1_open(self):
        self.tabs.setCurrentWidget(self.image_tab)
        self.image_tab.open_image()

    def task2_clear(self):
        self.tabs.setCurrentWidget(self.notepad_tab)
        self.notepad_tab.clear()

    def task2_open(self):
        self.tabs.setCurrentWidget(self.notepad_tab)
        self.notepad_tab.open_file()

    def task2_save(self):
        self.tabs.setCurrentWidget(self.notepad_tab)
        self.notepad_tab.save()

    def task2_save_as(self):
        self.tabs.setCurrentWidget(self.notepad_tab)
        self.notepad_tab.save_as()

    def task3_clear(self):
        self.tabs.setCurrentWidget(self.fields_tab)
        self.fields_tab.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
