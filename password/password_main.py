#---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------
# hier wird die passwort generriung gemacht <-----------------------------<-----------------------------<-------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------
# importe <-------------------
#-----------------------------
import secrets
import string
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
#-----------------------------
# passwort <------------------
#-----------------------------
def generate_random_password(length=12):
    """
    Generiert ein kryptographisch sicheres Passwort der angegebenen Länge.
    Enthält mindestens einen Großbuchstaben, eine Ziffer und ein Sonderzeichen.
    Verwendet secrets statt random (kryptographisch sicher).
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%^&*()" for c in password)):
            return password

class PasswordWindow(QWidget):
    """
    Gui für den Passwort Generator
    1. Label um das generierte Passwort anzuzeigen
    2. Textfeld um das Passwort anzuzeigen
    3. Button um ein neues Passwort zu generieren
    4. Beim Klicken auf den Button wird ein neues Passwort generiert und im Textfeld angezeigt
    5. Das Textfeld ist nur lesbar, um zu verhindern, dass der Benutzer das Passwort ändert
    6. Das Fenster hat den Titel "Passwort Generator"
    7. Die Länge des generierten Passworts ist standardmäßig 10 Zeichen
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Passwort Generator")
        layout = QVBoxLayout()

        self.label = QLabel("Generiertes Passwort:")
        layout.addWidget(self.label)
#----------------------------------------------
# -----> TEXT feld für generintes passwort<----
#----------------------------------------------
        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        layout.addWidget(self.password_field)
#----------------------------------------------
# -----> Button um Passwort zu generieren <----
#----------------------------------------------
        self.generate_btn = QPushButton("Passwort generieren")
        self.generate_btn.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_btn)

        self.setLayout(layout)

    def generate_password(self):
        """
        generiert ein neues Passwort und zeigt es im Textfeld an
        8 zeichen lang + 2 sonderregelzeichen = 10 chars
        1 großbuchstabe, 1 sonderzeichen, 8 zahlen
        """
        password = generate_random_password(12)
        self.password_field.setText(password)