# -------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

from typing import List

import re

import tqdm

import logging

# -------------------------------------------------------------------------------------------------------

class StaticParser:

	def __init__(self,
				 topic_classes: List[str] = None,
				 topic_container: str = None,
				 topic_url_field: str = None,
				 topic_prefix: str = None,
				 topic_suffix: str = None,
				 topic_slice: str = None,
				 comment_classes: List[str] = None,
				 comment_container: str = None,
				 comment_prefix: str = None,
				 comment_suffix: str = None,
				 comment_slice: str = None
				):

		self.logger = logging.getLogger(__name__)

		self.parsed_topics = {}
		self.parsed_comments = {}

		self.topic_classes = topic_classes
		self.topic_container = topic_container
		self.topic_url_field = topic_url_field

		self.topic_prefix = topic_prefix
		self.topic_suffix = topic_suffix
		self.topic_slice = topic_slice

		if not self.topic_classes: self.logger.warning("WARNING: not specified HTML/CSS classes for topic containers! Specify them when you wil parse topics!")
		if not self.topic_container: self.logger.warning("WARNING: not specified HTML container with topics! Specify it when you wil parse topics!")
		if not self.topic_url_field: self.logger.warning("WARNING: not specified HTML atribute in link with topic! Specify it when you wil parse topics!")

		self.comment_classes = comment_classes
		self.comment_container = comment_container

		if not self.comment_classes: self.logger.warning("WARNING: not specified HTML/CSS classes for comment containers! Specify them when you wil parse topics!")
		if not self.comment_container: self.logger.warning("WARNING: not specified HTML container with comments! Specify it when you wil parse topics!")

		self.comment_prefix = comment_prefix
		self.comment_suffix = comment_suffix
		self.comment_slice = comment_slice

	def parse_url(self,
				  url: str
				):

		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")

		return soup

	def parse_topics(self,
					 root_url: str,
					 deep = 1,

					 topic_classes: List[str]  | None = None,
				 	 topic_container: str | None = None,
				 	 topic_url_field: str | None = None
					):

		"""
		parsed: Dict[str, [str, list]]
		parsed = {"topic": url | [urls]}
		"""

		self.topic_classes = topic_classes if topic_classes else self.topic_classes
		self.topic_container = topic_container if topic_container else self.topic_container
		self.topic_url_field = topic_url_field if topic_url_field else self.topic_url_field

		assert self.topic_classes
		assert self.topic_container
		assert self.topic_url_field

		if self.topic_suffix: root_url += self.topic_suffix

		for d in range(1, deep + 1):

			if self.topic_slice:
				root_url = root_url[:root_url.rfind(self.topic_slice)] + self.topic_suffix + str(d)

			soup = self.parse_url(root_url)

			posts = soup.find_all(self.topic_container, class_=self.topic_classes)

			for post in posts:

				content = post.find("a")
				title = content.text.strip()
				url = content[self.topic_url_field]

				if self.topic_prefix: url = self.topic_prefix + url

				if title in self.parsed_topics:
					continue

				self.parsed_topics[title] = url

		return self.parsed_topics

	def parse_topic_comments(self,
							 topic_url: str,
							 topic_name: str,
							 deep: int = 1,
							 comment_classes: List[str] = None,
				 	 		 comment_container: str = None,
							):
		
		self.comment_classes = comment_classes if comment_classes else self.comment_classes
		self.comment_container = comment_container if comment_container else self.comment_container

		assert self.comment_classes
		assert self.comment_container

		if self.comment_prefix: topic_url = comment_prefix + topic_url
		if self.comment_suffix: topic_url += self.comment_suffix
		
		self.parsed_comments[topic_name] = []

		for d in range(1, deep + 1):

			if self.comment_slice:
				topic_url = topic_url[:topic_url.rfind(self.comment_slice)] + self.comment_suffix + str(d)

			soup = self.parse_url(topic_url)
			soup.features = "lxml"
			comments = soup.find_all(self.comment_container, class_ = self.comment_classes)

			for com in comments:
				try:
					
					parsed = re.sub(r"\s+", " ", com.text)

					if parsed in self.parsed_comments[topic_name]:
						continue

					self.parsed_comments[topic_name].append(parsed)
				
				except AttributeError:
					continue

		return self.parsed_comments

# -------------------------------------------------------------------------------------------------------

def build_kupus_parser():

	kupus_parser = StaticParser(
		topic_classes = ["ipsType_break ipsContained"],
		topic_container = "span", 
		topic_url_field = "data-ipshover-target",
		comment_classes = ["ipsType_normal", "ipsType_richText", "ipsPadding_bottom", "ipsContained"],
		comment_container = "div",
		comment_suffix = "page/",
		comment_slice = "?preview"
	)

	return kupus_parser

def build_hranidengi_parser():

	hranidengi_parser = StaticParser(
		topic_classes = ["structItem-title"],
		topic_container = "div", 
		topic_url_field = "href",
		topic_prefix = "https://hranidengi.com",
		comment_classes = ["bbWrapper", "message-userContent", "lbContainer", "js-lbContainer"],
		comment_container = "div",
		comment_suffix = "page-",
		comment_slice = "page"
	)

	return hranidengi_parser

def build_findozor_parser():

	findozor_parser = StaticParser(
		topic_classes = ["structItem-title"],
		topic_container = "div", 
		topic_url_field = "href",
		topic_prefix = "https://findozor.net",
		topic_suffix = 'page-',
		topic_slice = "page",
		comment_classes = ["bbWrapper", "message-userContent", "lbContainer", "js-lbContainer"],
		comment_container = "div",
		comment_suffix = "page-",
		comment_slice = "page"
	)

	return findozor_parser

def build_finforum_parser():

	finforum_parser = StaticParser(
		topic_classes = ["structItem-title"],
		topic_container = "div", 
		topic_url_field = "href",
		topic_prefix = "https://finforums.ru",
		comment_classes = ["bbWrapper", "message-userContent", "lbContainer", "js-lbContainer"],
		comment_container = "div",
		comment_suffix = "page-",
		comment_slice = "page"
	)

	return finforum_parser

# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

	test_parser = StaticParser(
		topic_classes = ["structItem-title"],
		topic_container = "div", 
		topic_url_field = "href",
		topic_prefix = "https://hranidengi.com",
		comment_classes = ["bbWrapper", "message-userContent", "lbContainer", "js-lbContainer"],
		comment_container = "div",
		comment_suffix = "page-",
		comment_slice = "page"
	)

	test_topics = test_parser.parse_topics("https://hranidengi.com/forums/kreditnaja-istorija/")

	print(test_topics, "\n")

	test_comments = test_parser.parse_topic_comments(
		"https://hranidengi.com/threads/nezakonnye-zaprosy-kreditnoj-istorii.229/",
		"Незаконные запросы кредитной истории",
		5
	)

	print(test_comments)

# -------------------------------------------------------------------------------------------------------
