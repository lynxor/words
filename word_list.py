import sys
from PySide.QtCore import *
from PySide.QtGui import *
from common import *

class WordsTable(QTableWidget):

	def __init__(self, words):
		QTableWidget.__init__(self)
		self.setColumnCount(5)
		self.showData(words)


	def showData(self, words):	
		self.setRowCount( len(words) )
		self.setHorizontalHeaderLabels(["Value", "Definition", "Examples", "Tags", "Language"])
		self.setSortingEnabled(False)
		for (row, word) in enumerate(words):

			items = [ QTableWidgetItem( word["value"] ), 
					  QTableWidgetItem(word["definition"]), 
					  QTableWidgetItem( "\n".join(word["examples"])), 
					  QTableWidgetItem( ", ".join(word["tags"]) ),
					  QTableWidgetItem( word.get("language", "?") ) ]

			for (col, item) in enumerate(items):
				self.setItem(row, col, item);
		self.setSortingEnabled(True)

class Search(QObject):
	search = Signal(str)

class Toolbar(QWidget):
	def __init__(self, dialog, languages):
		QWidget.__init__(self)
		self.dialog = dialog
		self.searching = Search()
		_layout = QHBoxLayout()

		addButton = QPushButton("Add Word")
		addButton.clicked.connect(self.showAddDialog)

		self.keyword = QLineEdit()
		self.keyword.returnPressed.connect(self.search)
		searchButton = QPushButton("Search")
		searchButton.clicked.connect(self.search)

		self.langs = QComboBox()
		self.langs.addItems( ["All languages"] + languages )
		self.langs.setInsertPolicy(QComboBox.NoInsert)

		_layout.addWidget(addButton)
		_layout.addWidget(self.keyword)
		_layout.addWidget(searchButton)
		_layout.addWidget(self.langs)
		self.setLayout(_layout)

	def showAddDialog(self):
		self.dialog.show()

	def search(self):
		self.searching.search.emit( self.keyword.text() )

class Save(QObject):
	save = Signal(dict)

class AddDialog(QDialog):
	def __init__(self, languages):
		QDialog.__init__(self)
		self.setWindowTitle("Add new word")
		self.setMinimumWidth(150)
		self.saving = Save()

		_layout = QGridLayout()
		
		self.value = QLineEdit()
		self.definition = QLineEdit()
		self.examples = QLineEdit()
		self.tags = QLineEdit()
		self.langs = QComboBox()
		self.langs.addItems(languages)
		self.langs.setInsertPolicy(QComboBox.InsertAtBottom)

		saveButton = QPushButton("Save")
		saveButton.clicked.connect(self.save)

		formRows = chunks( [ QLabel("Value"), self.value,
			QLabel("Definition"), self.definition, 
			QLabel("Examples"), self.examples, 
			QLabel("Tags"),  self.tags,
			QLabel("Language"),self.langs,
			saveButton], 2)
		for (rcount, row) in enumerate(formRows):
			for (cCount, item) in enumerate(row):
				_layout.addWidget(item, rcount, cCount)

		self.setLayout(_layout)


	def save(self):
		# just emit a save event
		theword = {"value": self.value.text(), "definition": self.definition.text(), 
			"examples" : self.examples.text().split(","), "tags": self.tags.text().split(","), "language" : self.langs.currentText()}
		self.value.setText("")
		self.definition.setText("")
		self.tags.setText("")
		self.examples.setText("")

		self.saving.save.emit(theword)
		self.close()


class WordItem(QWidget):

	def __init__(self, word):
		QWidget.__init__(self)
		_layout = QHBoxLayout()

		the_word = QLabel(word["value"])
		definition = QLabel(word["definition"])
		examples = QLabel( "\n".join(word["examples"]))
		tags = QLabel( ", ".join(word["tags"]) )

		_layout.addWidget(the_word)
		_layout.addWidget(definition)
		_layout.addWidget(examples)
		_layout.addWidget(tags)

		self.setLayout(_layout)


