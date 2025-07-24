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
		self.logger = logging.getLogger(__name__)

	def parse_html(self, url):

		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")

		return soup

	def parse_headers(self, url, deep=1):

		parsed_headers = {}

		if self.config["header_suffix"]:
			url += self.config["header_suffix"]

		for d in range(1, deep + 1):

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
		
		parsed_comments = []

		for d in range(1, deep + 1):

			if self.config["comment_slice"]:
				url = url[:url.rfind(self.config["comment_slice"])] + self.config["comment_suffix"] + str(d)

			soup = self.parse_html(url)
			soup.features = "lxml"
			comments = soup.find_all(self.config["comment_container"], class_=self.config["comment_classes"])

			for com in comments[self.config["skip_first"]:]:

				try:
					if self.config["comment_text_container"] and self.config["comment_date_container"]:
						parsed = re.sub(r"\s+", " ", com.find(self.config["comment_text_container"]).text)
						parsed_date = com.find(self.config["comment_date_container"])[self.config["comment_date_atr"]]
					else:
						parsed = re.sub(r"\s+", " ", com.text)
						parsed_date = com[self.config["comment_date_atr"]]

					if (parsed, parsed_date) not in parsed_comments:
						parsed_comments.append((parsed, parsed_date))
				
				except KeyError:
					self.logger.warning(f"""
						KeyError trying to parse {str(com)[:10]} in {url}...
					""")

				except AttributeError:
					self.logger.warning(f"""
						AttributeError trying to parse {str(com)[:10]} in {url}...
					""")

				finally:
					if (parsed, "dd:mm:yy") not in parsed_comments:
						parsed_comments.append((parsed, "dd:mm:yy"))

		return parsed_comments

# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

	pass

# -------------------------------------------------------------------------------------------------------
