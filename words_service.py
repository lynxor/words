from pymongo import *
import datetime
import sys
import re


class WordsService():
	ALL = "All languages"
	def __init__(self, client):
		db = client.words
		self.word = db.word

	def insert(self, word):
		return self.word.insert(word)

	def retrieveAll(self, lang):
		query = {"language" : lang}
		if(lang == self.ALL):
			query = {}

		return list(self.word.find(query))

	def search(self, keyword, lang):
		regex = re.compile( ".*" + ".*".join(keyword.split(",")) + ".*", re.IGNORECASE)
		query = {"$or" : [{"value" : regex}, {"definition": regex}, {"examples": regex}, {"tags": regex}]}
		if(lang != self.ALL):
			query["language"] = lang;

		return list(self.word.find(query))




