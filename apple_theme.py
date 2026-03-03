"""
Apple-Style QSS Theme für Verwaltungstool.
Orientiert an Apples Human Interface Guidelines:
  - Farben:  #007AFF (Systemblau), #F2F2F7 (Hintergrund), #1C1C1E (Text)
  - Radius:  8–12 px
  - Schrift: Systemfont (-apple-system / SF Pro)
"""

APPLE_STYLESHEET = """
/* ── Basis ─────────────────────────────────────────────── */
QWidget {
    background-color: #F2F2F7;
    color: #1C1C1E;
    font-family: -apple-system, "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}

QMainWindow {
    background-color: #F2F2F7;
}

/* ── Primäre Buttons ────────────────────────────────────── */
QPushButton {
    background-color: #007AFF;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 500;
    min-height: 32px;
}

QPushButton:hover {
    background-color: #0062CC;
}

QPushButton:pressed {
    background-color: #004EA8;
}

QPushButton:disabled {
    background-color: #C7C7CC;
    color: #EBEBF5;
}

/* Sekundäre Buttons – property secondary=true setzen */
QPushButton[secondary="true"] {
    background-color: #E5E5EA;
    color: #1C1C1E;
    border: none;
}

QPushButton[secondary="true"]:hover {
    background-color: #D1D1D6;
}

/* Destruktive Buttons – property destructive=true setzen */
QPushButton[destructive="true"] {
    background-color: #FF3B30;
    color: white;
}

QPushButton[destructive="true"]:hover {
    background-color: #CC2F26;
}

/* ── Module-Karten-Buttons (Hauptmenü) ──────────────────── */
QPushButton[module="true"] {
    background-color: white;
    color: #1C1C1E;
    border: none;
    border-radius: 12px;
    padding: 14px 10px;
    font-size: 13px;
    font-weight: 500;
    min-height: 52px;
    text-align: center;
}

QPushButton[module="true"]:hover {
    background-color: #F0F0F5;
}

QPushButton[module="true"]:pressed {
    background-color: #E5E5EA;
}

/* ── Labels ─────────────────────────────────────────────── */
QLabel {
    background: transparent;
    color: #1C1C1E;
}

QLabel[heading="true"] {
    font-size: 15px;
    font-weight: 600;
    color: #1C1C1E;
}

QLabel[caption="true"] {
    font-size: 11px;
    color: #8E8E93;
}

/* ── Eingabefelder ──────────────────────────────────────── */
QLineEdit {
    background-color: white;
    border: 1px solid #C7C7CC;
    border-radius: 8px;
    padding: 7px 10px;
    font-size: 13px;
    color: #1C1C1E;
    selection-background-color: #007AFF;
}

QLineEdit:focus {
    border: 1.5px solid #007AFF;
}

QLineEdit:read-only {
    background-color: #F2F2F7;
    color: #3A3A3C;
}

/* ── Dropdowns ──────────────────────────────────────────── */
QComboBox {
    background-color: white;
    border: 1px solid #C7C7CC;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 13px;
    color: #1C1C1E;
    min-height: 30px;
}

QComboBox:focus {
    border: 1.5px solid #007AFF;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #C7C7CC;
    border-radius: 8px;
    selection-background-color: #007AFF;
    selection-color: white;
    padding: 4px;
}

/* ── Checkboxen & Radiobuttons ──────────────────────────── */
QCheckBox, QRadioButton {
    background: transparent;
    color: #1C1C1E;
    spacing: 6px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 1.5px solid #C7C7CC;
    border-radius: 4px;
    background-color: white;
}

QCheckBox::indicator:checked {
    background-color: #007AFF;
    border-color: #007AFF;
}

QRadioButton::indicator {
    border-radius: 9px;
}

QRadioButton::indicator:checked {
    background-color: #007AFF;
    border-color: #007AFF;
}

/* ── Kalender ───────────────────────────────────────────── */
QCalendarWidget {
    background-color: white;
    border: 1px solid #E5E5EA;
    border-radius: 12px;
}

QCalendarWidget QToolButton {
    background-color: transparent;
    color: #007AFF;
    border: none;
    font-size: 13px;
    font-weight: 500;
    padding: 4px 8px;
    border-radius: 6px;
}

QCalendarWidget QToolButton:hover {
    background-color: #E5E5EA;
}

QCalendarWidget QMenu {
    background-color: white;
    border: 1px solid #C7C7CC;
    border-radius: 8px;
}

QCalendarWidget QSpinBox {
    background-color: white;
    border: 1px solid #C7C7CC;
    border-radius: 6px;
    padding: 3px 6px;
    color: #1C1C1E;
}

QCalendarWidget QAbstractItemView:enabled {
    background-color: white;
    color: #1C1C1E;
    selection-background-color: #007AFF;
    selection-color: white;
}

QCalendarWidget QAbstractItemView:disabled {
    color: #C7C7CC;
}

/* ── Dialoge ────────────────────────────────────────────── */
QDialog {
    background-color: #F2F2F7;
    border-radius: 14px;
}

QDialogButtonBox QPushButton {
    min-width: 80px;
}

/* ── Scrollbars ─────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #C7C7CC;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: #C7C7CC;
    border-radius: 4px;
    min-width: 20px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

/* ── Card-Frame ─────────────────────────────────────────── */
QFrame[card="true"] {
    background-color: white;
    border: none;
    border-radius: 12px;
}

/* ── MessageBox ─────────────────────────────────────────── */
QMessageBox {
    background-color: #F2F2F7;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""
