from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout,QPushButton,QLineEdit,QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QGuiApplication
import sys

class login(QWidget):
    
    envoie_donnee = pyqtSignal(str,str,str)
    
    def __init__(self):
        super().__init__()
        self.loginPincipale = QVBoxLayout()
        # On réduit l'espace entre les éléments et on ajoute de grosses marges sur les côtés
        self.loginPincipale.setSpacing(10)
        self.loginPincipale.setContentsMargins(80, 20, 80, 40) 
        self.setLayout(self.loginPincipale)
        
        self.new_width = QGuiApplication.primaryScreen().size().width() // 3
        self.new_height = int(QGuiApplication.primaryScreen().size().height() // 1.5)
        self.resize(self.new_width, self.new_height)
        
        """ELEMENT DU LOGIN """
        self.labLogin = QLabel("CONNEXION")
        self.labERR = QLabel("ERR")
        self.labERR.hide()
        self.labERR.setObjectName("labERR") # Pour le cibler en QSS

        # On retire le addStretch() du haut pour remonter le titre
        self.email = QLineEdit()
        self.email.setPlaceholderText("E-mail : something@gmail.com")
        
        self.pseudo = QLineEdit()
        self.pseudo.hide()
        self.pseudo.setPlaceholderText("Pseudo")
        
        self.mdp = QLineEdit()
        self.mdp.setPlaceholderText("Password")
        self.mdp.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.layoutButton = QHBoxLayout()
        self.layoutButton.setSpacing(20) # Espace entre les deux boutons
        self.submit = QPushButton("Submit")
        self.createAccount = QPushButton("Create Account")
        
        """STYLE"""
        self.layoutButton.addWidget(self.submit)
        self.layoutButton.addWidget(self.createAccount)
        
        self.setObjectName("Login")
        with open("assets/style/Login.qss") as f:
            self.setStyleSheet(f.read())
        
        """INTEGRATION DES ELEMENTS"""
        # On ajuste les facteurs d'étirement (stretch) pour que le titre soit petit
        self.loginPincipale.addWidget(self.labERR)
        self.loginPincipale.addWidget(self.labLogin)
        self.loginPincipale.addWidget(self.email)
        self.loginPincipale.addWidget(self.pseudo)
        self.loginPincipale.addWidget(self.mdp)
        self.loginPincipale.addLayout(self.layoutButton)
        
        # On ajoute un stretch à la fin pour tout pousser vers le haut
        self.loginPincipale.addStretch()
        
        self.submit.clicked.connect(self.envoie)
        self.createAccount.clicked.connect(self.createNewAccount)
    
    def envoie(self):
        if self.pseudo.isHidden():
            if self.email.text() != "" and self.mdp.text() != "":
                self.envoie_donnee.emit(self.email.text(),self.mdp.text(),"")
        else:
            if self.email.text() != "" and self.mdp.text() != "" and self.pseudo.text() != "":
                self.envoie_donnee.emit(self.email.text(),self.mdp.text(),self.pseudo.text())
        
    def createNewAccount(self):
        self.pseudo.show()
        
    def messageERR(self,message : str):
        self.labERR.setText(message)
        self.labERR.show()
        