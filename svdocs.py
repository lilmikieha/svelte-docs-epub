#!/usr/bin/env python3

import json
import os
import hashlib

from bs4 import BeautifulSoup
import requests

from pypub.epub import create_epub_from_htmls



AUTHOR = "Svelte Team"
BASE_URL = "https://svelte.dev"

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


def docs_to_epub(root_url, output_filename, title):
	soup = get_soup(root_url)
	sidebar = soup.find("ul", class_="sidebar")
	li_tags = [li for li in sidebar.children if li.name == "li"]
	chapter_html_paths = []
	for li_tag in li_tags:
		section_title = li_tag.find("h3").text.strip()
		# print(f"Section: {section_title}")
		a_tags = li_tag.find_all("a", class_="page")
		for a_tag in a_tags:
			page_title = a_tag.text.strip()
			page_href = f"{BASE_URL}{a_tag['href']}"
			# print(f"\t{page_title} ({page_href})")
			get_page_html(page_href)
			chapter_html_paths.append(get_cache_path(page_href))

	print(f"Found {len(chapter_html_paths)} chapters.")
	create_epub_from_htmls(
		chapter_html_paths,
		output_filename=output_filename,
		title=title,
		author=AUTHOR
	)


def main():
	docs_to_epub("https://svelte.dev/docs/svelte/overview", output_filename="svelte-docs.epub", title="Svelte Docs")
	docs_to_epub("https://svelte.dev/docs/kit/introduction", output_filename="sveltekit-docs.epub", title="SvelteKit Docs")
	docs_to_epub("https://svelte.dev/docs/cli/overview", output_filename="svelte-cli-docs.epub", title="Svelte CLI Docs")


if __name__ == '__main__':
	main()
