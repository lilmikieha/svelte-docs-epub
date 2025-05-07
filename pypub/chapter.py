import uuid

from .utils import get_soup



class EpubChapter:
	def __init__(self, url):
		self.url = url
		self.uuid = uuid.uuid4()
		self.soup = None

	@property
	def output_filepath(self):
		return f"texts/text-{self.uuid}.xhtml"

	def setup_soup(self):
		if not self.soup:
			self.soup = get_soup(self.url)

	def get_title(self):
		if not self.soup:
			self.setup_soup()
		return self.soup.title.decode_contents()

	def get_content(self):
		if not self.soup:
			self.setup_soup()
		docs_content = self.soup.find("div", id="docs-content")
		for div in docs_content.find_all("div", class_="breadcrumbs"):
			div.decompose() # removes breadcrumbs

		for span in docs_content.find_all("span", class_="twoslash-popup-container"):
			span.decompose() # removes code popups

		for p in docs_content.find_all("p", class_="edit"):
			p.decompose() # removes edit section

		for div in docs_content.find_all("div", class_="controls"):
			div.decompose() # removes next/previous links

		for details_tag in docs_content.find_all('details'):
			details_tag.name = 'div'

		for summary_tag in docs_content.find_all('summary'):
			summary_tag.name = 'h4'

		for tag in docs_content.find_all(True):
			if tag.name in ['input', 'button']:
				tag.decompose()
			else:
				tag.attrs = {}
		return str(docs_content)

