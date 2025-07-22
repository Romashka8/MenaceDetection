# -------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

from typing import List

import re

import tqdm

import logging

# -------------------------------------------------------------------------------------------------------

class OnlineParser:

	def __init__(self, config):
		
		self.config = config

	def parse_html(self, url):

		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")

		return soup

	def parse_headers(self, url, deep=1):

		parsed_headers = {}

		if self.config["header_suffix"]:
			url += self.config["header_suffix"]

		for d in tqdm.tqdm(range(1, deep + 1)):

			if self.config["header_slice"]:
				url = url[:url.rfind(self.config["header_slice"])] + self.config["header_suffix"] + str(d)

			soup = self.parse_html(url)

			posts = soup.find_all(self.config["header_container"], class_=self.config["header_classes"])
			dates = soup.find_all("time")
			date_slicer = 1

			for post in posts:

				content = post.find("a")
				title = content.text.strip()
				link = content[self.config["header_link_field"]]

				if self.config["header_prefix"]:
					link = self.config["header_prefix"] + link

				parsed_headers[title] = (link, dates[date_slicer - 1]["datetime"], dates[date_slicer]["datetime"])
				date_slicer += 2

		return parsed_headers

	def parse_comments(self, url, deep=1):

		pass

	def run_online(self, timeout):

		pass

# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

	pass

# -------------------------------------------------------------------------------------------------------
