import requests
from bs4 import BeautifulSoup

from .defs import User , WordDefinition



class Query:
	@staticmethod
	def definitions(q:str , single=False):
		r = requests.get(f"https://www.urbandictionary.com/define.php?term={q}")
		soup = BeautifulSoup(r.text , "lxml")
		def_elements = []
		defs = []
		for i in soup.find("div" , {"id" : "content"}).find_all("div" , {"class":"def-panel"}):
			if(not i.div.div.div.text.endswith("Word of the Day")):
				def_elements.append(i)
		if(single):
			def_elements = def_elements[:1]
		for i in def_elements:
			word = (i.find("div" , {"class":"def-header"}).a.text)
			meaning = i.find("div" , {"class":"meaning"}).text
			example = i.find("div" , {"class":"example"}).text
			author = User(name=str(i.find("div" , {"class":"contributor"}).a.text) , href=f'https://www.urbandictionary.com{i.find("div" , {"class":"contributor"}).a.get("href")}')
			thumbs_up = int(i.find("a" , {"class" : "up"}).span.text)
			thumbs_down = int(i.find("a" , {"class" : "down"}).span.text)

			curr = WordDefinition(word=word , meaning=meaning , example=example , author=author , timestamp=i.find("div" , {"class":"contributor"}).text)
			curr.data["upvotes"] = thumbs_up
			curr.data["downvotes"] = thumbs_down
			defs.append(curr)
		if(single):
			return defs[0]
		else:
			return defs


def GetUserDefinitions(u:User):
		r = requests.get(u.href)
		soup = BeautifulSoup(r.text , "lxml")
		def_elements = []
		defs = []
		for i in soup.find("div" , {"id" : "content"}).find_all("div" , {"class":"def-panel"}):
			if(not i.div.div.div.text.endswith("Word of the Day")):
				def_elements.append(i)

		for i in def_elements:
			word = (i.find("div" , {"class":"def-header"}).a.text)
			meaning = i.find("div" , {"class":"meaning"}).text
			example = i.find("div" , {"class":"example"}).text
			author = User(name=str(i.find("div" , {"class":"contributor"}).a.text) , href=f'https://www.urbandictionary.com{i.find("div" , {"class":"contributor"}).a.get("href")}')
			thumbs_up = int(i.find("a" , {"class" : "up"}).span.text)
			thumbs_down = int(i.find("a" , {"class" : "down"}).span.text)

			curr = WordDefinition(word=word , meaning=meaning , example=example , author=author , timestamp=i.find("div" , {"class":"contributor"}).text)
			curr.data["upvotes"] = thumbs_up
			curr.data["downvotes"] = thumbs_down
			defs.append(curr)

		return defs


def CategoryMeanings(cat:str , limit=10):
	cat_dict = {
	"college" : "https://www.urbandictionary.com/category.php?category=college",
	"drugs" : "https://www.urbandictionary.com/category.php?category=drugs",
	"food" : "https://www.urbandictionary.com/category.php?category=food",
	"internet" : "https://www.urbandictionary.com/category.php?category=internet",
	"music" : "https://www.urbandictionary.com/category.php?category=music",
	"name" : "https://www.urbandictionary.com/category.php?category=name" , 
	"relegion" : "https://www.urbandictionary.com/category.php?category=relegion" ,
	"sex" : "https://www.urbandictionary.com/category.php?category=sex",
	"sports" : "https://www.urbandictionary.com/category.php?category=sports",
	"work" : "https://www.urbandictionary.com/category.php?category=work"
	}
	if(cat in list(cat_dict.keys())):
		r = requests.get(cat_dict.get(cat))
		soup = BeautifulSoup(r.text , "lxml")
		words = soup.find("div" , {"id" : "columnist"}).ul.find_all("li")
		if(len(words) > limit):
			words = words[:limit]
		word_list = []
		for i in words:
			word_list.append(Query.definitions(i.a.text , single=True))
		return word_list
	else:
		raise ValueError("Category choice must be from " + str(list(cat_dict.keys())))


def WordofTheDay():
	r = requests.get("https://www.urbandictionary.com/")
	soup = BeautifulSoup(r.text , "lxml")

	wod = {}
	def_elements = soup.find("div" , {"id" : "content"}).find_all("div" , {"class":"def-panel"})

	for i in def_elements:
		word = (i.find("div" , {"class":"def-header"}).a.text)
		meaning = i.find("div" , {"class":"meaning"}).text
		example = i.find("div" , {"class":"example"}).text
		author = User(name=str(i.find("div" , {"class":"contributor"}).a.text) , href=f'https://www.urbandictionary.com{i.find("div" , {"class":"contributor"}).a.get("href")}')
		thumbs_up = int(i.find("a" , {"class" : "up"}).span.text)
		thumbs_down = int(i.find("a" , {"class" : "down"}).span.text)

		curr = WordDefinition(word=word , meaning=meaning , example=example , author=author , timestamp=i.find("div" , {"class":"contributor"}).text)
		curr.data["upvotes"] = thumbs_up
		curr.data["downvotes"] = thumbs_down
		wod[i.div.div.div.text] = (curr)
	return wod

