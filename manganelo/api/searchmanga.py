import string
import typing
import dataclasses

from manganelo.api import APIBase


@dataclasses.dataclass
class MangaSearchResult:
	title: str
	url: str


class SearchManga(list, APIBase):
	def __init__(self, title: str) -> None:
		super().__init__()

		self.url = self._SEARCH_URL + self._format_title(title)

		self._page_soup = self._get_soup(self.url)

		self._perform_search()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		""" Context manager exit method """

	def _perform_search(self) -> typing.Iterable[MangaSearchResult]:
		panels = self._page_soup.find(class_="panel-search-story")

		if panels is None:
			raise Exception("Search failed")

		stories = panels.find_all(class_="search-story-item")

		# Iterate through the soup and extract the information
		for i, ele in enumerate(stories):
			item = ele.find(class_="item-img")

			title = item["title"]
			link = item["href"]

			manga_result = MangaSearchResult(title=title, url=link)

			self.append(manga_result)

	def _format_title(self, title: str) -> str:
		allowed_characters = string.ascii_letters + string.digits + "_"

		# Remove all characters which are not allowed and replace spaces with underscores
		return "".join([char.lower() for char in title.replace(" ", "_") if char in allowed_characters])
