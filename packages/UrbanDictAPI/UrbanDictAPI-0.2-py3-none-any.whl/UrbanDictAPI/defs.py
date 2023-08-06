#Automatically creates a __repr__ method.
class AutoRepr:
	def __repr__(self):
		otpt = ""
		for i in self.__dict__:
			otpt = otpt+str(i)+"="
			if(type(self.__dict__.get(i)) == str):
				otpt=otpt+ '"'+ str(self.__dict__.get(i))+'"' + " , "
			else:
				otpt=otpt+ str(self.__dict__.get(i)) + " , "
		otpt = otpt[:-3]
		rtn = f'{self.__class__.__name__}({otpt})'
		return rtn


class User(AutoRepr):
	def __init__(self,name:str , href:str):
		self.name = name
		self.href = href
		self.data = {}

class WordDefinition(AutoRepr):
	def __init__(self,word:str , meaning:str , example:str , author:User ,timestamp:str=""):
		self.word = word
		self.meaning = meaning
		self.example = example
		self.author = author
		self.timestamp = timestamp
		self.data = {}