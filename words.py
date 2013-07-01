import sys
from PySide.QtCore import *
from PySide.QtGui import *

from word_list import *
from words_service import *
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL) # so that ctrl-c works

qt_app = QApplication(sys.argv)
client = MongoClient('localhost', 27017)

langs = ["English", "Afrikaans", "Zulu", "French", "Spanish", "Japanese", "Russian", "Mandarin"] #move to db?

class Words(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle("Words")
		self.setMinimumWidth(400)
		self.wordsService = WordsService(client)
		self.currentLanguage = "All languages"
		self.currentKeyword = ""
		self.initUI()


	def initUI(self):
		_layout = QVBoxLayout()
		self.dialog = AddDialog(langs)
		self.toolbar = Toolbar(self.dialog, langs)

		self.toolbar.searching.search.connect(self.search)
		self.toolbar.langs.activated[str].connect(self.languageChanged)
		self.dialog.saving.save.connect(self.saveWord)
		self.wordsTable = WordsTable([])

		_layout.addWidget(self.toolbar)
		_layout.addWidget(self.wordsTable)

		self.setLayout(_layout)


		self.refreshTable()

	def run(self):
		self.show()
		qt_app.exec_()


	def refreshTable(self):
		self.wordsTable.clear()
		self.wordsTable.showData( self.wordsService.search( self.currentKeyword, self.currentLanguage ) )
		self.show()

	@Slot(dict)
	def saveWord(self, word):
		self.wordsService.insert(word)
		self.refreshTable()

	@Slot(str)
	def search(self, keyword):
		self.currentKeyword = keyword
		self.refreshTable()

	@Slot(str)
	def languageChanged(self, lang):
		self.currentLanguage = lang
		self.refreshTable()

app = Words()
app.run()