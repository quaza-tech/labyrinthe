from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt,pyqtSignal
from PyQt6.QtGui import QKeySequence


class KeyBinder(QLineEdit):
    
    new_touche = pyqtSignal(str)
    
    def __init__(self, current_key, on_change,parent=None):
        super().__init__(parent)
        self.setText(str(current_key))
        self.on_change=on_change
        self.setReadOnly(True) # On ne veut pas qu'il tape au clavier normalement
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #1a120b;
                color: #e0ca82;
                border: 2px solid #3d2b1f;
                border-radius: 5px;
                font-family: 'Georgia';
                font-weight: bold;
                height: 40px;
            }
            QLineEdit:focus {
                border: 2px solid #e0ca82; /* Brille quand on attend la touche */
                background-color: #261b18;
            }
        """)

    # Cette fonction se déclenche dès qu'une touche est pressée
    def keyPressEvent(self, event):
        key = event.key()
        
        # On transforme le code de la touche en texte (ex: Qt.Key_Z -> "Z")
        key_text = QKeySequence(event.key()).toString()
        
        # Gestion des touches spéciales (Espace, Echap, etc.)
        if key == Qt.Key.Key_Space:
            key_text = "ESPACE"
        elif key == Qt.Key.Key_Escape:
            self.clearFocus() # Annule le changement
            return

        if key_text:
            self.setText(key_text)
            self.clearFocus() # Enlève le curseur une fois fini
            print(f"Nouvelle touche enregistrée : {key_text}")
            self.emit_touche()
            self.on_change(key_text)
    def emit_touche(self):
        self.new_touche.emit(self.text())
            