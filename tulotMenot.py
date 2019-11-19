import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout, QLabel, QListWidget, QMessageBox)
from PyQt5.QtGui import QPalette


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.mainWidget = QWidget()
        self.mainWidget.setMinimumSize(QtCore.QSize(640, 480))
        self.mainWidget.setWindowTitle("menoTulo")
        self.grid = QVBoxLayout()
        self.ui()

    def inputGrid(self):
        self.inputGrid = QHBoxLayout()
        self.otsikko = QLineEdit(self)
        self.summa = QLineEdit(self)
        self.otsikko.setPlaceholderText("Tulon/menon kuvaus...")
        self.summa.setPlaceholderText("Summa...")
        self.inputGrid.addWidget(self.otsikko)
        self.inputGrid.addWidget(self.summa)
        self.grid.addLayout(self.inputGrid)

    def nappiGrid(self):
        self.nappiGrid = QHBoxLayout()

        self.tuloButton = QPushButton("Lisää tulo", self)
        self.menoButton = QPushButton("Lisää meno", self)

        self.tuloButton.clicked.connect(self.addTulo)
        self.menoButton.clicked.connect(self.addMeno)

        self.nappiGrid.addWidget(self.tuloButton)
        self.nappiGrid.addWidget(self.menoButton)
        self.grid.addLayout(self.nappiGrid)

    def listaGrid(self):
        self.listaGrid = QHBoxLayout()
        self.tuloLista = QListWidget()
        self.menoLista = QListWidget()

        self.tuloLista.itemClicked.connect(self.deleteItem)
        self.menoLista.itemClicked.connect(self.deleteItem)

        self.listaGrid.addWidget(self.tuloLista)
        self.listaGrid.addWidget(self.menoLista)
        self.grid.addLayout(self.listaGrid)

    def totalGrid(self):
        self.totalGrid = QHBoxLayout()

        self.totalSum = 0
        self.totalMenot = 0
        self.totalTulot = 0

        self.tuloLabel = QLabel()
        self.sumLabel = QLabel()
        self.menoLabel = QLabel()
        self.clearButton = QPushButton("TYHJENNÄ KAIKKI", self)
        self.clearButton.clicked.connect(self.clearAll)

        self.totalGrid.addWidget(self.tuloLabel)
        self.totalGrid.addWidget(self.sumLabel)
        self.totalGrid.addWidget(self.menoLabel)
        self.totalGrid.addWidget(self.clearButton)
    
        self.tuloLabel.setText("TULOT:")
        self.sumLabel.setText("TOTAL:")
        self.menoLabel.setText("MENOT:")

        self.grid.addLayout(self.totalGrid)

    def ui(self):
        self.inputGrid()
        self.nappiGrid()
        self.listaGrid()
        self.totalGrid()
        self.mainWidget.setLayout(self.grid)
        self.mainWidget.show()

    def virhe(self):
        QMessageBox.about(self, "Virhe", "Syötä summaan vain numeroita!")

    def poistoVarmistus(self):
        vastaus = QMessageBox.question(self, "Poista valittu",
        "Poistetaanko varmasti?", QMessageBox.No | QMessageBox.Yes)
        if vastaus == QMessageBox.Yes:
            return True
        return False

    def tyhjennysVarmistus(self):
        vastaus = QMessageBox.question(self, "Tyhjennä kaikki",
        "Oletko varma?", QMessageBox.No | QMessageBox.Yes)
        if vastaus == QMessageBox.Yes:
            return True
        return False

    def clearAll(self):
        if self.tyhjennysVarmistus():
            self.totalSum = 0
            self.totalMenot = 0
            self.totalTulot = 0
            self.tuloLista.clear()
            self.menoLista.clear()
            self.tuloLabel.setText("TULOT:")
            self.sumLabel.setText("TOTAL:")
            self.menoLabel.setText("MENOT:")


    def deleteItem(self):
        if self.sender() == self.tuloLista:
            lista = self.tuloLista
        else:
            lista = self.menoLista

        if not lista.selectedItems():
            return
        
        if self.poistoVarmistus():
            for item in lista.selectedItems():
                poistoSumma = int(lista.takeItem(lista.row(item)).text().split()[0])
                lista.takeItem(lista.row(item))
                if lista == self.tuloLista:
                    self.totalTulot -= poistoSumma
                else:
                    self.totalMenot -= poistoSumma
                self.updateTotal()

        self.tuloLista.clearSelection()
        self.menoLista.clearSelection()
        
    def updateTotal(self):
        self.tuloLabel.setText("TULOT: "+str(self.totalTulot))
        self.menoLabel.setText("MENOT: "+str(self.totalMenot))
        
        self.totalSum = self.totalTulot - self.totalMenot
        self.sumLabel.setText("TOTAL: "+str(self.totalSum))

    def addMeno(self):
        if not self.summa.text().isdigit():
            self.virhe()
            self.summa.clear()
        else:
            infoText = self.summa.text()+" "+self.otsikko.text()
            if infoText != " ":
                self.menoLista.addItem(infoText)
                self.totalSum -= int(self.summa.text())
                self.sumLabel.setText("TOTAL: "+str(self.totalSum))
                self.totalMenot += int(self.summa.text())
                self.menoLabel.setText("MENOT: "+str(self.totalMenot))
                self.summa.clear()
                self.otsikko.clear()
            else:
                pass

    def addTulo(self):
        if not self.summa.text().isdigit():
            self.virhe()
            self.summa.clear()
        else:
            infoText = self.summa.text()+" "+self.otsikko.text()
            if infoText != " ":
                self.tuloLista.addItem(infoText)
                self.totalSum += int(self.summa.text())
                self.sumLabel.setText("TOTAL: "+str(self.totalSum))
                self.totalTulot += int(self.summa.text())
                self.tuloLabel.setText("TULOT: "+str(self.totalTulot))
                self.summa.clear()
                self.otsikko.clear()
            else:
                pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    sys.exit(app.exec_())
