import json
import os
import hashlib

from bs4 import BeautifulSoup
import requests



ROOT_URL = "https://svelte.dev/docs/svelte/overview"

session = requests.session()

def to_md5(message: str):
	return hashlib.md5(message.encode('utf-8')).hexdigest()


def get_page_html(page_url: str):
	md5_hash = to_md5(page_url)
	cache_path = f"cache/{md5_hash}.html"
	if os.path.isfile(cache_path):
		with open(cache_path) as f:
			html = f.read()
		return html

	response = session.get(page_url)
	with open(cache_path, "w") as f:
		f.write(response.text)
	print(f"Saved cache: {cache_path}")

	return get_page_html(page_url)


def get_soup(page_url: str):
	html = get_page_html(page_url)
	soup = BeautifulSoup(html, "lxml")
	return soup


def main():
	soup = get_soup(ROOT_URL)
	sidebar = soup.find("ul", class_="sidebar")
	li_tags = [li for li in sidebar.children if li.name == "li"]
	for li_tag in li_tags:
		title = li_tag.find("h3").text.strip()
		print(f"Section: {title}")
		a_tags = li_tag.find_all("a", class_="page")
		for a_tag in a_tags:
			page_title = a_tag.text.strip()
			page_href = f"https://svelte.dev{a_tag['href']}"
			print(f"\t{page_title} ({page_href})")


if __name__ == '__main__':
	main()
