#!/usr/bin/env python3

import json
import os
import sys

from pypub.epub import create_epub_from_htmls
from pypub.utils import get_soup, get_cache_path



AUTHOR = "Svelte Team"
BASE_URL = "https://svelte.dev"



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
			chapter_html_paths.append(get_cache_path(page_href))

	# print(f"Found {len(chapter_html_paths)} chapters.")
	create_epub_from_htmls(
		chapter_html_paths,
		output_filename=output_filename,
		title=title,
		author=AUTHOR
	)


def create_docs_epub(doc_name: str = "main"):
	match doc_name:
		case 'kit':
			docs_to_epub("https://svelte.dev/docs/kit/introduction", output_filename="sveltekit-docs.epub", title="SvelteKit Docs")
		case 'cli':
			docs_to_epub("https://svelte.dev/docs/cli/overview", output_filename="svelte-cli-docs.epub", title="Svelte CLI Docs")
		case 'main':
			docs_to_epub("https://svelte.dev/docs/svelte/overview", output_filename="svelte-docs.epub", title="Svelte Docs")
		case _:
			print(f"Unknown doc name: '{doc_name}'")


def main():
	args = sys.argv[1:]
	doc_name = args[0] if len(args) else 'main'

	if doc_name == "all":
		create_docs_epub('main')
		create_docs_epub('kit')
		create_docs_epub('cli')
	else:
		create_docs_epub(doc_name)


if __name__ == '__main__':
	main()
