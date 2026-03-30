from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QInputDialog,
)
import sys

from verwaltungstool.number_systems.functions import (
    bin_to_dec,
    dec_to_bin,
    dec_to_hex,
    hex_to_dec,
)


def ask_and_check(module):
    prompt, answer, input_type = module.get_quiz()
    text, ok = QInputDialog.getText(None, "Quiz", prompt)
    if not ok:
        return
    if input_type == 'int':
        try:
            user = int(text)
        except ValueError:
            QMessageBox.warning(None, "Fehler", "Bitte eine Zahl eingeben!")
            return
        correct = (user == answer)
    else:
        user = text.strip().upper()
        correct = (user == str(answer).upper())

    if correct:
        QMessageBox.information(None, "Ergebnis", "Richtig!")
    else:
        QMessageBox.information(None, "Ergebnis", f"Falsch! Richtig wäre: {answer}")


def run():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("Zahlensysteme Quiz")
    layout = QVBoxLayout()

    btn1 = QPushButton("Binär -> Dezimal")
    btn2 = QPushButton("Dezimal -> Binär")
    btn3 = QPushButton("Dezimal -> Hexadezimal")
    btn4 = QPushButton("Hexadezimal -> Dezimal")
    btn5 = QPushButton("Beenden")

    btn1.clicked.connect(lambda: ask_and_check(bin_to_dec))
    btn2.clicked.connect(lambda: ask_and_check(dec_to_bin))
    btn3.clicked.connect(lambda: ask_and_check(dec_to_hex))
    btn4.clicked.connect(lambda: ask_and_check(hex_to_dec))
    btn5.clicked.connect(app.quit)

    for btn in (btn1, btn2, btn3, btn4, btn5):
        layout.addWidget(btn)

    w.setLayout(layout)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
