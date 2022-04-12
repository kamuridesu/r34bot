import requests
from bs4 import BeautifulSoup
from typing import Generator
try:
	from helpers import Logger
except:
	from .helpers import Logger


class Rule34Paheal:
	def __init__(self):
		self.base_url: str = "https://rule34.paheal.net/"

	def parse_image_to_list(self, content: bytes) -> list:
		soup = BeautifulSoup(content, 'html.parser')
		div = soup.findAll("div", class_="shm-thumb")
		x = []
		total_pages = 0
		for tag in div:
			a_tag = tag.findAll("a")
			tags = None
			url = None
			for a in a_tag:
				if "File Only" in a.text.strip():
					url = (a['href'])
				if "" == a.text.strip():
					tags = ", ".join((a.find("img")['title'].split("\n")[0]).split(" "))
			x.append({"tags": tags, "url": url})

		total_results = soup.find("section", id="paginator")
		for res in total_results.findAll("a"):
			if "Last" in res.text.strip():
				total_pages = int(res['href'].split("/")[-1])

		return {
			"total": total_pages,
			"content": x
		}

	def checker(self, query: str) -> dict:
		url = "https://rule34.paheal.net/api/internal/autocomplete?s=" + str(query)
		response = requests.get(url)
		if response.status_code == 200:
			content = response.json()
			if content:
				total_content = int(content[list(content.keys())[0]])
				total_pages = total_content // 70
				if total_content % 70 != 0:
					total_pages += 1
				return {
					"total_pages": total_pages,
					"canon_name": list(content.keys())[0]
				}
		return False

	def check_if_exists(self, query: str) -> str:
		exists_all = True
		for x in query.split(" "):
			if self.checker(x) is False:
				exists_all = False
		return exists_all

	def search(self, query: str, pages_to_get: int = 1) -> list:
		pages_to_get = int(pages_to_get)
		if self.check_if_exists(query) is False:
			return False
		actual_page = 1
		hh_content = []
		while actual_page <= pages_to_get:
			search_url = self.base_url + f"/post/list/{query}/{actual_page}"
			response = requests.get(search_url)
			infos = self.parse_image_to_list(response.content)
			if infos['total'] < pages_to_get:
				pages_to_get = infos['total']
			yield infos['content']
			actual_page += 1

	def get_content(self, query: str, **kwargs) -> Generator[str, None, None]:
		fetched_content = self.search(query, kwargs['pages'])
		per_page = int(kwargs['per_page'])
		content = []
		for x in fetched_content:
			if len(x) < per_page:
				per_page = len(x)
			for y in x:
				content.append(y)
				if len(content) == per_page:
					yield content
					content = []
					break


# r34 = Rule34Paheal()
# # # r34.check_if_exists("hilda")
# x = r34.get_content("tuber porkyman", **{"pages": 1, "per_page": 70})
# print(x)
# for y in x:
# 	print(y)