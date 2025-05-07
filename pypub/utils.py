import hashlib
import os

from bs4 import BeautifulSoup
import requests


session = requests.session()

def to_md5(message: str):
	return hashlib.md5(message.encode('utf-8')).hexdigest()


def get_cache_path(page_url: str):
	md5_hash = to_md5(page_url)
	cache_path = f"cache/{md5_hash}.html"
	return cache_path

def get_page_html(page_url: str):
	cache_path = get_cache_path(page_url)
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

